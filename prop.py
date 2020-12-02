import entity


class Prop(entity.Entity):
    shape = ""
    is_rugged = False
    is_traversable = True

    def __init__(self, name):
        super().__init__(name)
