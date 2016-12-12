import json
import pyglet
from math import atan2,atan, sin, cos, degrees, pi, sqrt

# Prototypes of enemies, the player, bullets, and misc stuff (splash screens, explosions, etc.)


prototypes_json = {		#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'Player': obj_player,		#Object type Player.	(Future potential for multiple player types or upgrades?)
    'Bullet': obj_bullet,		#Object type Bullet.	(Future potential for various projectiles?)
    'Misc': obj_misc			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)
}

Type_lists = {
    'Enemy': Enemy_list,
    'Player': Player_list,
    'Bullet': Bullet_list,
    'Misc': Misc_list,
}

ai_action={
    "agro": agro_ai,
    "coward": coward_ai,
    "slow": slow_ai,
    "bullet": bullet_ai,
    "sword": sword_ai,
    "NULL": NULL_ai,
    "misc": misc_ai}


class Object_handler:
    def __init__(self):

        #Initialise object prototype lists:
        self.obj_enemy=[]	#Lists of object prototypes
        self.obj_player=[]	#The one and only player prototype
        self.obj_bullet=[]
        self.obj_misc=[]

        #Initialise active object lists:     #No longer referenced by index.
        self.Player_list=[]			#Active player list - Swap player objects for powerup effects
        self.Enemy_list= []			#Active enemy list
        self.Bullet_List=[]			#Active bullet list
        self.Misc_List = []			#Active cosmetic sprite list
        self.Backgrounds_List = []		#Active backgrounds list

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
    def spawn(self,object_type, id, x, y, as_type = None):
        list_of_prototypes = prototypes_json[object_type]
        # Find an object x in the collection that matches the specified ID; defaults to None
        prototype = next((x for x in list_of_prototypes if x['ID'] == id), None)
        if as_type is None:
            spawned = GameObject(self,prototype)
        else:
            spawned = as_type(self,prototype)
    
        spawned.x = x
        spawned.y = y
        spawned.sprite.set_position(x,y)
        return spawned

    def collision(self):
        for player in self.Player_list:
            for bullet in self.Bullet_list:
                player.collision(bullet)
            for enemy in self.Enemy_list:
                player.collision(enemy)
        for enemy in self.Enemy_list:
            for bullet in self.Bullet_list:
                enemy.collision(bullet)

    def update(self):
        for player in self.Player_list:
            player.move()
        for enemy in self.Enemy_list:
            enemy.ai()
            enemy.move()
        for bullet in self.Bullet_list:
            bullet.ai()
            bullet.move()
        for misc in self.misc_list:
            misc.ai()
        self.collision()




##TODO: Decide new location for below:

        # Call your update method, if you have one
        #if hasattr(obj, "update") and callable(getattr(obj, "update")):
        #    obj.update()
        #pass
            


