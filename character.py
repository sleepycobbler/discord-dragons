import statsheet
import entity


class Character(entity.Entity):
    initiative = 0

    def __init__(self, name, player_name, max_health, armor_class, speed, stats=None):
        super().__init__(name)
        self.sheet = statsheet.StatSheet(max_health, armor_class, speed, stats)
        self.player_name = player_name

    def set_sheet(self, stats):
        self.sheet = stats

    def set_initiative(self, initiative):
        assert self.is_integer(initiative), "Initiative must be a whole number."
        self.initiative = initiative

    def get_sheet(self):
        return self.sheet

    def get_initiative(self):
        return self.initiative

    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()


