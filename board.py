from PIL import Image, ImageDraw, ImageFont


class Board:
    name = ''
    id = 0
    width = 0
    length = 0
    entities = []
    fill = '.'
    wall = '█'
    blank = ' '
    axis_is_labeled = True
    mobile_friendly = False
    y_buffer = 3
    x_buffer = 4

    def __init__(self, width, length, name='', fill='.', wall='█', axis_is_labeled=True, mobile_friendly=False):
        self.set_width(width)
        self.set_length(length)
        self.set_name(name)
        self.set_fill(fill)
        self.set_wall(wall)
        self.set_axis_is_labeled(axis_is_labeled)
        self.set_mobile_friendly(mobile_friendly)

    def set_name(self, name):
        self.name = name

    def set_width(self, width):
        assert self.is_integer(width) and width > 0, "Width must be a whole number larger than 0."
        if self.axis_is_labeled:
            assert width <= 52, "Width cannot be labeled and go past lowercase z."
        self.width = width
        pass

    def set_length(self, length):
        assert self.is_integer(length) and length > 0, "Length must be a whole number larger than 0."
        self.length = length
        pass

    def set_fill(self, fill):
        self.fill = fill
        pass

    def set_axis_is_labeled(self, axis_is_labeled):
        self.axis_is_labeled = axis_is_labeled
        pass

    def set_mobile_friendly(self, mobile_friendly):
        self.mobile_friendly = mobile_friendly

    def set_wall(self, wall):
        self.wall = wall

    def add_entity(self, new_entity):
        new_entity.verify_entity()
        self.entities.append(new_entity)

    def remove_entity(self, old_entity):
        self.entities.remove(old_entity)

    def display(self):

        x = self.width + 4
        y = self.length + 3

        assert x * y < 2000, "Board cannot exceed 2000 Characters."

        my_board = []

        for row in range(y):
            my_board.append([self.fill] * x)

        my_board[1] = [self.wall] * x
        my_board[y - 1] = [self.wall] * x

        for row in my_board:
            row[2] = self.wall
            row[int(x) - 1] = self.wall
            row[0] = self.blank
            row[1] = self.blank

        my_board[0] = [self.blank] * x

        my_char = 'A'
        count = 1

        for column in range(3, x - 1):
            my_board[0][column] = my_char
            if ord(my_char) == ord('Z'):
                my_char = chr(ord(my_char) + 7)
            else:
                my_char = chr(ord(my_char) + 1)

        for row in range(2, y - 1):
            if row < 11:
                my_board[row][1] = str(count)
                count += 1
            else:
                my_board[row][0] = str(count)[0]
                my_board[row][1] = str(count)[1]
                count += 1

        # Display all entities on board

        for token in self.entities:
            pos = token.get_position()
            token_x = token.get_size()[0]
            token_y = token.get_size()[1]
            token_row = 0
            token_column = 0
            for area in range(token_x * token_y):
                temp_x = (pos[0] + 3) + token_column
                temp_y = pos[1] * -1 + 2 + token_row
                if not bool((area + 1) % token_x):
                    if temp_x < x and temp_y < y:
                        my_board[temp_y][temp_x] = token.get_icon()[area % len(token.get_icon())]
                    token_column = 0
                    token_row += 1
                else:
                    if temp_x < x and temp_y < y:
                        my_board[temp_y][temp_x] = token.get_icon()[area % len(token.get_icon())]
                    token_column += 1

        board_string = '```'

        for row in my_board:
            board_string += '\n'
            for cell in row:
                board_string += cell

        board_string += '```'

        assert len(board_string) <= 2000, "Board cannot exceed 2000 Characters."

        return board_string

    def display_no_axis(self):
        x = self.width + 2
        y = self.length + 2

        assert x * y < 2000, "Board cannot exceed 2000 Characters."

        my_board = []

        for row in range(y):
            my_board.append([self.fill] * x)

        my_board[0] = [self.wall] * x
        my_board[y] = [self.wall] * x

        for row in my_board:
            row[0] = self.wall
            row[int(x)] = self.wall

        board_string = '```'

        for row in my_board:
            board_string += '\n'
            for cell in row:
                board_string += cell

        board_string += '```'

        assert len(board_string) <= 2000, "Board cannot exceed 2000 Characters."

        return board_string

    def convert_mobile_friendly(self, board_string):
        if self.mobile_friendly:
            img = Image.new('RGB', (self.length * 38, self.width * 60), color=(73, 109, 137))
            fnt = ImageFont.truetype('fonts/cour.ttf', 60)
            d = ImageDraw.Draw(img)
            d.text((10, 10), board_string.strip('`'), font=fnt, fill=(255, 255, 0))
            img.save('my_file.png')

    def is_within_board(self, token):
        if 0 < token.get_position()[0] <= self.width + self.x_buffer - 1 and 0 > token.get_position()[1] >= \
                ((self.length + self.y_buffer - 1) * -1):
            return True
        else:
            return False

    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()
