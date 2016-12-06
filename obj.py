import copy
import json
import pyglet

# Prototypes of enemies, the player, bullets, and misc stuff (splash screens, explosions, etc.)
obj_enemy=[]	#Lists of object prototypes
obj_player=[]	#The one and only player prototype
obj_bullet=[]
obj_misc=[]

obj_type={				#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'Player': obj_player,			#Object type Player.	(Future potential for multiple player types or upgrades?)
    'Bullet': obj_bullet,			#Object type Bullet.	(Future potential for various projectiles?)
    'Misc': obj_misc}			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)


class game_object:
    def __init__ (self, data):	#on object creation (Loading), object details loaded.
        #print(data['ID'])
        self.id = data['ID']					#Todo: Check list on generation of conflicting IDs and throw error.
        self.health = data['Health']				#Hits to remove || frames until timeout
        self.img = pyglet.image.load(data['Img'])		#Load image for object, Todo: Construct list of images, check/skip if image already loaded by previous object.
        self.x = 0						#Current Positions
        self.y = 0
        self.mx = 0						#Current Movement
        self.my = 0		
        self.sprite = pyglet.sprite.Sprite(self.img,self.x,self.y)
        #print(data['Size'])
        #self.sprite.scale = data['Size']
        #self.sprite.width = data['Size'][1]
        self.ai = data['Behavior']				#AI reference	- See ai.py
        #print(data['Behavior'])

def load_prototype_data():
    obfile = open('data/object.json','r')
    obj = json.load(obfile)
    obj_type["Enemy"] = obj["Enemies"]
    obj_type["Player"] = obj["Player"]
    obj_type["Bullet"] = obj["Bullets"]
    obj_type["Misc"] = obj["Misc"]

def spawn(obj_list, obj_proto, id, x, y):	#References object from object list, copies object-prototype into active objects lists.
    list_of_prototypes = obj_type[obj_proto]
    prototype = next((x for x in list_of_prototypes if x['ID'] == id), None)
    #spawned = copy.copy(obj_type[obj_proto])		#Make copy of object from prototype lists
    spawned = game_object(prototype)
    spawned.x = x					#Set gameworld co-ord specifed
    spawned.y = y
    spawned.sprite.set_position(x,y)
    obj_list.append(spawned)				#Append object to active lists so it is processed and rendered in game.
    return spawned
