import pyglet
from pyglet.window import key
from shooter import obj


from math import atan2,sin,cos, degrees, pi

class input_handler:
    def __init__(self,window):
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_button = 0
        self.keyboard = pyglet.window.key.KeyStateHandler()
        window.push_handlers(self.keyboard)

    def mouse_update(self,x,y,button):
        self.mouse_x = x
        self.mouse_y = y
        self.mouse_button = button




def input(main_list, input_handle): 
    for player in main_list[0]:
        player.mx = input_handle.keyboard[key.A]*-1 + input_handle.keyboard[key.D]*1
        player.my = input_handle.keyboard[key.S]*-1 + input_handle.keyboard[key.W]*1
        if not (abs(player.mx) + abs(player.my) == 1):
            player.mx = player.mx * 0.707
            player.my = player.my * 0.707

        if not (player.cooldown):
            if (input_handle.mouse_button == 1):
                b1 = obj.spawn('Bullet','Melee',player.x,player.y)  #Short range attack. Todo: Short cooldown
                player.cooldown = 10   #Todo: Add attribute to object
            elif (input_handle.mouse_button == 4):
                b1 = obj.spawn('Bullet','Basic',player.x,player.y)  #Long range attack. Todo: Long cooldown
                player.cooldown = 50   #Todo: Add attribute to object
            else:
                return
        else:
            return
        input_handle.mouse_button = 0  #Bug Experienced - Button state sticks, Stopgap fix: Clear button after processing once. 
        dx = input_handle.mouse_x-b1.x
        dy = input_handle.mouse_y-b1.y
        theta = atan2(dx,dy)
        b1.mx = 10*sin(theta)
        b1.my = 10*cos(theta)
        main_list[2].append(b1)
    pass


    pass

def collision(obj_check):
    pass

def update(obj_list):
    for obj in obj_list:
        obj.x = obj.x + obj.mx
        obj.y = obj.y + obj.my
        obj.sprite.set_position(obj.x,obj.y)

        if obj.cooldown:
            obj.cooldown = obj.cooldown -1
        
        print(obj.id)
        print(obj.ai)
        print(obj.health)


        if obj.health <= 0:
            obj_list.remove(obj)

        # Call your update method, if you have one
        if hasattr(object, "update") and callable(getattr(obj, "update")):
            obj.update()
    pass
        


#Standard behavior, rush player, attack location
def agro_ai(obj):
    obj.mx = 1
    if (obj.x > 300):
        obj.health = 0
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
    obj.health = obj.health - 1

#No AI attached to this object
def NULL_ai(obj):
    pass

#Undefined behavior referenced.
def error_ai(obj):
    raise(Exception('Error: AI has gone rouge'))


def ai(obj_list):			#Generic AI handler
    for obj in obj_list:
        ai_action[obj.ai](obj)		#Reference dictionary against object AI variable, Vector to specific function for AI type.

ai_action={
    "agro": agro_ai,
    "coward": coward_ai,
    "slow": slow_ai,
    "NULL": NULL_ai,
    "misc": misc_ai}
