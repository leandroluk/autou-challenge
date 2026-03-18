from collections.abc import Callable
from typing import Any, get_type_hints, overload

_registry: dict[type, type] = {}


@overload
def injectable[T](cls: type[T], *, as_type: None = None) -> type[T]: ...
@overload
def injectable[T](cls: None = None, *, as_type: type) -> Callable[[type[T]], type[T]]: ...


def injectable(cls: type | None = None, *, as_type: type | None = None) -> type | Callable[[type], type]:
    def decorator(c: type) -> type:
        key = as_type if as_type is not None else c
        _registry[key] = c
        return c

    if cls is not None:
        return decorator(cls)
    return decorator


def resolve[T](t: type[T]) -> T:
    impl = _registry.get(t, t)
    hints = {
        name: hint
        for name, hint in get_type_hints(impl.__init__).items()
        if name != "self" and isinstance(hint, type) and hint is not Any
    }
    deps: dict[str, object] = {name: resolve(hint) for name, hint in hints.items()}
    return impl(**deps)
