import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import models


@pytest.mark.asyncio
async def test_create_prompt(client: AsyncClient, prompt_payload):
    response = await client.post("/prompts/", json=prompt_payload)
    assert response.status_code == 200
    created_prompt = response.json()
    assert created_prompt.get("text") == prompt_payload.get("text")
    assert created_prompt.get("variables") == prompt_payload.get("variables")
    assert created_prompt.get("created_by") == prompt_payload.get("created_by")
    assert isinstance(created_prompt.get("id"), int)
    assert isinstance(created_prompt.get("created_at"), str)


@pytest.mark.asyncio
async def test_create_prompt_empty_text(client: AsyncClient, prompt_payload):
    prompt_payload["text"] = ""
    response = await client.post("/prompts/", json=prompt_payload)
    assert response.status_code == 422
    assert (
        response.json().get("detail")[0].get("message")
        == "String should have at least 1 character"
    )


@pytest.mark.asyncio
async def test_create_prompt_empty_created_by(client: AsyncClient, prompt_payload):
    prompt_payload["created_by"] = ""
    response = await client.post("/prompts/", json=prompt_payload)
    assert response.status_code == 422
    assert (
        response.json().get("detail")[0].get("message")
        == "String should have at least 1 character"
    )


@pytest.mark.asyncio
async def test_prompts_list(
    client: AsyncClient, db_session: AsyncSession, prompt_payload
):
    prompt = models.Prompt(**prompt_payload)
    db_session.add(prompt)
    await db_session.commit()
    await db_session.refresh(prompt)
    response = await client.get("/prompts/")
    assert response.status_code == 200
    prompts = response.json()
    assert isinstance(prompts, list)
    assert len(prompts) == 1
    assert prompts[0].get("text") == prompt.text
    assert prompts[0].get("variables") == prompt.variables
    assert prompts[0].get("created_by") == prompt.created_by
    assert isinstance(prompts[0].get("id"), int)
    assert isinstance(prompts[0].get("created_at"), str)


@pytest.mark.asyncio
async def test_prompts_list_empty(
    client: AsyncClient, db_session: AsyncSession, prompt_payload
):
    response = await client.get("/prompts/")
    assert response.status_code == 200
    prompts = response.json()
    assert prompts == []
