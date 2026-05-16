import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Topic
from ..ai import get_client, get_system_prompt, get_lesson_system

router = APIRouter(prefix="/api")

MODEL = "claude-sonnet-4-6"


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


def _no_key_stream():
    async def gen():
        msg = "<p>No API key set. Add <code>ANTHROPIC_API_KEY</code> as an environment variable in your Render dashboard, then redeploy.</p>"
        yield f"data: {json.dumps({'text': msg})}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")


@router.post("/chat/{topic_id}")
async def chat(topic_id: int, req: ChatRequest, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        async def err():
            yield f"data: {json.dumps({'text': '<p>Topic not found.</p>'})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(err(), media_type="text/event-stream")

    client = get_client()
    if not client:
        return _no_key_stream()

    system = get_system_prompt(topic.title, topic.notes)
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    if not messages:
        messages = [{"role": "user", "content": "Please start the quiz."}]

    async def stream():
        async with client.messages.stream(
            model=MODEL,
            max_tokens=1024,
            system=system,
            messages=messages,
        ) as s:
            async for text in s.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@router.post("/lesson/{topic_id}")
async def generate_lesson(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        async def err():
            yield f"data: {json.dumps({'text': '<p>Topic not found.</p>'})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(err(), media_type="text/event-stream")

    client = get_client()
    if not client:
        return _no_key_stream()

    system = get_lesson_system()

    async def stream():
        async with client.messages.stream(
            model=MODEL,
            max_tokens=2048,
            system=system,
            messages=[{
                "role": "user",
                "content": f"Generate a detailed lesson on: {topic.title}\n\nMy current understanding: {topic.notes}",
            }],
        ) as s:
            async for text in s.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
