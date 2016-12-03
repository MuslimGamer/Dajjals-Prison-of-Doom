	#Standard behavior, rush player, attack location
def agro_ai():

    pass

	#Coward behavior, maintain distance, attack location
def coward_ai():
    pass

	#Tank behavoir, Slower agro.
def slow_ai():
    pass

	#Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
def misc_ai():
    obj.health=obj.health -1

	#No AI attached to this object
def NULL_ai():
    pass

	#Undefined behavior referenced.
def error_ai():
    print('Error: AI has gone rouge\n')


def init_ai():
    ai_action={
        "agro": agro_ai,
        "coward": coward_ai,
        "slow": slow_ai,
        "NULL": NULL_ai}

def ai_update():
    pass

