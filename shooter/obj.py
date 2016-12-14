import json
import pyglet
import random
from shooter import config
from shooter import file_watcher
from math import atan2,atan, sin, cos, degrees, pi, sqrt



obj_enemy=[]	#Lists of object prototypes
obj_player=[]	#The one and only player prototype
obj_bullet=[]
obj_misc=[]

Player_list=[]			#Active player list - Swap player objects for powerup effects
Enemy_list= []			#Active enemy list
Bullet_list=[]			#Active bullet list
Misc_list = []			#Active cosmetic sprite list
Backgrounds_list = []		#Active backgrounds list

Type_lists = {
    'Enemy': Enemy_list,
    'Player': Player_list,
    'Bullet': Bullet_list,
    'Misc': Misc_list,
    'Background': Backgrounds_list
}

prototypes_json = {				#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'Player': obj_player,			#Object type Player.	(Future potential for multiple player types or upgrades?)
    'Bullet': obj_bullet,			#Object type Bullet.	(Future potential for various projectiles?)
    'Misc': obj_misc			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)
}

# Set by main.py
GAME_WIDTH = 0
GAME_HEIGHT = 0

def load_prototype_data(raw_json):
    json_object = json.loads(raw_json)
    prototypes_json["Enemy"] = json_object["Enemies"]
    prototypes_json["Player"] = json_object["Player"]
    prototypes_json["Bullet"] = json_object["Bullets"]
    prototypes_json["Misc"] = json_object["Misc"]
    prototypes_json["Background"] = json_object["Misc"] # horrible, hideous hack

def loot():
    SpawnIncome += 0.1

class Object_handler:      #Should I remove this class and just have the various functions loose in this file?
                           #IE outside of this file, call obj.spawn(), rather than Object_handler.spawn()
    def __init__(self):
        file_watcher.watch('data/object.json', load_prototype_data)

    SpawnBudget = 1
    SpawnIncome = 0.1
    NextEnemy = 0

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
            spawned = GameObject(self,object_type,prototype)
        else:
            spawned = as_type(self,prototype)
    
        spawned.x = spawned.centroid_x = x
        spawned.y = spawned.centroid_y = y
        spawned.sprite.set_position(x,y)
        Type_lists[object_type].append(spawned)
        return spawned

    def spawn_enemy(self,id, x, y):
        e = self.spawn("Enemy", id, x, y)
        #e.on_death = lambda: Loot()
        return e

    def spawn_random(self,dt):
        self.SpawnBudget += dt* self.SpawnIncome
        self.SpawnIncome += 0.01


        type_select_result = {
            0: "Enemy_Basic",
            1: "Enemy_Coward",
            2: "Enemy_Slow"
        }

        EnemyID = type_select_result[self.NextEnemy]


        list_of_prototypes = prototypes_json["Enemy"]
        # Find an object x in the collection that matches the specified ID; defaults to None
        prototype = next((x for x in list_of_prototypes if x['ID'] == EnemyID), None)
        
        print("SpawnBudget: " + str(self.SpawnBudget) + " NextEnemy: " + EnemyID + " Enemy.cost: " + str(prototype['Cost']))

        if self.SpawnBudget >= prototype['Cost']:
            self.SpawnBudget -= prototype['Cost']
            self.NextEnemy = random.randrange(3)
            side = random.randrange(4)
            rand_x = random.randrange(GAME_WIDTH)
            rand_y = random.randrange(GAME_HEIGHT)

            position_generate_x = {
                0: GAME_WIDTH + 100,
                1: -100,
                2: rand_x,
                3: rand_x
            }

            position_generate_y = {
                0: rand_y,
                1: rand_y,
                2: -100,
                3: GAME_HEIGHT + 100
            }


            self.spawn_enemy(EnemyID, position_generate_x[side],position_generate_y[side])


    def collision(self):
        for player in Player_list:
            for bullet in Bullet_list:
                player.Circle_collision(bullet)
            for enemy in Enemy_list:
                player.Circle_collision(enemy)
        for enemy in Enemy_list:
            for bullet in Bullet_list:
                enemy.Circle_collision(bullet)

    def update(self):
        for player in Player_list:
            player.move()
            player.update()
        for enemy in Enemy_list:
            enemy.ai()
            enemy.move()
            enemy.update()
        for bullet in Bullet_list:
            bullet.ai()
            bullet.move()
            bullet.update()
        for misc in Misc_list:
            misc.ai()
            misc.update()

        self.collision()

