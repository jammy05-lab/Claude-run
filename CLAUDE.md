# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A spaced repetition web app for tracking and reviewing things you've learned. You add topics with notes in your own words; the SM-2 algorithm schedules when to review each one so knowledge moves into long-term memory. Daily review sessions aim for ~10 minutes.

## Commands

```bash
uv sync                                          # install dependencies
uv run uvicorn app.main:app --reload             # dev server at localhost:8000
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000  # expose externally
```

No test suite yet. Verify manually by adding a topic and completing a review.

## Architecture

```
app/
  main.py          # FastAPI app — mounts /static, creates DB tables on startup, includes routers
  database.py      # SQLite engine + SessionLocal + get_db dependency
  models.py        # Topic (title, notes, category, SM-2 fields) + ReviewLog
  srs.py           # SM-2 algorithm as a pure function — the core scheduling logic
  routers/
    topics.py      # GET / (dashboard), GET+POST /add
    reviews.py     # GET /review (next due topic), POST /review/{id} (submit rating)
  templates/       # Jinja2 — base.html, dashboard.html, add.html, review.html
static/
  style.css        # All styles (no framework)
learning.db        # SQLite file, created at first run (gitignored)
```

## Key Concepts

**SM-2 scheduling** (`app/srs.py`): After each review the user rates recall 1–5. Ratings ≥ 3 grow the interval (1 day → 6 days → interval × ease_factor). Ratings < 3 reset to interval=1, review_count=0. Ease factor adjusts up on 5s, down on 3s, unchanged on 4s — so hard topics come back sooner automatically.

**Template API**: Uses Starlette 1.0.0 — `request` is the first positional argument, not part of the context dict:
```python
# correct
templates.TemplateResponse(request, "template.html", {"key": value})
# wrong (old API)
templates.TemplateResponse("template.html", {"request": request, "key": value})
```

**Review flow**: Dashboard shows due count → `/review` loads the first due topic → user clicks `<details>` to reveal their notes → submits a 1–5 rating → SM-2 recalculates → loops until no topics remain → redirects to dashboard.

## Development Branch

Active development on `claude/add-claude-documentation-PRxkq`; `main` is stable.
