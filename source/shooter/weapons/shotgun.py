from shooter.weapons import gun

class Shotgun(gun.Gun):
    def __init__(self):
        gun.Gun.__init__(self, "shotgun")
