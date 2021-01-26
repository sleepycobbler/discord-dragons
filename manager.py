import discord
import jsonmaster

tl_corn = '╔'
tr_corn = '╗'
bl_corn = '╚'
br_corn = '╝'
hor = '═'
vert = '║'
t_up = '╩'
t_down = '╦'
t_left = '╣'
t_right = '╠'
cross = '╬'


class Manager(commands.Cog):
    def __init__(self):
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        pass

    def get_target(self):
        pass

    def set_target(self):
        pass

    def display_main(self):
        pass

    def display_floor_plans(self):
        pass

    def display_characters(self):
        pass

    def display_props(self):
        pass

    def display_parties(self):
        pass
