

class GameObject:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        print("adding component: ", component)
        self.components[component.name] = component

    def get_component(self, component_name):
        print("getting component: ", component_name)
        return self.components[component_name]

    def remove_component(self, component_name):
        print("removing component: ", component_name)
        self.components[component_name] = None
