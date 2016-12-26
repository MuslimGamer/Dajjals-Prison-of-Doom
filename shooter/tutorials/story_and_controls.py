import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial

class StoryAndControls(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self):
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("HELLO THERE. This unusually long message is brought to you by that one-eyed red ogre guy.", "dajjal")
        self.closed = False

    def draw(self):
        self.window.draw()

    def update(self, keys_pressed):
        if self.check_input_to_advance(keys_pressed):
           self.window.close()
           self.closed = True