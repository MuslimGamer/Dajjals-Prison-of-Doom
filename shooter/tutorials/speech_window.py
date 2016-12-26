import pyglet
import shooter.obj
import shooter.ui_manager

class SpeechWindow:

    PADDING = 16

    def __init__(self):
        self.window = pyglet.sprite.Sprite(pyglet.image.load("images/text-window.png"), 0, 0)
        self.window.x = (shooter.obj.GAME_WIDTH - self.window.width) / 2
        self.window.y = (shooter.obj.GAME_HEIGHT - self.window.height) / 2

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
        print("{0} - {1} - {2}".format(self.window.width, self.avatar.width, 2 * SpeechWindow.PADDING))
        self.text_label.width = self.window.width - self.avatar.width - 2 * SpeechWindow.PADDING
        self.text_label.text = "{0}: {1}".format(avatar.capitalize(), text)

    def draw(self):
        self.window.draw()
        # Did you set an avatar yet?
        if (self.avatar != None):
            self.avatar.draw()

        self.text_label.draw()