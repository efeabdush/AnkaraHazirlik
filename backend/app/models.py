import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def uid() -> str:
    return str(uuid.uuid4())


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    kind: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(200))
    topic: Mapped[str] = mapped_column(String(120), default="")
    cefr: Mapped[str] = mapped_column(String(16), default="B1+")
    source: Mapped[str] = mapped_column(String(32), default="seed")
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    transcript_json: Mapped[str] = mapped_column(Text, default="[]")
    audio_path: Mapped[str] = mapped_column(String(400), default="")
    duration_sec: Mapped[int] = mapped_column(Integer, default=0)
    note_scaffold: Mapped[str] = mapped_column(Text, default="")
    glossary_json: Mapped[str] = mapped_column(Text, default="[]")
    content_json: Mapped[str] = mapped_column(Text, default="{}")
    instructions: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    questions: Mapped[list["Question"]] = relationship(back_populates="test", order_by="Question.order")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="test")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    test_id: Mapped[str] = mapped_column(ForeignKey("tests.id"), index=True)
    order: Mapped[int] = mapped_column(Integer)
    stem: Mapped[str] = mapped_column(Text)
    options_json: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(String(1))
    points: Mapped[int] = mapped_column(Integer, default=1)
    rationale: Mapped[str] = mapped_column(Text, default="")
    qtype: Mapped[str] = mapped_column(String(32), default="detail")

    test: Mapped[Test] = relationship(back_populates="questions")


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    status: Mapped[str] = mapped_column(String(24), default="queued")
    kind: Mapped[str] = mapped_column(String(32))
    topic: Mapped[str] = mapped_column(String(200), default="")
    prompt: Mapped[str] = mapped_column(Text, default="")
    test_id: Mapped[str] = mapped_column(String(36), default="")
    error: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(Text, default="")


class ApiUsage(Base):
    __tablename__ = "api_usage"

    key: Mapped[str] = mapped_column(String(160), primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[int] = mapped_column(Integer, index=True)


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    test_id: Mapped[str] = mapped_column(ForeignKey("tests.id"), index=True)
    mode: Mapped[str] = mapped_column(String(16), default="exam")
    answers_json: Mapped[str] = mapped_column(Text, default="{}")
    notes_text: Mapped[str] = mapped_column(Text, default="")
    score: Mapped[float] = mapped_column(Float, default=0)
    max_score: Mapped[float] = mapped_column(Float, default=0)
    plays_used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    test: Mapped[Test] = relationship(back_populates="attempts")


AKIS_LEVELS = ("A1", "A2", "B1", "B1+")
AKIS_KINDS = ("sorular", "kelime", "bosluk")


class AkisReel(Base):
    """One short-form practice card. Answers stay server-side until submission."""

    __tablename__ = "akis_reels"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=uid)
    kind: Mapped[str] = mapped_column(String(16), default="sorular", index=True)
    level: Mapped[str] = mapped_column(String(8), default="A2", index=True)
    body: Mapped[str] = mapped_column(Text, default="")
    title: Mapped[str] = mapped_column(String(200))
    topic: Mapped[str] = mapped_column(String(120), default="")
    script_json: Mapped[str] = mapped_column(Text, default="[]")
    stem: Mapped[str] = mapped_column(Text, default="")
    options_json: Mapped[str] = mapped_column(Text, default="{}")
    answer: Mapped[str] = mapped_column(String(1), default="A")
    explain_tr: Mapped[str] = mapped_column(Text, default="")
    key_line: Mapped[str] = mapped_column(Text, default="")
    audio_path: Mapped[str] = mapped_column(String(400), default="")
    seconds: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(16), default="seed")
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