class GameObject:
    __screen_width = 0
    __screen_height = 0

    def note_screen_size(width, height):
        global __screen_width
        global __screen_height

        __screen_width = width
        __screen_height = height 
        

    #on object creation (Loading), object details loaded.
    def __init__ (self,owner,json_data):
        #Asset management attributes
        self.owner = owner                                      #Pointer to Object handler for Inter-object functions.
        self.type = json_data					#Store object type for easy referencing of own list.
        self.id = json_data['ID']				#Todo: Check list on generation of conflicting IDs and throw error.
        self.parent = 0						#Reference of parent object (If any)

        #Behavior management attributes
        self.ai = json_data['Behavior']				#AI reference	- See proc.py
        self.cost = json_data['Cost']
        self._health = json_data['Health']			#Hits to remove || frames until timeout

	#Sprite relevent attributes
	#TODO: Construct list of images, check/skip if image already loaded by previous object.
        self.img = pyglet.image.load(json_data['Img'])		#Load image for object 
        self.sprite = pyglet.sprite.Sprite(self.img,self.x,self.y)
        self.size = json_data['Size']

	#Initialisation of object tracking variables
        self.x = 0						#Current Positions (Sprite Datum)
        self.y = 0
        self.mx = 0						#Current Movement
        self.my = 0	
        self.cooldown = 0					#Time until next attack avaliable
        self.centroid_x = 0					#Storing calculated centroid of sprite for current rotation.
        self.centroid_y = 0

        #Pre-calculating numbers for centering sprites after rotation. Maths is expensive, space is not.
        #Better to pre calculate constant trig functions than re-calculate when required.
            #Calculate 'radius' of sprite - Hyp component for finding sprite centroid following rotation.
            #Theta offset - Rotation offset for centroid location from sprite base rotation
        self.radius = sqrt(self.sprite.height*self.sprite.height + self.sprite.width * self.sprite.width)/2
        self.theta_offset = atan2(self.sprite.height,self.sprite.width)
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

    def collision(self, Target_object):
        if (self.parent == Target_object.id):return 0
    
        #Simple collision detection for rotating sprites.
        #Abstract circle is appoximated around sprite bounding the maximum sprite overlap area during rotation.
        #Calculated radius of this circle is accumulated from 2 test objects to detect range of collision
        #Distance between sprite centroids is calculated and compared to the detection range.
        dx = self.centroid_x - Target_object.centroid_x
        dy = self.centroid_y - Target_object.centroid_y
        radius = self.radius + Target_object.radius
        if(radius>sqrt(dx*dx + dy*dy)):
            self.health = obj1.health - 1
            Target_object.health = 0
            return 1   #Hit detected
        return 0       #No Hit Detected


    def attack(self, Attack_Type, target_x,target_y):
        #Check object is currently able to attack (On screen, cooldown expired)
        if not (source_obj.is_on_screen()) or (source_obj.cooldown): return	

        # Calculate the angle of the shot by using trig
        # This gives us consistent bullet speed regardless of angle
        dx = target_x - self.x    
        dy = target_y - self.y
        theta = atan2(dx,dy)			

	#Spawn attack object
        b = obj.spawn('Bullet',attack_type,self.x+mx*self.sprite.scale,self.y+my*self.sprite.scale)	
        b.parent = self.id
        b.sprite.rotation = theta

        self.cooldown = b.cost     		#Apply cooldown from attack.
        self.owner.bullet_list.append(b)	#Enter bullet object into active list for processing

    def move(self):
        #Function name move is misleading: Function responsible for processing movement, rotation & object maintainance
        if(self.mx!=0)or(self.my!=0):
            self.x = self.x + self.mx
            self.y = self.y + self.my
            #Calculate sprite rotation + position(Sprite centroid, not datum) and update sprite

            theta = atan2(-self.my,self.mx)		#Sprite face direction of movement.
            self.sprite.rotation = theta*180/pi	#Sprite rotation in degrees, while trig functions return radians (Like real maths)

            self.centroid_x = self.x - self.radius * sin(theta+self.theta_offset)	#Calculate centroid position given:
            self.centroid_y = self.y - self.radius * cos(theta+self.theta_offset)	# Sprite Datum position/Rotation &
           										# Calculated centroid offsets from sprite aspects
            self.sprite.set_position(self.centroid_x,self.centroid_y)

        if obj.health <= 0:
            self.owner.Type_lists[self.type].remove(obj)
        
        if obj.cooldown:
            obj.cooldown = obj.cooldown - 1


    def is_on_screen(self):
        global __screen_width
        global __screen_height
        return self.x >= 0 and self.x <= __screen_width - self.sprite.width and self.y >= 0 and self.y <= __screen_height - self.sprite.width


    #Generic AI handler
    #Reference dictionary against object AI variable, Vector to specific function for AI type.
    def ai(self, player):			
        ai_action[obj.ai](player)		

    #AI functions:
    #Standard behavior, rush player, attack location
    def agro_ai(self, player):
        dx = self.centroid_x - player.centroid_x
        dy = self.centroid_y - player.centroid_y
        distance_from_player = sqrt(dx*dx + dy*dy)
        if (distance_from_player > 30):				#Get in close
            theta = atan2(dx,dy)					#Mathy goodness.
            self.mx = -1 * self.speed * sin(theta)
            self.my = -1 * self.speed *cos(theta)
    return


    #Coward behavior, maintain distance, attack location
    def coward_ai(self, player):
        dx = obj.x - player.x
        dy = obj.y - player.y
        theta = atan2(dx,dy)			#Mathy goodness.
        distance_from_player = sqrt(dx*dx + dy*dy)
        # NOTE: ranodm here means sporadic firing when we're within d=150-250 of the player
        # This extra value should be persisted with the object somewhere for consistency
        # But, I doubt anyone will notice :)
        if (distance_from_player < 150 + random.randrange(100)):			#Get in kind of close.
            theta = theta *-0.9								#Jittery holding pattern
            if obj.is_on_screen():
                bullet_list = main_list[2]
                attack(obj,"Bullet_Basic",player.x-50+random.randrange(100),player.y-50+random.randrange(100),bullet_list)	
	#Added inaccuracy

        obj.mx = -1 *self.speed* sin(theta)
        obj.my = -1 *self.speed* cos(theta)
   
        return


#Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
def misc_ai(obj, main_list):
    if (obj.health > 0):
        obj.health = obj.health - 1

    def sword_ai(self, player):
    #if left button pressed, calc theta, rotation, then update sprite 
    return

    def bullet_ai(self,player):
    


#No AI attached to this object
def NULL_ai(obj, main_list):
    pass

#Undefined behavior referenced.
def error_ai(obj, main_list):
    raise(Exception('Error: AI has gone rouge'))



