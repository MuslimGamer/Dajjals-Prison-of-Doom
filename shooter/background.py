from shooter import obj

# Lightweight object used for Backgrounds
class Background(obj.GameObject):
    def __init__(self, image, x = 0, y = 0):
        # call base class constructor
        prototype_data = {
            "ID":  "none", "Img":  image, "Speed":  0, "Cost":  0, "Health":  0, "Size":  1, "Behavior":  "NULL" }

        obj.GameObject.__init__(self, None, 'Background', prototype_data)
        
        self.sprite.x = x
        self.sprite.y = y