import json
import random

import pyglet

from shooter import config
from shooter import file_watcher
from shooter import sound
from shooter import ai
from shooter import ui_manager
import shooter.tutorials.tutorial_manager

from math import atan2,atan, sin, cos, degrees, pi, sqrt
from shooter.weapons import gun, shotgun, rocket

from math import atan2,atan, sin, cos, degrees, pi, sqrt

obj_enemy=[]	#Lists of object prototypes
obj_player=[]	#The one and only player prototype
obj_bullet=[]
obj_misc=[]
obj_pickup=[]
obj_NPC=[]

Player_list=[]			#Active player list - Swap player objects for powerup effects
Enemy_list= []			#Active enemy list
NPC_list= []
Bullet_list=[]			#Active bullet list
Misc_list = []			#Active cosmetic sprite list
Pickup_list = []
Backgrounds_list = []		#Active backgrounds list

Type_lists = {
    'Enemy': Enemy_list,
    'Player': Player_list,
    'NPC': NPC_list,
    'Bullet': Bullet_list,
    'Misc': Misc_list,
    'Pickup': Pickup_list,
    'Background': Backgrounds_list
}

prototypes_json = {			#Define object_type dictionary. Used to parse objects into correct list for later referencing.
    'Enemy': obj_enemy,			#Object type Enemy.	(Add arbitary enemy times later)
    'Player': obj_player,		#Object type Player.	(Future potential for multiple player types or upgrades?)
    'Bullet': obj_bullet,		#Object type Bullet.	(Future potential for various projectiles?)
    'Misc': obj_misc,			#Object type Misc.	(Intended for graphical effects, Eg enemy dies spawn Explosion object)
    'Pickup': obj_pickup,
    'NPC': obj_NPC
}	

# Set by main.py
GAME_WIDTH = 0
GAME_HEIGHT = 0

score = 0

def load_prototype_data(raw_json):
    json_object = json.loads(raw_json)
    prototypes_json["Enemy"] = json_object["Enemies"]
    prototypes_json["NPC"] = json_object["NPC"]
    prototypes_json["Player"] = json_object["Player"]
    prototypes_json["Bullet"] = json_object["Bullet"]
    prototypes_json["Misc"] = json_object["Misc"]
    prototypes_json["Pickup"] = json_object["Pickup"]
    prototypes_json["Background"] = json_object["Misc"] # horrible, hideous hack

