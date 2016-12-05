import copy
import json
import pyglet

obj_enemy=[]	#Lists of object prototypes
obj_player=[]		#Lists of objects in play in main.py  - Likely subject to clean up later.
obj_bullet=[]
obj_misc=[]

obj_type={				#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'Player': obj_player,			#Object type Player.	(Future potential for multiple player types or upgrades?)
    'Bullet': obj_bullet,			#Object type Bullet.	(Future potential for various projectiles?)
    'Misc': obj_misc}			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)


class game_object:
    def __init__ (self, data,otype):	#on object creation (Loading), object details loaded.
        #print(data['ID'])
        self.id = data['ID']					#Todo: Check list on generation of conflicting IDs and throw error.
        self.type = otype
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

def init_obj():
    obfile = open('data/object.json','r')
    obj = json.load(obfile)
    for obj_import_type in obj:
        for instance in obj[obj_import_type]:
            import_object = game_object(obj[obj_import_type][instance],obj_import_type)
            obj_type[obj_import_type].append(import_object)


def spawn(obj_list,obj_proto,obj_id,x,y):	#References object from object list, copies object-prototype into active objects lists.
    spawned = copy.copy(obj_type[obj_proto][obj_id])		#Make copy of object from prototype lists
    spawned.x = x					#Set gameworld co-ord specifed
    spawned.y = y
    spawned.sprite.set_position(x,y)
    obj_list.append(spawned)				#Append object to active lists so it is processed and rendered in game.
    return spawned
