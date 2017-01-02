import pyglet
import shooter.obj
import shooter.ui_manager

class SpeechWindow:

    PADDING = 16
    BUTTON_PADDING = 16

    def __init__(self):
        self.window = pyglet.sprite.Sprite(pyglet.image.load("images/text-window.png"), 0, 0)
        self.window.x = (shooter.obj.GAME_WIDTH - self.window.width) / 2
        self.window.y = (shooter.obj.GAME_HEIGHT - self.window.height) / 2
        self.closed = False
        self.buttons = []
        self.button_callbacks = {} # button => callback

        self.text_label = pyglet.text.Label("", font_name = shooter.ui_manager.UiManager.FONT_NAME, 
            y = self.window.y + self.window.height - 2 * SpeechWindow.PADDING, multiline = True,            
            # dummy width. Anything <= 0 fails. We set this when we show text, because that's when we
            # know the avatar size (and thus, the amount of space left).
            width = 1)

    # TODO: on click, advance to next text
    def show(self, text, avatar):
        self.avatar = pyglet.sprite.Sprite(pyglet.image.load("images/avatars/{0}.png".format(avatar)))
        self.avatar.x = self.window.x + SpeechWindow.PADDING
        self.avatar.y = self.window.y + self.window.height - self.avatar.height - SpeechWindow.PADDING

        self.text_label.x = self.avatar.x + self.avatar.width + SpeechWindow.PADDING
        # Should be 2x padding for a close fit. Too close, since the window has a border (it looks like
        # the text bleeds into it). Let's make it 3x padding so it fits comfortably (we have small texts).
        self.text_label.width = self.window.width - self.avatar.width - 3 * SpeechWindow.PADDING
        self.text_label.text = "{0}: {1}".format(avatar.capitalize(), text)

    def draw(self):
        if not self.closed:
            self.window.draw()
            # Did you set an avatar yet?
            if (self.avatar != None):
                self.avatar.draw()

            self.text_label.draw()

            for button in self.buttons:
                button.draw()

    def close(self):
        self.closed = True

    def add_button(self, image, callback):
        button = pyglet.sprite.Sprite(pyglet.image.load(image))        
        button.y = self.window.y + SpeechWindow.PADDING
        
        x = self.window.x + SpeechWindow.PADDING
        if self.avatar != None:
            x += self.avatar.width + SpeechWindow.PADDING

        if len(self.buttons) > 0:
            previous_button = self.buttons[-1]
            x = previous_button.x + previous_button.width + SpeechWindow.BUTTON_PADDING

        button.x = x

        self.buttons.append(button)
        self.button_callbacks[button] = callback     
        