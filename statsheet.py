class StatSheet:
    max_health = 0
    temp_max_health = 0
    health = 0
    temp_health = 0
    ac = 0
    speed = 0
    stats = [0, 0, 0, 0, 0, 0]

    def __init__(self, max_health, ac, speed, stats=None):
        self.max_health = max_health
        self.ac = ac
        self.speed = speed
        if stats is not None and len(stats) == 6:
            self.stats = stats
        else:
            self.stats = [0, 0, 0, 0, 0, 0]

    def heal(self, amount):
        assert self.is_integer(amount), "Heal amount must be whole number."
        self.health += amount
        self.validate_health()

    def damage(self, amount):
        assert self.is_integer(amount), "Damage amount must be whole number."
        if self.temp_health > 0:
            self.temp_health = self.temp_health - amount
            if self.temp_health < 0:
                self.health += self.temp_health
        else:
            self.health = self.health - amount
        self.validate_health()

    def validate_health(self):
        if self.health < 0:
            self.health = 0

        if self.temp_health < 0:
            self.temp_health = 0

        if self.health > self.max_health + self.temp_max_health:
            self.health = self.max_health + self.temp_max_health

    def set_temp_max_health(self, amount):
        assert self.is_integer(amount), "Temporary maximum health must be a whole number."
        self.temp_max_health = amount

    def set_max_health(self, amount):
        assert self.is_integer(amount) and amount >= 0, "Maximum health must be a whole number of 0 or higher."
        self.max_health = amount

    def set_speed(self, amount):
        assert self.is_integer(amount) and amount >= 0, "Speed must be a whole number of 0 or higher."
        self.speed = amount

    def set_ac(self, amount):
        assert self.is_integer(amount) and amount >= 0, "Armor class must be a whole number of 0 or higher."
        self.ac = amount

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_temp_max_health(self):
        return self.temp_max_health

    def get_temp_health(self):
        return self.temp_health

    def get_ac(self):
        return self.ac

    def get_speed(self):
        return self.speed

    def get_stats(self):
        return self.stats

    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()
