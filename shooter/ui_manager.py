import pyglet
import shooter.obj
from shooter import config

###
# A manager to draw just UI concerns, like points, lives, etc.
# Game Over should probably go in here too. Probably.
###

class UiManager:
    SPACE_BETWEEN_LINES = 24
    RIGHT_PADDING = 130
    LEFT_PADDING = 20
    
    FONT_NAME = "Orbitron"
    FONT_FILE = "fonts/Orbitron-Medium.ttf"

    

    def __init__(self):

        self.AlertTimeout = 0
        self.health_label = pyglet.text.Label('Health: ?', font_name = UiManager.FONT_NAME,
            x = shooter.obj.GAME_WIDTH - UiManager.RIGHT_PADDING, y = shooter.obj.GAME_HEIGHT - UiManager.SPACE_BETWEEN_LINES)

        self.ammo_label = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.health_label.x, y = self.health_label.y - UiManager.SPACE_BETWEEN_LINES)

        self.score_label = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.health_label.x, y = self.ammo_label.y - UiManager.SPACE_BETWEEN_LINES)

        self.drive_label = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = UiManager.LEFT_PADDING, y = shooter.obj.GAME_HEIGHT - UiManager.SPACE_BETWEEN_LINES)

        self.crew_label = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.drive_label.x, y = self.drive_label.y - UiManager.SPACE_BETWEEN_LINES)

        self.alert_label = pyglet.text.Label("",font_name = UiManager.FONT_NAME,x = 0,y=0, color=(0, 0, 0, 0), align='center')
 
        if not (config.get('debugging')): return

        self.debug1 = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.drive_label.x, y = UiManager.SPACE_BETWEEN_LINES)
        self.debug2 = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.drive_label.x, y = self.debug1.y + UiManager.SPACE_BETWEEN_LINES)
        self.debug3 = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.drive_label.x, y = self.debug2.y + UiManager.SPACE_BETWEEN_LINES)

        self.debug4 = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.health_label.x-300, y = self.debug1.y)
        self.debug5 = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.health_label.x-300, y = self.debug2.y)
        self.debug6 = pyglet.text.Label("", font_name = UiManager.FONT_NAME,
            x = self.health_label.x-300, y = self.debug3.y)

    def alert(self,x,y,message, colour, timeout):
 
        Colour = {
            'Red': (255,0,0,255),
            'Green': (0,255,0,255),
            'Blue': (0,0,255,255),
            'White': (255,255,255,255)
        }

        self.alert_label.x = x
        self.alert_label.y = y
        self.alert_label.color=Colour[colour]
        self.alert_label.text = message
        self.AlertTimeout = timeout

    def draw(self, player):

        if self.AlertTimeout:
            self.alert_label.draw()
            AlertTimeout -=1
        
        self.health_label.text = "Health: {0}".format(int(player.health))
        self.health_label.draw()

        self.score_label.text = "Score: {0}".format(shooter.obj.score)
        self.score_label.draw()

        if player.is_reloading():
            self.ammo_label.text = "Reloading!"
        else:
            self.ammo_label.text = "{0} bullets".format(player.shots_left)
        self.ammo_label.draw()

        self.crew_label.text = "Crew: {0} / {1}".format(player.crew, config.get("max_crew"))
        self.crew_label.draw()

        if player.drive == 0:
            self.drive_label.text = "Jump Drive Disabled"
        else:
            self.drive_label.text = "Jump Drive Charging: {0}%".format(player.drive / 100)
        self.drive_label.draw()

        if not (config.get('debugging')): return

        self.debug3.text = "#NPC: {0}".format(len(shooter.obj.Player_list)-1)
        self.debug3.draw()
        self.debug2.text = "#Enemy: {0}".format(len(shooter.obj.Enemy_list))
        self.debug2.draw()
        self.debug1.text = "#Bullets: {0}".format(len(shooter.obj.Bullet_list))
        self.debug1.draw()


        self.debug6.text = "Spawn Income: {0}".format(player.handle.SpawnIncome)
        self.debug6.draw()
        self.debug5.text = "Spawn Budget: {0}".format(player.handle.SpawnBudget)
        self.debug5.draw()
        self.debug4.text = "Spawn Cost: {0}".format(player.handle.SpawnCost)
        self.debug4.draw()

pyglet.font.add_file(UiManager.FONT_FILE)
pyglet.font.load(UiManager.FONT_NAME, bold=False)
