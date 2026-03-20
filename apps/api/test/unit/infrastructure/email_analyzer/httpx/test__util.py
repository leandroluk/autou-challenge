import pytest
from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer.httpx._util import parse_raw_response


def test_parse_raw_response_success() -> None:
    raw = '{"category": "Productive", "reply": "a reply"}'
    cat, reply = parse_raw_response(raw)
    assert cat == CategoryEnum.PRODUCTIVE
    assert reply == "a reply"


def test_parse_raw_response_with_markdown() -> None:
    raw = '```json\n{"category": "Unproductive", "reply": "markdown"}\n```'
    cat, reply = parse_raw_response(raw)
    assert cat == CategoryEnum.UNPRODUCTIVE
    assert reply == "markdown"

    raw_no_lang = '```\n{"category": "Unproductive", "reply": "markdown2"}\n```'
    cat, reply = parse_raw_response(raw_no_lang)
    assert cat == CategoryEnum.UNPRODUCTIVE
    assert reply == "markdown2"


def test_parse_raw_response_invalid_json() -> None:
    with pytest.raises(Exception, match="Unexpected model output"):
        parse_raw_response("invalid json")


def test_parse_raw_response_missing_keys() -> None:
    with pytest.raises(Exception, match="Unexpected model output"):
        parse_raw_response('{"reply": "missing category"}')


def test_parse_raw_response_invalid_enum() -> None:
    with pytest.raises(Exception, match="Unexpected model output"):
        parse_raw_response('{"category": "InvalidEnum", "reply": "..."}')
