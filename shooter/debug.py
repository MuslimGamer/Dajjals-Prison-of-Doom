import random

from shooter import obj

def process_generically(input):
    pass

def ask_and_process_cheat_code(player):
    cheat_code = input("Code: ")
    
    if len(cheat_code) > 0:
        cheat_code = cheat_code.lower()
        if cheat_code in cheats:
            cheats[cheat_code](player)
            return

    process_generically(cheat_code)

def invincible(player):
    player.health = 999

def spawn_enemies(player):
    x = 3 + random.randrange(3)
    for i in range(x):
        obj.Object_handler().spawn_random(5)

def lots_of_bullets(player):
    player.unlimited_ammo()

cheats = {
    "roketfiq": invincible,
    "spawn": spawn_enemies,
    "ammo": lots_of_bullets
}