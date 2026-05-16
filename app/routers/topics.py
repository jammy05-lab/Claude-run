from datetime import date
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Topic

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    due_count = db.query(Topic).filter(Topic.next_review_date <= date.today()).count()
    topics = db.query(Topic).order_by(Topic.created_at.desc()).all()
    est_minutes = max(1, round(due_count * 0.4))
    return templates.TemplateResponse(request, "dashboard.html", {
        "due_count": due_count,
        "topics": topics,
        "est_minutes": est_minutes,
    })


@router.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse(request, "add.html")


@router.post("/add")
def add_topic(
    title: str = Form(...),
    notes: str = Form(...),
    category: str = Form(""),
    db: Session = Depends(get_db),
):
    topic = Topic(
        title=title.strip(),
        notes=notes.strip(),
        category=category.strip() or None,
        next_review_date=date.today(),
    )
    db.add(topic)
    db.commit()
    return RedirectResponse("/", status_code=303)
