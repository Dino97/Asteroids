from engine.component import Component


class Transform(Component):
    def __init__(self, x=0, y=0, z=0):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
