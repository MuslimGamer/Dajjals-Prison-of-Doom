from shooter import sound
import shooter.obj


def init(bullet):

    pass

def update(bullet):
    if not bullet.is_on_screen:
        bullet.health = 0
    pass

def on_death(bullet):
    if (bullet.x > 0 and bullet.x < shooter.obj.GAME_WIDTH and bullet.y > 0 and bullet.y < shooter.obj.GAME_HEIGHT):
        bullet.handle.spawn('Misc',"Hit",bullet.x,bullet.y)
        sound.enemy_hit.play()


