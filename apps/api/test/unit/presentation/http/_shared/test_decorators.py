import pytest
from fastapi import HTTPException
from src.presentation.http._shared.decorators import map_domain_error


class DomainError(Exception):
    pass


class UnexpectedError(Exception):
    pass


@pytest.mark.asyncio
async def test_map_domain_error_success():
    @map_domain_error((DomainError, 400))
    async def fn() -> str:
        return "ok"

    assert await fn() == "ok"


@pytest.mark.asyncio
async def test_map_domain_error_mapped_exception():
    @map_domain_error((DomainError, 404))
    async def fn():
        raise DomainError("resource not found")

    with pytest.raises(HTTPException) as exc:
        await fn()

    assert exc.value.status_code == 404
    assert exc.value.detail == "resource not found"


@pytest.mark.asyncio
async def test_map_domain_error_unmapped_exception_reraises():
    @map_domain_error((DomainError, 400))
    async def fn():
        raise UnexpectedError("unmapped")

    with pytest.raises(UnexpectedError, match="unmapped"):
        await fn()


@pytest.mark.asyncio
async def test_map_domain_error_multiple_positional_mappings():
    @map_domain_error((DomainError, 404), (ValueError, 400))
    async def fn(ex: type[Exception]):
        raise ex("fail")

    with pytest.raises(HTTPException) as exc1:
        await fn(DomainError)
    assert exc1.value.status_code == 404

    with pytest.raises(HTTPException) as exc2:
        await fn(ValueError)
    assert exc2.value.status_code == 400


@pytest.mark.asyncio
async def test_map_domain_error_dict_mapping():
    @map_domain_error({DomainError: 409})
    async def fn():
        raise DomainError("conflict")

    with pytest.raises(HTTPException) as exc:
        await fn()
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_map_domain_error_list_mapping():
    @map_domain_error([(DomainError, 422), (ValueError, 400)])
    async def fn(ex: type[Exception]):
        raise ex("list test")

    with pytest.raises(HTTPException) as exc1:
        await fn(DomainError)
    assert exc1.value.status_code == 422

    with pytest.raises(HTTPException) as exc2:
        await fn(ValueError)
    assert exc2.value.status_code == 400
