from shooter.weapons import gun

class Rail(gun.Gun):
    def __init__(self):
        gun.Gun.__init__(self, "rail")
