import character


class Player:
    name = ''
    id = ''
    characters = []
    isDM = False

    def __init__(self, name, id):
        self.name = name
        self.id = id
