import pyglet
from shooter import obj

###
# A manager to draw just UI concerns, like points, lives, etc.
# Game Over should probably go in here too. Probably.
###
class UiManager:
    SPACE_BETWEEN_LINES = 24
    FONT_NAME = "Orbitron"
    RIGHT_PADDING = 120

    def __init__(self):
        self.health_label = pyglet.text.Label('Health: ?', font_name = UiManager.FONT_NAME,
            x = obj.GAME_WIDTH - UiManager.RIGHT_PADDING, y = obj.GAME_HEIGHT - UiManager.SPACE_BETWEEN_LINES)

        self.ammo_label = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.health_label.x, y = self.health_label.y - UiManager.SPACE_BETWEEN_LINES)

    def draw(self, player):
        self.health_label.text = "Health: {0}".format(player.health)
        self.health_label.draw()

        if player.is_reloading():
            self.ammo_label.text = "Reloading!"
        else:
            self.ammo_label.text = "{0} bullets".format(player.shots_left)
        self.ammo_label.draw()

pyglet.font.add_file('fonts/Orbitron-Bold.ttf')
pyglet.font.load(UiManager.FONT_NAME, bold=True)
