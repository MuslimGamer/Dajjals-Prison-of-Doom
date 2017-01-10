from shooter.obj import GameObject
import pyglet

class Npc(GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        GameObject.__init__(self, owner, "NPC", prototype)
        self.npcimage = pyglet.image.load('images/bluetriangle.png')
        self.npcseq = pyglet.image.ImageGrid(self.npcimage, 2, 1)
        self.image_index = 0
        self.sprite = pyglet.sprite.Sprite(self.npcseq[self.image_index], self.x, self.y)
        self.frame_count = 0

    def update(self):
        # Alternate images.
        self.frame_count += 1
        if self.frame_count >= 15:
            self.frame_count = 0
            # flip bit
            self.image_index = 1 - self.image_index
            self.sprite.image = self.npcseq[self.image_index]            