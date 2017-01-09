import pyglet
from pyglet.window import mouse

import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial
import shooter.tutorials.tutorial_manager
import shooter.config

class StoryAndControls(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self):
        self.showing = "1"
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("More Muslim meat for my armies! I'll chase you to the ends of the galaxy!", "dajjal")

        self.window.add_button('images/next-button.png', lambda: self.update(mouse.LEFT)) # advance
        self.window.add_button('images/skip-button.png', lambda: self.close())
        self.closed = False

    def draw(self):
        self.window.draw()

    def update(self, key):
        if self.check_input_to_advance(key):
            if self.showing == "1":
                self.showing = "2"
                max_pods = shooter.config.get("max_crew")
                self.window.show("Looks like the jump drive is offline. I'll need to rescue {0} grey escape pods so we can repair the ship so we can jump to safety.".format(max_pods), "captain")
            elif self.showing == "2":
                self.showing = "3"
                self.window.show("Use WASD to operate the thrusters, and the mouse to aim and shoot. R reloads the guns.", "captain")
            elif self.showing == "3":
                self.showing = "4"
                self.window.show("Here come the Dajjal's minions!", "captain")                
            else:
               self.close()

    def close(self):
        self.window.close()
        self.closed = True
        # Tutorial Manager: we're closed!
        shooter.tutorials.tutorial_manager.on_keypress(None, [])