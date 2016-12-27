import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial

class StoryAndControls(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self):
        self.showing = "dajjal"
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("More Muslim meat for my armies! I'll chase you to the ends of the galaxy!", "dajjal")
        self.closed = False

    def draw(self):
        self.window.draw()

    def update(self, key):
        if self.check_input_to_advance(key):
            if self.showing == "dajjal":
                self.showing = "hyperdrive"
                self.window.show("Looks like the hyper-drive is offline. I'll need to rescue crew-members to get it operational again.", "captain")
                self.window.show("Here come the Dajjal's war ships!", "captain")
            else:
               self.window.close()
               self.closed = True