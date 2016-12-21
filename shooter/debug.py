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

def spawn_pickup(player):
    types = ["Weapon_Pistol", "Weapon_Machine", "Weapon_Shotgun", "Weapon_Rocket"]
    spawn = random.randrange(len(types))
    if len(obj.Enemy_list) > 0:
        obj.Enemy_list[0].Loot(100) # turn the first enemy into kibble
    else:
        player.Loot(100)

def invincible(player):
    player.health = 999

def spawn_enemies(player):
    x = 3 + random.randrange(3)
    for i in range(x):
        obj.Object_handler().spawn_random(5)

def lots_of_bullets(player):
    player.unlimited_ammo()

def die(player):
    player.health = 0

cheats = {
    "roketfiq": invincible,
    "spawn": spawn_enemies,
    "ammo": lots_of_bullets,
    "pickup": spawn_pickup,
    "die": die
}