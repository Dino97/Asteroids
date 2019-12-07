from engine.component import Component
from engine.components.transform import Transform


class GameObject:
    def __init__(self):
        self.components = {"Transform": Transform()}
        self.transform = self.components["Transform"]

    def add_component(self, component):
        assert issubclass(component.__class__, Component)
        self.components[component.__class__.__name__] = component
        component.gameobject = self

    def get_component(self, component_name):
        if component_name in self.components:
            return self.components[component_name]

        return None

    def remove_component(self, component_name):
        if component_name in self.components:
            self.components[component_name] = None
