from shooter import obj

def ask_and_process_cheat_code(player):
    cheat_code = input("Code: ")
    
    if len(cheat_code) > 0:
        cheat_code = cheat_code.lower()
        if cheat_code in cheats:
            cheats[cheat_code](player)

def invincible(player):
    player.health = 999

def spawn_enemy(player):
    which_one = input("Which enemy (eg. basic): ").lower().capitalize()
    which_one = "Enemy_{0}".format(which_one)
    obj.Object_handler().spawn_enemy(which_one, 1024, 576)

cheats = {
    "roketfiq": invincible,
    "spawn": spawn_enemy,
    "ammo": lots_of_bullets
}