class Object_handler:      #Should I remove this class and just have the various functions loose in this file?
                           #IE outside of this file, call obj.spawn(), rather than Object_handler.spawn()

    def __init__(self):
        file_watcher.watch('data/object.json', load_prototype_data)
        self.start()
        Object_handler.instance = self

	###
	# Spawns an object of type object_type (from prototypes_json, eg. "Enemy"), using
	# data for the item with ID=id. It moves the object to (x, y).
	# If as_type is not None, creates the object as an instance of the specified class (eg. SplashScreen)
	# NOTE: as_type must be a subclass of GameObject with a constructor that takes 
	# a single parameter "prototype" (JSON) data and passes it to the base class.
	###
    def start(self):

        Player_list[:]=[]
        NPC_list[:]=[]
        Enemy_list[:]=[]
        Bullet_list[:]=[]
        Misc_list[:]=[]
        Pickup_list[:]=[]
        Backgrounds_list[:]=[]
        score = 0
        self.SpawnBudget = 4 # spawn an enemy quickly to start
        self.SpawnCost = 1
        self.SpawnIncome = 0.5
        self.NextEnemy = 0

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
        e.on_death = lambda: e.Loot(10)
        return e

    def spawn_random(self, dt, screen):
        spawned = 0

        if not (config.get('enable_enemies')):
            return
            
        if screen.paused or shooter.tutorials.tutorial_manager.is_showing_tutorial:
            return

        self.SpawnBudget += dt * self.SpawnIncome
        while(self.SpawnBudget >= self.SpawnCost):
            self.SpawnBudget -= self.SpawnCost

            type_select_result = {
                0: "NPC_Basic",
                1: "Enemy_Basic",
                2: "Enemy_Coward",
                3: "Enemy_Slow", 
            }

            EnemyID = type_select_result[self.NextEnemy]

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

            if(self.NextEnemy>0):
                self.spawn_enemy(EnemyID, position_generate_x[side],position_generate_y[side])
                spawned += 1
            else: 
                if config.get("enable_npc") and len(Player_list) <=3 and len(Enemy_list) > 0:
                    self.spawn('NPC',"NPC_Basic",position_generate_x[side],position_generate_y[side])
                    spawned += 1
            self.NextEnemy = random.randrange(4)

            if(self.NextEnemy>0):
                list_of_prototypes = prototypes_json["Enemy"]
                EnemyID = type_select_result[self.NextEnemy]
                prototype = next((x for x in list_of_prototypes if x['ID'] == EnemyID), None)
                self.SpawnCost = prototype['Cost']
            else: self.SpawnCost = 1

    def collision(self):
        for player in Player_list:
            if player == Player_list[0]:
                for pickup in Pickup_list:
                    player.pickup(pickup)
            for bullet in Bullet_list:
                player.Circle_collision(bullet)
            for enemy in Enemy_list:
                player.Circle_collision(enemy)
        for NPC in NPC_list:
            for bullet in Bullet_list:
                NPC.Circle_collision(bullet)
            for enemy in Enemy_list:
                NPC.Circle_collision(enemy)
        for enemy in Enemy_list:
            for bullet in Bullet_list:
                enemy.Circle_collision(bullet)

    def update(self):
        #ai.update()

        for enemy in Enemy_list:
            if enemy.health: enemy.ai()
        for NPC in NPC_list:
            NPC.ai()
        for bullet in Bullet_list:
            if bullet.health: bullet.ai()
        for misc in Misc_list:
            misc.ai()

        self.collision()    	#Attempting to add kick-back to collision.
                    #Collsion must be called after AI, but before move/update()

        for player in Player_list:

            # every tick, regenerate health
            player.health += player.repair
            if player.health > config.get("max_health"): 
                player.health = config.get("max_health")
            # If we're a full crew, repair the jump drive
            if player.crew == config.get("max_crew"):
                player.drive += 1

            player.update()
            player.move()

        for NPC in NPC_list:
            NPC.update()
            NPC.move()

        for enemy in Enemy_list:
            enemy.update()
            enemy.move()

        for bullet in Bullet_list:
            bullet.update()
            bullet.move()

        for misc in Misc_list:
            misc.update()
            misc.move()

        for pickup in Pickup_list:
            pickup.ai()
            pickup.update()
            pickup.move()


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
        self.destinationx = random.randrange(GAME_WIDTH)
        self.destinationy = random.randrange(GAME_HEIGHT)
        self.distance_from_player = 1000
        self.cooldown = 0					#Time until next attack avaliable
        self.aicooldown = 0
        self.centroid_x = 0					#Storing calculated centroid of sprite for current rotation.
        self.centroid_y = 0					#Reference of parent object (If any)
        self.theta = 0

        #Behavior management attributes
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
        if "Splash" in self.id or self.id == "Game Over" or self.id == "You Win":
            self.radius = 0
        else:
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

    def Loot(self,chance):
        self.handle.SpawnIncome += 0.1

        global score # obj.score
        score += self.cost

        if((random.randrange(100)<chance) and (len(Pickup_list)<3)):
            Type = random.randrange(5)
            PickupType = {
                0:"Weapon_Pistol",
                1:"Weapon_Machine",
                2:"Weapon_Shotgun",
                3:"Weapon_Rocket",
                4:"Weapon_Rail"
            }
            self.handle.spawn('Pickup',PickupType[Type],self.x, self.y)


    def pickup(self, Target_object):    #Cheap and hacky - Copy pasted collsion detection and modify for pickup rather than damage. 

        dx = self.x - Target_object.x
        dy = self.y - Target_object.y
        radius = self.radius + Target_object.radius
        if(radius>sqrt(dx*dx + dy*dy)):
            PickupType = {
                "Weapon_Pistol":"pistol",
                "Weapon_Machine":"machine",
                "Weapon_Shotgun":"shotgun",
                "Weapon_Rocket":"rocket",
                "Weapon_Rail":"rail"
            }

            # TODO: fix
            # main.Screen_handler.__ui_manager.alert(self.x, self.y +100, "New weapon: " + PickupType[Target_object.id], 'White')
            self.switch(PickupType[Target_object.id])
            sound.pickup.play()
            Target_object.health = 0
        

    def Circle_collision(self, Target_object):
        if (self.id == Target_object.parent): # ???
            return 0

        # Make sure we're on screen. No dying off-screen allowed. Points confuse the player.
        global GAME_WIDTH
        global GAME_HEIGHT
        if self.x < 0 or self.x > GAME_WIDTH or self.y < 0 or self.y > GAME_HEIGHT:
            return 0

        #Simple collision detection for rotating sprites.
        #Abstract circle is appoximated around sprite bounding the maximum sprite overlap area during rotation.
        #Calculated radius of this circle is accumulated from 2 test objects to detect range of collision
        #Distance between sprite centroids is calculated and compared to the detection range.
        dx = self.x - Target_object.x
        dy = self.y - Target_object.y
        radius = self.radius + Target_object.radius
        if(radius>sqrt(dx*dx + dy*dy)):

            self.health = self.health - 1
            if (self.id == "Deflect"): 
                theta = atan2(dx,dy)
                Target_object.mx = -1*Target_object.speed*sin(theta)
                Target_object.my = -1*Target_object.speed*cos(theta)
                if Target_object.type == "Bullet":
                    Target_object.parent = "Player_Basic"

                    Target_object.sprite.rotation = theta * 180/pi
                    Target_object.theta = theta	
                    Target_object.rotate()
                return
            else: 
                Target_object.health = 0

            #If self is still alive after collision, apply kick-back
            #Apply acceleration proportional to the ratio of mass of colliding objects.
            if self.health:

                if config.get("apply_recoil") == True:
                    self.mx += Target_object.mx *(Target_object.size/self.size)
                    self.my += Target_object.my *(Target_object.size/self.size)

                if(self.id == "Player_Basic"):
                    #If hit, % chance of losing crew
                    if random.randrange(100) < config.get("chance_to_lose_crew_on_hit_percent"):
                        self.crew -= 1
                        if not (self.crew): self.crew = 1		#Preserve atleast 1 crew member.

            if self.type == "Player": # Target type is enemy or bullet; with bullet, the explosion sound overtakes.
                sound.hurt.play()

            return 1   #Hit detected
        return 0       #No Hit Detected


    def attack(self, Attack_Type, target_x,target_y):
        if not (self.type == "Player" or self.type == "Bullet") and (not (self.is_on_screen()) or (self.cooldown)):
            # Check object is currently able to attack (On screen, cooldown expired)
            # Player manages its own cooldown            
            return False	

        # Calculate the angle of the shot by using trig
        # This gives us consistent bullet speed regardless of angle
        dx = target_x - self.x    
        dy = target_y - self.y
        theta = atan2(dx,dy)		

	#Spawn attack object
        b = self.handle.spawn('Bullet',Attack_Type,self.x,self.y,Bullet)
        b.sprite.rotation = theta * 180/pi
        b.theta = theta	

        b.mx = sin(b.theta) * b.speed
        b.my = cos(b.theta) * b.speed

        b.rotate()

        b.parent = self.id

        if(b.id == "Bullet_rocket"):self.on_death=lambda: self.explode()
        self.cooldown = b.cost     		#Apply cooldown from attack.
        return True

    def move(self):
        #Function name move is misleading: Function responsible for processing movement, rotation & object maintainance
        self.x = self.x + self.mx
        self.y = self.y + self.my

        if not (self.id == "Player_Basic"):

            #Calculate sprite rotation + position(Sprite centroid, not datum) and update sprite

            theta = atan2(-self.my,self.mx)		#Sprite face direction of movement
        else: 
            theta = self.theta
            if self.x < 0: self.x = GAME_WIDTH
            if self.x > GAME_WIDTH: self.x = 0
            if self.y < 0: self.y = GAME_HEIGHT
            if self.y > GAME_HEIGHT: self.y = 0

        if not config.get("control_style") == "relative":theta = atan2(-self.my,self.mx)
        self.sprite.rotation = theta*180/pi	#Sprite rotation in degrees, while trig functions return radians (Like real maths)

        self.sprite_x = self.x - self.radius * sin(theta+self.theta_offset)	#Calculate centroid position given:
        self.sprite_y = self.y - self.radius * cos(theta+self.theta_offset)	# Sprite Datum position/Rotation &
           										# Calculated centroid offsets from sprite aspects
        self.sprite.set_position(self.sprite_x,self.sprite_y)

        if self.health < 1:
            self.on_death()
            Type_lists[self.type].remove(self)
        
        if self.cooldown:
            self.cooldown = self.cooldown - 1
        if self.aicooldown:
            self.aicooldown -= 1


    def is_on_screen(self):
        return self.x >= 0 and self.x <= GAME_WIDTH - self.sprite.width and self.y >= 0 and self.y <= GAME_HEIGHT - self.sprite.width

    #AI functions:
    #Standard behavior, rush player, attack location

    def npc_ai(self, player):
        global score
        if player is None or self.health == 0:
            return
        
            #if not self.aicooldown:
        player = Player_list[0]				#Otherwise, look for player to follow.
        if not player.id == "Player_Basic": return
        dx = self.x - player.x
        dy = self.y - player.y
        self.distance_from_player = sqrt(dx*dx+dy*dy)
            
        if (self.distance_from_player < 10):		#Keep some distance from player to avoid crowding.
            player = Player_list[0]				#Otherwise, look for player to follow.
            if not player.id == "Player_Basic": return
            self.mx=self.my = 0
            self.health = 0
            sound.npc_pickup.play()

            player.crew = player.crew + 1
            if player.crew > config.get("max_crew"):
                player.crew = config.get("max_crew")
                score += config.get("max_npcs_score_boost")
                player.drive += 100 * config.get("max_npcs_drive_boost")
            player.upgrade() 
            return

        if (self.distance_from_player < 200):		#If player near: follow
            ai.charge(self,player)
            return
                   						#If player far:
        if not (self.aicooldown):
            ai.wander(self)				#Seek player or other NPCs (Preference to player)
            self.aicooldown = config.get("ai_cooldown_seconds") * 30
								#Flee bullets and enemies.wwwwwwwww
                    

    def agro_ai(self, player):
        if player is None:
            return
        if not (self.aicooldown):
            nearest = 1000
            self.Target = Player_list[0]
            for player in Player_list:				#Select nearest target
                dx = self.x - player.x
                dy = self.y - player.y
                self.distance_from_player = sqrt(dx*dx+dy*dy)
                if (self.distance_from_player < nearest): 
                    nearest = self.distance_from_player
                    self.Target = player
            for NPC in NPC_list:				#Select nearest target
                if not (NPC.id == "Deflect"):
                    dx = self.x - player.x
                    dy = self.y - player.y
                    self.distance_from_player = sqrt(dx*dx+dy*dy)
                    if (self.distance_from_player < nearest): 
                        nearest = self.distance_from_player
                        self.Target = NPC


            self.aicooldown = 120
        ai.charge(self,self.Target)					#Agro range: 400
        return

    #Coward behavior, maintain distance, attack location
    def coward_ai(self, player):
        if player is None:
            return
        #if self.is_on_screen():
        if not (self.aicooldown):
            nearest = 1000
            self.Target = Player_list[0]
            for player in Player_list:					#Select nearest target
                dx = self.x - player.x
                dy = self.y - player.y
                self.distance_from_player = sqrt(dx*dx+dy*dy)
                if (self.distance_from_player < nearest): 
                    nearest = self.distance_from_player
                    self.Target = player

            for NPC in NPC_list:				#Select nearest target
                if not (NPC.id == "Deflect"):
                    dx = self.x - player.x
                    dy = self.y - player.y
                    self.distance_from_player = sqrt(dx*dx+dy*dy)
                    if (self.distance_from_player < nearest): 
                        nearest = self.distance_from_player
                        self.Target = NPC
            self.aicooldown = 120

        player = self.Target

        if (self.distance_from_player < 150 + random.randrange(100)):	#If target in range, attempt to attack
            if self.attack('Bullet_Basic',player.x-50+random.randrange(100),player.y-50+random.randrange(100)): 
                sound.pistol.play()
            ai.flee(self, self.Target)					#Hold distance
            return
        ai.charge(self,self.Target)
        return


    # "virtual" method. Subclasses override it.
    def update(self):
        pass

    # "virtual" method. Subclasses override it.
    def on_death(self):
       pass



    #Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
    def misc_ai(self, player):
        if (self.health > 0):
            self.health = self.health - 1


    def deflect_ai(self, player):
        if player is None:
            return

        ##player = Player_list[0]
        #if not (player.id == "Player_Basic"):return
        shield_radius = config.get("sword_attack_radius") * 2



        self.health -=1
        self.mx = 0.01 * sin(self.theta)	#Apply small movement to ensure sword renders with correct rotation.
        self.my = 0.01 * cos(self.theta)        #Position applied below instead of movement function so position updated before collsion detection
        self.sprite.rotation = self.theta

        # +width/2, -height/2 makes the sword perfectly center on the player
        self.x = player.x +shield_radius * sin(self.theta)    #Apply position immediately so factors in collision detection
        self.y = player.y + shield_radius * cos(self.theta)  



    def sword_ai(self, player):
        pass

    def bullet_ai(self, player):
        pass

    def rocket_ai(self, player):
        pass


#No AI attached to this object - No decision making required on behalf of this object (EG Player or bullet)
    def NULL_ai(self, player):
        #raise(Exception("NULL AI?!"))
        pass

#Undefined behavior referenced.
    def error_ai(self, player):
        raise(Exception('Error: AI has gone rouge'))


    #Generic AI handler
    #Reference dictionary against object AI variable, Vector to specific function for AI type.
    def ai(self):	
        ai_action={
            "agro": self.agro_ai,
            "coward": self.coward_ai,
            "deflect": self.deflect_ai,
            "npc": self.npc_ai,
            "bullet": self.bullet_ai,
            "rocket": self.rocket_ai,
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


from shooter.bullets.bullet import Bullet
