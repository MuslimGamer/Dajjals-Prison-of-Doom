from pyglet.window import key, mouse

# Virtual/common methods used by all tutorial windows
class BaseTutorial:
    def __init__(self):
        self.closed = False
        
    # virtual
    def draw(self):
        pass

    # virtual
    def update(self, key):
        pass

    # process button clicks
    def on_click(self, button, x, y):
        for button in self.window.buttons:
            if x >= button.x and x <= button.x + button.width and y >= button.y and y <= button.y + button.height:
                if button in self.window.button_callbacks:
                    callback = self.window.button_callbacks[button]
                    if callback != None:
                        callback()

    # helper method: keys/mouse we use to signal next/close the tutorial
    # note: spams. If you press space, you probably get 3-4 of these events.
    def check_input_to_advance(self, symbol):
        return symbol == key.SPACE or symbol == key.ENTER or symbol == mouse.LEFT
    