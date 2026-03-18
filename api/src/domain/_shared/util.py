from collections.abc import Callable
from typing import Any, TypedDict, Unpack

from pydantic import AliasChoices, AliasPath, BaseModel, Discriminator, Field
from pydantic.config import JsonDict
from pydantic.fields import Deprecated, FieldInfo
from pydantic_core import PydanticUndefined


class _FieldProxyCallKwargs(TypedDict, total=False):
    default: Any
    default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any]
    alias: str
    alias_priority: int
    validation_alias: str | AliasPath | AliasChoices
    serialization_alias: str
    title: str
    field_title_generator: Callable[[str, FieldInfo], str]
    description: str
    examples: list[Any]
    exclude: bool
    exclude_if: Callable[[Any], bool]
    discriminator: str | Discriminator
    deprecated: Deprecated | str | bool
    json_schema_extra: JsonDict | Callable[[JsonDict], None]
    frozen: bool
    validate_default: bool
    repr: bool
    init: bool
    init_var: bool
    kw_only: bool
    metadata: list[Any]


class _FieldProxy[T: BaseModel]:
    def __init__(self, entity: type[T], field: str):
        self._entity = entity
        self._field_name = field

        if field not in entity.model_fields:
            available = ", ".join(entity.model_fields.keys())
            raise AttributeError(f"Field '{field}' not found in {entity.__name__}. Available fields: {available}")

        self._original = entity.model_fields[field]

    def __call__(self, **kwargs: Unpack[_FieldProxyCallKwargs]) -> Any:
        field_info: FieldInfo = self._original

        base: dict[str, Any] = {
            attr: val
            for attr in _FieldProxyCallKwargs.__annotations__.keys()
            if (val := getattr(field_info, attr, None)) not in (None, PydanticUndefined)
        }

        provided: dict[str, Any] = dict(kwargs)

        if provided.keys() & {"default", "default_factory"}:
            base.pop("default", None)
            base.pop("default_factory", None)

        return Field(**{**base, **provided})


class _EntityFieldSelector[T: BaseModel]:
    def __init__(self, entity: type[T]):
        self._entity = entity

    def __getattr__(self, field: str) -> _FieldProxy[T]:
        return _FieldProxy(self._entity, field)


def FieldOf[T: BaseModel](entity: type[T]) -> _EntityFieldSelector[T]:
    return _EntityFieldSelector(entity)
