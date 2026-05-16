from datetime import date
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Topic, ReviewLog
from ..srs import calculate_next_review

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/review")
def review_page(request: Request, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.next_review_date <= date.today()).first()
    if not topic:
        return RedirectResponse("/", status_code=303)
    remaining = db.query(Topic).filter(Topic.next_review_date <= date.today()).count()
    return templates.TemplateResponse(request, "review.html", {
        "topic": topic,
        "remaining": remaining,
    })


@router.post("/review/{topic_id}")
def submit_review(
    topic_id: int,
    rating: int = Form(...),
    db: Session = Depends(get_db),
):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        return RedirectResponse("/", status_code=303)

    result = calculate_next_review(
        rating=rating,
        interval_days=topic.interval_days,
        ease_factor=topic.ease_factor,
        review_count=topic.review_count,
    )

    topic.next_review_date = result.next_review_date
    topic.interval_days = result.interval_days
    topic.ease_factor = result.ease_factor
    topic.review_count = result.review_count

    db.add(ReviewLog(topic_id=topic_id, rating=rating))
    db.commit()

    return RedirectResponse("/review", status_code=303)
