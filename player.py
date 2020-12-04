import character


class Player:
    name = ''
    characters = []
    is_dm = False

    def __init__(self, name, player_id):
        self.name = name
        self.id = player_id
        self.characters = []
        self.is_dm = False
