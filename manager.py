import discord
import jsonmaster
from discord.ext import tasks, commands
import emoji

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
up_arrow = emoji.emojize(':up_arrow:')
down_arrow = emoji.emojize(':down_arrow:')
question_mark = emoji.emojize(':question_mark:')
eye = emoji.emojize(':eye:')

states = {'Main Menu': '1', 'floor plans': '2', 'characters': '3', 'props': '4', 'players': '5', 'parties': '6'}

state_menus = {'Main Menu': '\n:arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show / hide tips\n:eye: = View',
               'floor plans': '2',
               'characters': '3',
               'props': '4',
               'players': '5',
               'parties': '6'}

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def display_main_manager():
    return (
     "Main Menu\n```╔══╦═════════════╗\n║##║  Category   ║\n╠══╬═════════════╣\n║->║/Floor plans ║\n║  " +
     "║/Characters  ║\n║  ║/Props       ║\n║  ║/Players     ║\n║  ║/Party       ║\n╚══╩═════════════╝" +
     "```\n:arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show / hide tips\n:eye: = View"
    )


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id != self.bot.user.id:
            ctx_str = str(reaction.message.content)
            current_state = ctx_str.splitlines()[0]
            indexes = list(find_all(ctx_str, '║  ║'))
            c_index = list(find_all(ctx_str, '║->║'))[0]
            if reaction.emoji == up_arrow:
                ctx_str = str(ctx_str[:int(c_index)] + '║  ║' + ctx_str[(int(c_index)+4):])
                for ii in range(len(indexes)):
                    if ii == len(indexes) - 1:
                        if indexes[ii] < c_index:
                            ctx_str = str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                            break
                        elif indexes[ii] > c_index:
                            ctx_str = str(ctx_str[:int(indexes[len(indexes) - 1])] + '║->║' + ctx_str[int(indexes[len(indexes) - 1]) + 4:])
                            break
                    elif indexes[ii] < c_index < indexes[ii + 1]:
                        ctx_str = str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                        break
                await reaction.message.edit(content=str(ctx_str))
            elif reaction.emoji == down_arrow:
                ctx_str = str(ctx_str[:int(c_index)] + '║  ║' + ctx_str[(int(c_index) + 4):])
                for ii in range(len(indexes)):
                    if indexes[ii] > c_index:
                        ctx_str = str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                        break
                    elif ii == len(indexes) - 1:
                        ctx_str = str(ctx_str[:int(indexes[0])] + '║->║' + ctx_str[int(indexes[0]) + 4:])
                        break
                await reaction.message.edit(content=str(ctx_str))
            elif reaction.emoji == eye:
                new_menu = ctx_str[c_index + 5:].split()[0]
                print(new_menu)
            elif reaction.emoji == question_mark:
                quote_index = list(find_all(ctx_str, '```'))[1]
                if len(ctx_str[quote_index:]) <= 3:
                    await reaction.message.edit(content=str(ctx_str + state_menus[current_state]))
                else:
                    await reaction.message.edit(content=str(ctx_str[:quote_index + 3]))

    @commands.Cog.listener(name="on_reaction_remove")
    async def on_reaction_remove(self, reaction, user):
        if user.id != self.bot.user.id:
            ctx_str = await jsonmaster.JsonMaster.get_manager_text(reaction)
            current_state = ctx_str.splitlines()[0]
            indexes = list(find_all(ctx_str, '║  ║'))
            c_index = list(find_all(ctx_str, '║->║'))[0]
            if reaction.emoji == up_arrow:
                ctx_str = str(ctx_str[:int(c_index)] + '║  ║' + ctx_str[(int(c_index) + 4):])
                for ii in range(len(indexes)):
                    if ii == len(indexes) - 1:
                        if indexes[ii] < c_index:
                            ctx_str = str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                            break
                        elif indexes[ii] > c_index:
                            ctx_str = str(ctx_str[:int(indexes[len(indexes) - 1])] + '║->║' + ctx_str[int(
                                indexes[len(indexes) - 1]) + 4:])
                            break
                    elif indexes[ii] < c_index < indexes[ii + 1]:
                        ctx_str = str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                        break
                await reaction.message.edit(content=str(ctx_str))
            elif reaction.emoji == down_arrow:
                ctx_str = str(ctx_str[:int(c_index)] + '║  ║' + ctx_str[(int(c_index) + 4):])
                for ii in range(len(indexes)):
                    if indexes[ii] > c_index:
                        ctx_str = str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                        break
                    elif ii == len(indexes) - 1:
                        ctx_str = str(ctx_str[:int(indexes[0])] + '║->║' + ctx_str[int(indexes[0]) + 4:])
                        break
                await reaction.message.edit(content=str(ctx_str))
            elif reaction.emoji == eye:
                new_menu = ctx_str[c_index + 5:].split()[0]
                print(new_menu)
            elif reaction.emoji == question_mark:
                quote_index = list(find_all(ctx_str, '```'))[1]
                if len(ctx_str[quote_index:]) <= 3:
                    await reaction.message.edit(content=str(ctx_str + state_menus[current_state]))
                else:
                    await reaction.message.edit(content=str(ctx_str[:quote_index + 3]))

    def get_target(self):
        pass

    def set_target(self):
        pass

    def display_main(self, ctx):
        pass

    def display_floor_plans(self):
        pass

    def display_characters(self):
        pass

    def display_props(self):
        pass

    def display_parties(self):
        pass
