from typing import Callable, Any

class Container:
    def __init__(self):
        self._providers: dict[str, tuple[Callable[[], Any]], bool] = {}
        self._singleton: dict[str, Any] = {}
        self._factories: dict[str, Callable[..., Any]] = {}

    def register(self, name: Any, provider: Callable[[], Any], is_singleton: bool = False) -> None:
        self._providers[name.__name__] = (provider, is_singleton)

    def register_factory(self, name: Any, factory: Callable[..., Any]) -> None:
        self._factories[name.__name__] = factory

    def resolve(self, name:Any) -> Any:
        if name.__name__ in self._singleton:
            return self._singleton[name.__name__]

        if name.__name__ not in self._providers:
            raise ValueError(f'No provider registered for {name.__name__}')

        provider, is_singleton = self._providers[name.__name__]
        instance = provider()

        if is_singleton:
            self._singleton[name.__name__] = instance

        return instance

    def resolve_factory(self, name:Any, *args, **kwargs) -> Any:
        if name.__name__ not in self._factories:
            raise ValueError(f'No provider registered for {name.__name__}')

        factory = self._factories[name.__name__]

        return factory(*args, **kwargs)