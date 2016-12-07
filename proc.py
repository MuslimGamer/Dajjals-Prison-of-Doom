import pyglet

def input(obj_list):
    pass

def collision(obj_check):
    pass

def update(obj_list):
    for obj in obj_list:
        obj.x = obj.x + obj.mx
        obj.y = obj.y + obj.my
        obj.sprite.set_position(obj.x,obj.y)
        if (obj.health == 0):
            obj_list.remove(obj)
            print('Killing object: '+obj.id)
    pass
        


	#Standard behavior, rush player, attack location
def agro_ai(obj):
    obj.mx = 1
    if (obj.x > 300):
        obj.health = 0
        print('Time to close')
    pass

	#Coward behavior, maintain distance, attack location
def coward_ai(obj):
    obj.my = 1
    pass

	#Tank behavoir, Slower agro.
def slow_ai(obj):
    pass

	#Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
def misc_ai(obj):
    obj.health=obj.health -1

	#No AI attached to this object
def NULL_ai(obj):
    pass

	#Undefined behavior referenced.
def error_ai(obj):
    print('Error: AI has gone rouge\n')


def ai(obj_list):			#Generic AI handler
    for obj in obj_list:
        ai_action[obj.ai](obj)		#Reference dictionary against object AI variable, Vector to specific function for AI type.

ai_action={
    "agro": agro_ai,			#Default AI
    "coward": coward_ai,		#Ranged AI
    "slow": slow_ai,			#Tank AI
    "NULL": NULL_ai}			#No AI