class GameObject:

    #on object creation (Loading), object details loaded.
    def __init__ (self,owner,object_type,json_data):
        #Asset management attributes
        self.handle = owner		                        #Needed to call spawn function from object for attacking
        self.type = object_type					#Store object type for easy referencing of own list.
        self.id = json_data['ID']				#Todo: Check list on generation of conflicting IDs and throw error.
        self.parent = 0	

    #Initialisation of object tracking variables
        self.x = 0						#Current Positions (Sprite Datum)
        self.y = 0
        self.mx = 0						#Current Movement
        self.my = 0	
        self.cooldown = 0					#Time until next attack avaliable
        self.centroid_x = 0					#Storing calculated centroid of sprite for current rotation.
        self.centroid_y = 0					#Reference of parent object (If any)
        self.theta = 0

        #Behavior management attributes
        #self.ai = json_data['Behavior']				#AI reference	- See proc.py
        self.speed = json_data['Speed']
        self.cost = json_data['Cost']
        self._health = json_data['Health']			#Hits to remove || frames until timeout

    #Sprite relevent attributes
	    #TODO: Construct list of images, check/skip if image already loaded by previous object.
        self.img = pyglet.image.load(json_data['Img'])		#Load image for object 
        self.sprite = pyglet.sprite.Sprite(self.img,self.x,self.y)
        self.size = json_data['Size']

    #Pre-calculating numbers for centering sprites after rotation. Maths is expensive, space is not.
    #Better to pre calculate constant trig functions than re-calculate when required.
            #Calculate 'radius' of sprite - Hyp component for finding sprite centroid following rotation.
            #Theta offset - Rotation offset for centroid location from sprite base rotation
        self.radius = sqrt(self.sprite.height*self.sprite.height + self.sprite.width * self.sprite.width)/2
        self.theta_offset = atan2(self.sprite.height,self.sprite.width)

        # Event handlers you can override
        self.on_death = lambda: None
        self.ai_type = json_data['Behavior']

        

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



    def Circle_collision(self, Target_object):
        if (self.id == Target_object.parent):return 0

    
        #Simple collision detection for rotating sprites.
        #Abstract circle is appoximated around sprite bounding the maximum sprite overlap area during rotation.
        #Calculated radius of this circle is accumulated from 2 test objects to detect range of collision
        #Distance between sprite centroids is calculated and compared to the detection range.
        dx = self.centroid_x - Target_object.centroid_x
        dy = self.centroid_y - Target_object.centroid_y
        radius = self.radius + Target_object.radius
        if(radius>sqrt(dx*dx + dy*dy)):
            print ("\nHit Detection! - Radius: " +str(radius))
            print (self.id +" X:" + str(self.centroid_x)+" " +self.id+" Y:"+str(self.centroid_y))
            print (Target_object.id +" X:" + str(Target_object.centroid_x)+" " +Target_object.id+" Y:"+str(Target_object.centroid_y))
            print (self.id +" Heath: " +str(self.health)+"\n")

            #print(self.id + Target_object.id)
            self.health = self.health - 1
            Target_object.health = 0
            return 1   #Hit detected
        return 0       #No Hit Detected


    def attack(self, Attack_Type, target_x,target_y):
        #Check object is currently able to attack (On screen, cooldown expired)
        if not (self.is_on_screen()) or (self.cooldown): return	

        # Calculate the angle of the shot by using trig
        # This gives us consistent bullet speed regardless of angle
        dx = target_x - self.centroid_x    
        dy = target_y - self.centroid_y
        theta = atan2(dx,dy)			

	#Spawn attack object
        b = self.handle.spawn('Bullet',Attack_Type,self.centroid_x+10*self.sprite.scale,self.centroid_y+10*self.sprite.scale)
        b.sprite.rotation = theta * 180/pi
        b.theta = theta	
        b.parent = self.id
        self.cooldown = b.cost     		#Apply cooldown from attack.

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

        if self.health <= 0:
            Type_lists[self.type].remove(self)
        
        if self.cooldown:
            self.cooldown = self.cooldown - 1


    def is_on_screen(self):
        return self.x >= 0 and self.x <= GAME_WIDTH - self.sprite.width and self.y >= 0 and self.y <= GAME_HEIGHT - self.sprite.width

    #AI functions:
    #Standard behavior, rush player, attack location
    def agro_ai(self, player):
        if player is None:
            return
            
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
        if player is None:
            return

        dx = self.x - player.x
        dy = self.y - player.y
        theta = atan2(dx,dy)			#Mathy goodness.
        distance_from_player = sqrt(dx*dx + dy*dy)
        # NOTE: ranodm here means sporadic firing when we're within d=150-250 of the player
        # This extra value should be persisted with the object somewhere for consistency
        # But, I doubt anyone will notice :)
        if (distance_from_player < 150 + random.randrange(100)):			#Get in kind of close.
            theta = theta *-0.9								#Jittery holding pattern
            if self.is_on_screen():
                self.attack('Bullet_Basic',player.x-50+random.randrange(100),player.y-50+random.randrange(100))	
	#Added inaccuracy

        self.mx = -1 * self.speed * sin(theta)
        self.my = -1 * self.speed * cos(theta)
   
        return

    def update(self):
        # "virtual" method. Subclasses override it.
        pass



#Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
    def misc_ai(self, player):
        if (self.health > 0):
            self.health = self.health - 1

    def sword_ai(self, player):
        if player is None:
            return
            
        self.health = player.cooldown
        self.mx = 0.01
        self.theta = self.theta +0.3
        self.sprite.rotation = self.theta * 180/pi + 90
        sword_attack_radius = config.get("sword_attack_radius")
        # +width/2, -height/2 makes the sword perfectly center on the player
        self.x = player.x + (player.img.width / 2) - (self.img.width / 2) + sin(self.theta) * sword_attack_radius
        self.y = player.y + (player.img.height / 2) + (self.img.height / 2) + cos(self.theta) * sword_attack_radius
    #if left button pressed, calc theta, rotation, then update sprite 
        pass

    def bullet_ai(self,player):
        self.health = self.health - 1
        self.mx = sin(self.theta) * self.speed
        self.my = cos(self.theta) * self.speed
        pass


#No AI attached to this object
    def NULL_ai(self,player):
        raise(Exception("NULL AI?!"))
        pass

#Undefined behavior referenced.
    def error_ai(self,player):
        raise(Exception('Error: AI has gone rouge'))


    #Generic AI handler
    #Reference dictionary against object AI variable, Vector to specific function for AI type.
    def ai(self):	
        ai_action={
            "agro": self.agro_ai,
            "coward": self.coward_ai,
            "bullet": self.bullet_ai,
            "sword": self.sword_ai,
            "NULL": self.NULL_ai,
            "misc": self.misc_ai
        }

        # Misc and bullet AIs don't depend on the player. We have to run them
        # even if there is no player. Trust that the AIs are smart enough not
        # to throw if player is null (null-check, or don't get instantiated
        # unless the player is around).
        if len(Player_list) > 0:
            for player in Player_list:
                ai_action[self.ai_type](player)		
            return
        else:
            ai_action[self.ai_type](None) # We don't have a player right now


# Prototypes of enemies, the player, bullets, and misc stuff (splash screens, explosions, etc.)


#prototypes_json = {		#Define object_type dictionary. Used to parse objects into correct list for later referencing.
#    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
#    'Player': obj_player,		#Object type Player.	(Future potential for multiple player types or upgrades?)
#    'Bullet': obj_bullet,		#Object type Bullet.	(Future potential for various projectiles?)
#    'Misc': obj_misc			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)
#}








