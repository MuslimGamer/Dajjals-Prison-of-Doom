from pyglet.window import key, mouse

# Virtual/common methods used by all tutorial windows
class BaseTutorial:
    # virtual
    def draw(self):
        pass

    # virtual
    def update(self, keys_pressed):
        pass

    # helper method: keys/mouse we use to signal next/close the tutorial
    # note: spams. If you press space, you probably get four of these.
    def check_input_to_advance(self, keys_pressed):
        return key.SPACE in keys_pressed or key.ENTER in keys_pressed or mouse.LEFT in keys_pressed
    