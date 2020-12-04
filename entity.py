class Entity:
    name = ''
    position = [0, 0]
    icon = ''
    size = [1, 1]
    id = -1

    def __init__(self, name):
        self.name = name
        self.id = -1
        self.position = [0, 0]
        self.icon = ''
        self.size = [1, 1]
        pass

    def set_name(self, name):
        assert name != '', 'Name must have at least one character.'
        self.name = name

    def set_position(self, pos):
        assert pos[0] >= 0 and self.is_integer(pos[0]), "X-Position must be on board and a whole number."
        assert pos[1] <= 0 and self.is_integer(pos[1]), "Y-Position must be on board and a whole number."
        self.position = pos

    def set_icon(self, icon):
        assert len(icon) <= (self.size[0] * self.size[1]), "Icon must fit within dimensions of entity."
        self.icon = icon

    def set_size(self, width, length=0):
        if length == 0:
            length = width
        assert self.is_integer(width) and self.is_integer(length), "Both width and length must be whole numbers."
        assert width > 0 and length > 0, "Both width and length of entity must be greater than 0."
        self.size = [width, length]

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_icon(self):
        return self.icon

    def get_size(self):
        return self.size

    def move(self, direction):
        assert self.is_integer(direction), "Movement must be either North(1), East(2), South(3), or West(4)."
        switcher = {
            1: [0, 1],
            2: [1, 0],
            3: [-1, 0],
            4: [0, -1]
        }

        self.position[0] += switcher[direction][0]
        self.position[1] += switcher[direction][1]

    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()
