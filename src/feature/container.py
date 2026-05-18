from typing import Callable, Any
from feature_interfaces.enums.settings_enum import FunctionEnum


class Container:
    def __init__(self):
        self._providers: dict[str, tuple[Callable[[], Any]], bool] = {}
        self._singleton: dict[str, Any] = {}
        self._factories: dict[str, Callable[..., Any]] = {}
        self._functions: dict[FunctionEnum, Callable[..., Any]] = {}

    def register(
        self, name: Any, provider: Callable[[], Any], is_singleton: bool = False
    ) -> None:
        self._providers[name.__name__] = (provider, is_singleton)

    def register_factory(self, name: Any, factory: Callable[..., Any]) -> None:
        self._factories[name.__name__] = factory

    def register_function(self, name: FunctionEnum, func: Callable[..., Any]) -> None:
        self._functions[name] = func

    def resolve(self, name: Any) -> Any:
        if name.__name__ in self._singleton:
            return self._singleton[name.__name__]

        if name.__name__ not in self._providers:
            raise ValueError(f"No provider registered for {name.__name__}")

        provider, is_singleton = self._providers[name.__name__]
        instance = provider()

        if is_singleton:
            self._singleton[name.__name__] = instance

        return instance

    def resolve_factory(self, name: Any, *args, **kwargs) -> Any:
        if name.__name__ not in self._factories:
            raise ValueError(f"No provider registered for {name.__name__}")

        factory = self._factories[name.__name__]

        return factory(*args, **kwargs)

    def resolve_function(self, name: FunctionEnum) -> Callable[..., Any]:
        if name.value not in self._functions:
            raise ValueError(f"No function registered for {name.value}")

        func = self._functions[name.value]
        return func
