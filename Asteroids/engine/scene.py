from engine.gameobject import GameObject


class Scene:
    def __init__(self):
        self.gameobjects = []

    def register_gameobject(self, gameobject):
        # proveri da li je tip argumenta GameObject
        assert issubclass(gameobject.__class__, GameObject)

        self.gameobjects.append(gameobject)