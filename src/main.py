from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas
from src.db import get_db

app = FastAPI(
    title="prompt management API", description="Technical Assignment", version="0.0.0"
)


@app.post("/prompts/", response_model=schemas.PromptView)
async def create_prompt(prompt: schemas.PromptCreate, db: AsyncSession = Depends(get_db)):
    db_prompt = models.Prompt(**dict(prompt))
    db.add(db_prompt)
    await db.commit()
    await db.refresh(db_prompt)
    return db_prompt


@app.get("/prompts/", response_model=list[schemas.PromptView])
async def prompts_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Prompt))
    prompts = result.scalars().all()
    return prompts
