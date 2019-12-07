

class Component:
    def __init__(self):
        self.name = __class__.__name__
        self.enabled = True
        self.gameobject = None

    # dt = delta time, time between this and last frame
    def on_update(self, dt):
        pass
