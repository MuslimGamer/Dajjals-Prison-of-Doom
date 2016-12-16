def ask_and_process_cheat_code(player):
    cheat_code = input("Code: ")
    
    if len(cheat_code) > 0:
        cheat_code = cheat_code.lower()
        if cheat_code in cheats:
            cheats[cheat_code](player)

def invincible(player):
    player.health = 999

cheats = {
    "roketfiq": invincible
}