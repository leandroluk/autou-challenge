import json
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from src.presentation.http.server import pydantic_validation_handler, request_validation_handler


class DummyModel(BaseModel):
    field: int


@pytest.mark.asyncio
async def test_request_validation_handler():
    mock_request = MagicMock(spec=Request)
    errors = [{"loc": ("body", "field"), "msg": "value is not a valid integer"}]
    exc = RequestValidationError(errors)

    response = await request_validation_handler(mock_request, exc)

    assert response.status_code == 400
    content = json.loads(cast(Any, response.body).decode())
    assert content["detail"] == "body -> field: value is not a valid integer"


@pytest.mark.asyncio
async def test_pydantic_validation_handler():
    mock_request = MagicMock(spec=Request)

    exc = None
    try:
        DummyModel(**cast(Any, {"field": "not an int"}))
    except ValidationError as e:
        exc = e

    assert exc is not None
    response = await pydantic_validation_handler(mock_request, exc)

    assert response.status_code == 400
    content = json.loads(cast(Any, response.body).decode())
    assert "field" in content["detail"]
    assert "Input should be a valid integer" in content["detail"]
