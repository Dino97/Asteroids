import pygame


class InputManager:
    def __init__(self):
        # Dictionary that links keycode to a tuple of keystates (general button state and current frame key state)
        self.keymap = {}

    def poll_events(self):
        # Reset current frame key state to false
        for key in self.keymap:
            self.keymap[key] = [self.keymap[key][0], False]

        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event.type == pygame.KEYDOWN:
                self.keymap[event.key] = [True, True]
            elif event.type == pygame.KEYUP:
                self.keymap[event.key] = [False, False]

    # True for every frame in which user is holding the button
    def get_key(self, keycode):
        if keycode not in self.keymap:
            return False

        return self.keymap[keycode][0]

    # True only in the frame in which user pressed the button
    def get_key_down(self, keycode):
        if keycode not in self.keymap:
            return False

        return self.keymap[keycode][1]
