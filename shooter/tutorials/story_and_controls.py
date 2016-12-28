import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial

class StoryAndControls(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self):
        self.showing = "1"
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("More Muslim meat for my armies! I'll chase you to the ends of the galaxy!", "dajjal")
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