import pyglet
from pyglet.window import mouse

import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial

class StoryAndControls(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self):
        self.showing = "1"
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("More Muslim meat for my armies! I'll chase you to the ends of the galaxy!", "dajjal")

        # Click already registers globally, no need to act        
        self.window.add_button('images/next-button.png', None)
        self.window.add_button('images/skip-button.png', None)
        self.closed = False

    def draw(self):
        self.window.draw()

    def update(self, key):
        if self.check_input_to_advance(key):
            if self.showing == "1":
                self.showing = "2"
                self.window.show("Looks like the hyper-drive is offline. I'll need to rescue enough escape pods to repair the ship so we can jump to safety.", "captain")
            elif self.showing == "2":
                self.showing = "3"
                self.window.show("Use WASD to operate the thrusters, and the mouse to aim and shoot. R reloads the guns.", "captain")
            elif self.showing == "3":
                self.showing = "4"
                self.window.show("Here come the Dajjal's war ships!", "captain")                
            else:
               self.window.close()
               self.closed = True

    def on_click(self, button, x, y):
        for button in self.window.buttons:
            if x >= button.x and x <= button.x + button.width and y >= button.y and y <= button.y + button.height:
                print("xlixked {0}, {1}; b goes from {2}, {3} to {4}, {5}".format(x, y, button.x, button.y, button.x + button.width, button.y + button.height))
                callback = self.window.button_callbacks[button]
                if callback != None:
                    callback()