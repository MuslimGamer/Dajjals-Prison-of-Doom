obj_enemy=[]
obj_player=[]
obj_bullet=[]
obj_misc=[]


def obj_enemy():
    obj_enemy.append(objtype(obparse[0],obparse[2],obparse[3],obparse[4],obparse[5]))

def obj_player():
    obj_player.append(objtype(obparse[0],obparse[2],obparse[3],obparse[4],obparse[5]))

def obj_bullet():
    obj_bullet.append(objtype(obparse[0],obparse[2],obparse[3],obparse[4],obparse[5]))

def obj_misc ():
    obj_misc.append(objtype(obparse[0],obparse[2],obparse[3],obparse[4],obparse[5]))


class objtype:
    def __init__ (self, obj_id, health, img, size, behaviour):
	if not (obj_id in obj_list):
        self.id = obj_id
	    self.health = health	#Hits to remove || frames until timeout
	    self.img = pyglet.image.load(img)
        self.ai = behaviour		#AI reference
    else:
        raise(Exception('Error: Duplicate object-ID {0}'.format(obj_id)))
        return -1

def object_init():
    obfile = open('objlist','r');
    for line in obfile:
        obparse = line.split()
        if (obparse.len() == 6):
            obj_list.append(objtype(obparse[0],obparse[1],obparse[2],obparse[3],obparse[4],obparse[5]))
