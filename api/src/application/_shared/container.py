from collections.abc import Callable
from typing import Any, get_type_hints, overload

_registry: dict[type, type] = {}
_instances: dict[type, Any] = {}


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


def register(key: type, impl: type) -> None:
    _registry[key] = impl
    if key in _instances:
        del _instances[key]


def resolve[T](t: type[T]) -> T:
    if t in _instances:
        return _instances[t]

    impl = _registry.get(t, t)

    initializer = impl.__init__
    hints = {
        name: hint
        for name, hint in get_type_hints(initializer).items()
        if name != "self" and isinstance(hint, type) and hint is not Any
    }

    deps = {name: resolve(hint) for name, hint in hints.items()}
    instance = impl(**deps)

    _instances[t] = instance
    return instance


def clear() -> None:
    _registry.clear()
    _instances.clear()
