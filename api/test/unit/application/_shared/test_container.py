import pytest

from src.application._shared.container import _registry, clear, injectable, register, resolve


@pytest.fixture(autouse=True)
def reset_registry():
    clear()


class DummyDep:
    pass


class DummyClass:
    def __init__(self, dep: DummyDep):
        self.dep = dep


def test_injectable_decorator_direct():
    @injectable
    class A:
        pass

    assert _registry[A] == A


def test_injectable_decorator_as_type():
    class Base:
        pass

    @injectable(as_type=Base)
    class Impl(Base):
        pass

    assert _registry[Base] == Impl


def test_register_and_resolve():
    register(DummyDep, DummyDep)

    instance1 = resolve(DummyDep)
    instance2 = resolve(DummyDep)

    assert isinstance(instance1, DummyDep)
    assert instance1 is instance2


def test_register_invalidates_existing_instance_cache():
    instance_a = resolve(DummyDep)
    register(DummyDep, DummyDep)
    instance_b = resolve(DummyDep)

    assert instance_a is not instance_b


def test_resolve_instantiates_with_dependencies():
    @injectable(as_type=DummyDep)
    class Dep(DummyDep):
        pass

    @injectable
    class MyClass(DummyClass):
        pass

    instance = resolve(MyClass)
    assert isinstance(instance, MyClass)
    assert isinstance(instance.dep, Dep)


def test_resolve_unregistered_class():
    instance = resolve(DummyClass)
    assert isinstance(instance, DummyClass)
    assert isinstance(instance.dep, DummyDep)


def test_clear():
    register(DummyDep, DummyDep)
    assert _registry[DummyDep] == DummyDep
    clear()
    assert _registry == {}
