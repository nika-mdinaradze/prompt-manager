import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String

from src.db import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    variables = Column(JSON)
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
