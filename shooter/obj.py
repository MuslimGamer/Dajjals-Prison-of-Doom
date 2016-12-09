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
        self._health = json_data['Health']				#Hits to remove || frames until timeout
        self.img = pyglet.image.load(json_data['Img'])		#Load image for object, Todo: Construct list of images, check/skip if image already loaded by previous object.
        self.x = 0						#Current Positions
        self.y = 0
        self.mx = 0						#Current Movement
        self.my = 0		
        self.sprite = pyglet.sprite.Sprite(self.img,self.x,self.y)
        self.size = json_data['Size']
        self.ai = json_data['Behavior']				#AI reference	- See proc.py
        self.cooldown = 0
        self.cost = json_data['Cost']

        # Event handlers you can override
        self.on_death = lambda: None

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        if self._health <= 0 and self.on_death != None:
            self.on_death()

    @property
    def size(self):
        return self.sprite.scale

    @size.setter
    def size(self, value):
        self.sprite.scale = value

def load_prototype_data(raw_json):
    json_object = json.loads(raw_json)
    prototypes_json["Enemy"] = json_object["Enemies"]
    prototypes_json["Player"] = json_object["Player"]
    prototypes_json["Bullet"] = json_object["Bullets"]
    prototypes_json["Misc"] = json_object["Misc"]

###
# Spawns an object of type object_type (from prototypes_json, eg. "Enemy"), using
# data for the item with ID=id. It moves the object to (x, y).
# If as_type is not None, creates the object as an instance of the specified class (eg. SplashScreen)
# NOTE: as_type must be a subclass of GameObject with a constructor that takes 
# a single parameter "prototype" (JSON) data and passes it to the base class.
###
def spawn(object_type, id, x, y, as_type = None):
    list_of_prototypes = prototypes_json[object_type]
    # Find an object x in the collection that matches the specified ID; defaults to None
    prototype = next((x for x in list_of_prototypes if x['ID'] == id), None)
    if as_type is None:
        spawned = GameObject(prototype)
    else:
        spawned = as_type(prototype)
    
    spawned.x = x
    spawned.y = y
    spawned.sprite.set_position(x,y)
    return spawned
