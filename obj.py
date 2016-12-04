import copy
import pyglet

obj_enemy=[]	#Lists of object prototypes
obj_player=[]		#Lists of objects in play in main.py  - Likely subject to clean up later.
obj_bullet=[]
obj_misc=[]

obj_type={				#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'player': obj_player,			#Object type Player.	(Future potential for multiple player types or upgrades?)
    'bullet': obj_bullet,			#Object type Bullet.	(Future potential for various projectiles?)
    'misc': obj_misc}			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)


class objtype:
    def __init__ (self, obj_id, health, img, size_x, behaviour):	#on object creation (Loading), object details loaded.
        self.id = obj_id					#Todo: Check list on generation of conflicting IDs and throw error.
        self.health = health				#Hits to remove || frames until timeout
        self.img = pyglet.image.load(img)			#Load image for object
        self.x = 0
        self.y = 0
        self.sprite = pyglet.sprite.Sprite(self.img,self.x,self.y)
        self.ai = behaviour					#AI reference	- See ai.py

def init_obj():
    obfile = open('objlist','r');			#text file of tab seperated variables. Line = Object, tab = field.
    for line in obfile:						#Id, Type, Health, Image location, sprite size, Behavior.
        obparse = line.split()				#Parse read line into list for processing.
        if (len(obparse) == 6):			#Line contains expected number of elements
							#Populate relvent list as specified in line element[1] and object type dictionary.
            new_object=objtype(obparse[0],obparse[2],obparse[3],obparse[4],obparse[5])
            obj_type[obparse[1]].append(new_object)


def spawn(obj_list,obj_proto,obj_id,x,y):	#References object from object list, copies object-prototype into active objects lists.
    spawned = copy.copy(obj_type[obj_proto][obj_id])		#Make copy of object from prototype lists
    spawned.x = x					#Set gameworld co-ord specifed
    spawned.y = y
    spawned.sprite = pyglet.sprite.Sprite(spawned.img,x,y)
    obj_list.append(spawned)				#Append object to active lists so it is processed and rendered in game.
	
