import unittest

from src.feature.container import Container

class DummyService:
    def __init__(self):
        self.value = 42

class AnotherService:
    def __init__(self, dep):
        self.dep = dep

class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = Container()

    def test_register_and_resolve(self):
        self.container.register(DummyService, DummyService)
        instance = self.container.resolve(DummyService)
        self.assertIsInstance(instance, DummyService)
        self.assertEqual(instance.value, 42)

    def test_singleton(self):
        self.container.register(DummyService, DummyService, is_singleton=True)
        instance1 = self.container.resolve(DummyService)
        instance2 = self.container.resolve(DummyService)
        self.assertIs(instance1, instance2)

    def test_resolve_unregistered(self):
        with self.assertRaises(ValueError):
            self.container.resolve(AnotherService)

    def test_register_factory_and_resolve(self):
        def factory(dep):
            return AnotherService(dep)
        self.container.register(DummyService, DummyService)
        self.container.register_factory(AnotherService, factory)
        # Simulate manual dependency resolution
        dep_instance = self.container.resolve(DummyService)
        result = self.container.resolve_factory(AnotherService, dep_instance)
        self.assertIsInstance(result, AnotherService)
        self.assertIsInstance(result.dep, DummyService)

    def test_resolve_factory_unregistered(self):
        with self.assertRaises(ValueError):
            self.container.resolve_factory(AnotherService)

    def test_overwrite_provider(self):
        self.container.register(DummyService, DummyService)
        self.container.register(DummyService, lambda: DummyService())
        instance = self.container.resolve(DummyService)
        self.assertIsInstance(instance, DummyService)

if __name__ == "__main__":
    unittest.main()
