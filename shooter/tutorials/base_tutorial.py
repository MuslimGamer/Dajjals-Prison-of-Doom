from pyglet.window import key, mouse

# Virtual/common methods used by all tutorial windows
class BaseTutorial:
    # virtual
    def draw(self):
        pass

    # virtual
    def update(self, key):
        pass

    # helper method: keys/mouse we use to signal next/close the tutorial
    # note: spams. If you press space, you probably get 3-4 of these events.
    def check_input_to_advance(self, symbol):
        return symbol == key.SPACE or symbol == key.ENTER
    