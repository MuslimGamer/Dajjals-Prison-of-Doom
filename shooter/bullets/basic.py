from shooter import sound
from shooter import obj


def init(bullet):

    pass

def update(bullet):
    if not bullet.is_on_screen:
        bullet.health = 0
    pass

def on_death(bullet):
    print (str(bullet.x), str(bullet.y))
    if (bullet.x > 0 and bullet.x < obj.GAME_WIDTH and bullet.y > 0 and bullet.y < obj.GAME_HEIGHT):
        bullet.handle.spawn('Misc',"Hit",bullet.x,bullet.y)
        sound.enemy_hit.play()


