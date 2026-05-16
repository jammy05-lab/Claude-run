import os
from pathlib import Path
from anthropic import AsyncAnthropic

SKILLS_PATH = Path("skills.md")

DEFAULT_SYSTEM = """You are a personal learning tutor. Your job is to quiz the user on topics they have learned, evaluate their answers honestly, and explain mistakes clearly.

Format all responses as HTML:
- Use <p>, <strong>, <em>, <ul>, <li>, <code>, <pre><code> for structure
- Use $...$ for inline math and $$...$$ for display math (LaTeX)
- Ask one focused question at a time when quizzing
- After the user has answered, suggest a self-rating: "I'd suggest rating yourself X/5 because..."
"""


def get_system_prompt(topic_title: str, topic_notes: str) -> str:
    base = SKILLS_PATH.read_text() if SKILLS_PATH.exists() else DEFAULT_SYSTEM
    return f"""{base}

<topic>
Title: {topic_title}
User's notes: {topic_notes}
</topic>

Begin by asking one question to test their understanding of this topic."""


def get_lesson_system() -> str:
    base = SKILLS_PATH.read_text() if SKILLS_PATH.exists() else ""
    return f"""{base}

Generate a comprehensive, well-structured lesson. Use rich HTML formatting.
Use $...$ for inline LaTeX and $$...$$ for display math. Start with intuition, then formalism. Include examples."""


def get_client() -> AsyncAnthropic | None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    return AsyncAnthropic(api_key=key) if key else None
