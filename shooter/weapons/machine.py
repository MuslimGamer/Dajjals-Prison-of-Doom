from shooter.weapons import gun

class Machine(gun.Gun):
    def __init__(self):
        gun.Gun.__init__(self, "machine")
