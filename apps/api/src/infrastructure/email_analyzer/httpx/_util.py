import json
import re

from src.domain.email.enums import CategoryEnum


def parse_raw_response(raw: str) -> tuple[CategoryEnum, str]:
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
        return (CategoryEnum(data["category"]), data["reply"])
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise Exception(f"Unexpected model output: {e}") from e
