import copy
import json
import pyglet

# Prototypes of enemies, the player, bullets, and misc stuff (splash screens, explosions, etc.)
obj_enemy=[]	#Lists of object prototypes
obj_player=[]	#The one and only player prototype
obj_bullet=[]
obj_misc=[]

prototypes_json = {				#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'Player': obj_player,			#Object type Player.	(Future potential for multiple player types or upgrades?)
    'Bullet': obj_bullet,			#Object type Bullet.	(Future potential for various projectiles?)
    'Misc': obj_misc			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)
}

class GameObject:
    def __init__ (self, json_data):	#on object creation (Loading), object details loaded.
        #print(data['ID'])
        self.id = json_data['ID']					#Todo: Check list on generation of conflicting IDs and throw error.
        self.health = json_data['Health']				#Hits to remove || frames until timeout
        self.img = pyglet.image.load(json_data['Img'])		#Load image for object, Todo: Construct list of images, check/skip if image already loaded by previous object.
        self.x = 0						#Current Positions
        self.y = 0
        self.mx = 0						#Current Movement
        self.my = 0		
        self.sprite = pyglet.sprite.Sprite(self.img,self.x,self.y)
        #print(data['Size'])
        #self.sprite.scale = data['Size']
        #self.sprite.width = data['Size'][1]
        self.ai = json_data['Behavior']				#AI reference	- See proc.py
        #print(data['Behavior'])

def load_prototype_data():
    with open('data/object.json','r') as f:
        raw_json = json.load(f)
        prototypes_json["Enemy"] = raw_json["Enemies"]
        prototypes_json["Player"] = raw_json["Player"]
        prototypes_json["Bullet"] = raw_json["Bullets"]
        prototypes_json["Misc"] = raw_json["Misc"]

def spawn(object_type, id, x, y):	#References object from object list, copies object-prototype into active objects lists.
    list_of_prototypes = prototypes_json[object_type]
    # Find an object x in the collection that matches the specified ID; defaults to None
    prototype = next((x for x in list_of_prototypes if x['ID'] == id), None)
    spawned = GameObject(prototype)
    spawned.x = x					#Set gameworld co-ord specifed
    spawned.y = y
    spawned.sprite.set_position(x,y)
    return spawned
