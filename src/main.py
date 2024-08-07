from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas
from src.db import get_db

app = FastAPI(
    title="prompt management API", description="Technical Assignment", version="0.0.0"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    detail = [
        {"location": error["loc"], "message": error["msg"]} for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": detail}),
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
