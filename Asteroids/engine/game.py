from engine.scene import Scene
from engine.gameobject import GameObject


class Game:
    loadedscene: Scene

    def __init__(self):
        self.loadedscene = Scene()

    def start(self):
        # main update loop
        while True:
            for gameobject in self.loadedscene.gameobjects:
                for component in gameobject.components:
                    component.update(0.0016)

    def load_scene(self, scene):
        self.loadedscene = scene

