from shooter.weapons import gun

class Rocket(gun.Gun):
    def __init__(self):
        gun.Gun.__init__(self, "rocket")

