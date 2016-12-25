from shooter import sound

def init(bullet):
    pass

def update(bullet):
    if not bullet.is_on_screen:
        bullet.health = 0
    pass

def on_death(bullet):
    if bullet.is_on_screen:
        bullet.handle.spawn('Misc',"Hit",bullet.x,bullet.y)
        sound.enemy_hit.play()
    pass


