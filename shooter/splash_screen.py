from shooter import obj

class SplashScreen(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, "Misc", prototype)
        self.total_health = self.health

    def update(self):        
        health_percent = self.health / self.total_health
        if health_percent <= 0.50:
            # scale from [0 ... total_health] to [0 ... 255] if health < 50%
            # *2 means when health is 50%, we get 255 (fully opaque)
            # when health is 25%, we get 128 (half transparent)            
            self.sprite.opacity = health_percent * 255.0 * 2
