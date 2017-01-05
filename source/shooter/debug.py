import random

import shooter.obj
import shooter.config

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
    if len(shooter.obj.Enemy_list) > 0:
        shooter.obj.Enemy_list[0].Loot(100) # turn the first enemy into kibble
    else:
        player.Loot(100)

def spawn_enemies(player):
    x = 3 + random.randrange(3)
    for i in range(x):
        shooter.obj.Object_handler.instance.spawn_random(5)

def spawn_npcs(player):
    # Spawn in a RANGExRANGE area around the player
    RANGE = 100
    
    for i in range(5 + random.randrange(5)):
        x = player.x - RANGE/2 + random.randrange(RANGE)
        y = player.y - RANGE/2 + random.randrange(RANGE)    
        shooter.obj.Object_handler.instance.spawn("Player", "NPC_Basic", x, y)

def die(player):
    player.health = 0

def nearly_win(player):
    player.crew = shooter.config.get("max_crew")
    player.drive = 100 * 100

cheats = {
    "spawn": spawn_enemies,
    "ammo": lambda p: p.unlimited_ammo,
    "pickup": spawn_pickup,
    "die": die,
    "rail": lambda p: p.switch("rail"),
    "players": lambda p: print("P={1} and players: {0}".format(shooter.obj.Player_list, p)),
    "rescue": spawn_npcs,
    "win": nearly_win
}