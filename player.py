import character


class Player:
    name = ''
    id = ''
    characters = []
    is_dm = False

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.characters = []
        self.is_dm = False
