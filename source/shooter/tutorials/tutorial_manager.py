from enum import Enum
from shooter.tutorials.story_and_controls import StoryAndControls
from shooter.tutorials.you_win import YouWin
import shooter.obj

# Enum with two values
Tutorials = Enum("Tutorials", "Story_and_Controls You_Win")

# UI class that handles rendering context-sensitive tutorial stuff.
# eg. renders the story and intro in the first game of the session.
# Renders hints when the first rescuable NPC shows up in the first session.

is_first_game = True
is_showing_tutorial = False

_current_tutorial = None
tutorials_shown = []

# key: keyboard key or mouse button integer (eg. mouse.LEFT = 1)
def on_keypress(key, previously_pressed):
    global is_first_game, is_showing_tutorial, tutorials_shown, _current_tutorial

    if is_first_game and not Tutorials.Story_and_Controls in tutorials_shown:
        tutorials_shown.append(Tutorials.Story_and_Controls)
        is_showing_tutorial = True
        _current_tutorial = StoryAndControls()

    if _current_tutorial != None:
        _current_tutorial.update(key)
        
        if _current_tutorial.closed:
            _current_tutorial = None
            is_showing_tutorial = False

# Called every draw. Draw stuff specific to the current tutorial.
def draw():
    global _current_tutorial
    
    player = None
    if len(shooter.obj.Player_list) > 0:
        player = shooter.obj.Player_list[0]

    if _current_tutorial != None:
        _current_tutorial.draw()
    # Has to be here to trigger even if the user doesn't press anything
    # No tutorial, and victory conditions? Incite victory.
    elif Tutorials.You_Win not in tutorials_shown and player != None and player.has_won:
        _current_tutorial = YouWin(player)
