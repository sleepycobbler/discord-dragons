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

state_menus = {'Main Menu': '\n:arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show / hide tips\n'
                            ':eye: = View',
               'floor plans': ':arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show/Hide  tips\n'
                              ':eye: = View\n:pencil: = Edit\n:tools: = Create New\n'
                              ':busts_in_silhouette: = Copy\n:wastebasket: = Delete\n'
                              ':arrow_heading_up: = Return to Main Menu',
               'characters': ':arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show/Hide  tips\n'
                              ':eye: = View\n:pencil: = Edit\n:tools: = Create New\n'
                              ':busts_in_silhouette: = Copy\n:wastebasket: = Delete\n'
                              ':arrow_heading_up: = Return to Main Menu',
               'props': ':arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show/Hide  tips\n'
                              ':eye: = View\n:pencil: = Edit\n:tools: = Create New\n'
                              ':busts_in_silhouette: = Copy\n:wastebasket: = Delete\n'
                              ':arrow_heading_up: = Return to Main Menu',
               'players': ':arrow_up: = Move up\n:arrow_down: = Move down\n:question: = Show/Hide  tips\n'
                              ':eye: = View\n:pencil: = Edit\n:tools: = Create New\n'
                              ':busts_in_silhouette: = Copy\n:wastebasket: = Delete\n'
                              ':arrow_heading_up: = Return to Main Menu',
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
                await reaction.message.edit(content=str(self.up_arrow_handle(ctx_str, c_index, indexes)))
            elif reaction.emoji == down_arrow:
                await reaction.message.edit(content=str(self.down_arrow_handle(ctx_str, c_index, indexes)))
            elif reaction.emoji == eye:
                new_menu = ctx_str[c_index + 5:].split()[0]
                await reaction.message.edit(content=(await Manager.eye_handle(self, reaction, new_menu)))
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
                await reaction.message.edit(content=str(self.up_arrow_handle(ctx_str, c_index, indexes)))
            elif reaction.emoji == down_arrow:
                await reaction.message.edit(content=str(self.down_arrow_handle(ctx_str, c_index, indexes)))
            elif reaction.emoji == eye:
                new_menu = ctx_str[c_index + 5:].split()[0]
                await reaction.message.edit(content=(await Manager.eye_handle(self, reaction, new_menu)))
            elif reaction.emoji == question_mark:
                quote_index = list(find_all(ctx_str, '```'))[1]
                if len(ctx_str[quote_index:]) <= 3:
                    await reaction.message.edit(content=str(ctx_str + state_menus[current_state]))
                else:
                    await reaction.message.edit(content=str(ctx_str[:quote_index + 3]))

    @staticmethod
    def up_arrow_handle(ctx_str, c_index, indexes):
        ctx_str = str(ctx_str[:int(c_index)] + '║  ║' + ctx_str[(int(c_index) + 4):])
        for ii in range(len(indexes)):
            if ii == len(indexes) - 1:
                if indexes[ii] < c_index:
                    return str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
                elif indexes[ii] > c_index:
                    return str(ctx_str[:int(indexes[len(indexes) - 1])] + '║->║' + ctx_str[int(
                        indexes[len(indexes) - 1]) + 4:])
            elif indexes[ii] < c_index < indexes[ii + 1]:
                return str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])

    @staticmethod
    def down_arrow_handle(ctx_str, c_index, indexes):
        ctx_str = str(ctx_str[:int(c_index)] + '║  ║' + ctx_str[(int(c_index) + 4):])
        for ii in range(len(indexes)):
            if indexes[ii] > c_index:
                return str(ctx_str[:int(indexes[ii])] + '║->║' + ctx_str[int(indexes[ii]) + 4:])
            elif ii == len(indexes) - 1:
                return str(ctx_str[:int(indexes[0])] + '║->║' + ctx_str[int(indexes[0]) + 4:])

    def get_target(self):
        pass

    def set_target(self):
        pass

    def display_main(self, ctx):
        pass

    @staticmethod
    async def eye_handle(self, ctx, new_menu):
        eyeSwitcher = {
            "Floor": self.display_floor_plans,
            "Characters": self.display_characters,
            "Props": self.display_props,
            "Players": self.display_players,
            "Party": self.display_party,
            "Board": self.display_board
        }
        func = eyeSwitcher.get(new_menu)
        return await func(ctx)

    async def display_players(self, ctx):
        pass

    async def display_party(self, ctx):
        pass

    @staticmethod
    async def display_floor_plans(ctx):
        c_data = await jsonmaster.JsonMaster.get_current_data(ctx.message)
        plans = c_data['floor_plans']

        list_fp = ''

        body = ''

        list_fp += '**Floor plans:**\n'
        list_fp += '```'
        col_size = max(len(p.name) for p in plans) + 1
        if col_size > 15:
            col_size = 15
        nhs = ' ' * (col_size - 3)
        list_fp += tl_corn + hor * 2 + t_down + (hor * (col_size + 1)) + t_down + (hor * 13) + tr_corn + '\n'
        list_fp += vert + '##' + vert + nhs[:int(len(nhs) / 2)] + 'Name' + nhs[
                                                             int(len(nhs) / 2):] + vert + ' Board Count ' + vert + '\n'
        list_fp += t_right + hor * 2 + cross + (hor * (col_size + 1)) + cross + (hor * 13) + t_left + '\n'
        first = True
        for plan in plans:
            if first is True:
                if len(plan.name) > 15:
                    body += vert + '->' + vert + ' ' + plan.name[:12] + '...' + (' ' * (col_size - len(plan.name))) + vert + ' ' + str(len(plan.boards)) + \
                            (11 * ' ') + vert + '\n'
                else:
                    body += vert + '->' + vert + ' ' + plan.name + (' ' * (col_size - len(plan.name))) + vert + ' ' + str(len(plan.boards)) + \
                            (11 * ' ') + vert + '\n'
                    first = False
            else:
                if len(plan.name) > 15:
                    body += vert + '  ' + vert + ' ' + plan.name[:12] + '...' + (' ' * (col_size - len(plan.name))) + vert + ' ' + str(
                        len(plan.boards)) + \
                            (11 * ' ') + vert + '\n'
                else:
                    body += vert + '  ' + vert + ' ' + plan.name + (
                                ' ' * (col_size - len(plan.name))) + vert + ' ' + str(
                        len(plan.boards)) + \
                            (11 * ' ') + vert + '\n'
        list_fp += body
        list_fp += bl_corn + hor * 2 + t_up + (hor * (col_size + 1)) + t_up + (hor * 13) + br_corn + '\n'
        list_fp += '```'
        return str(list_fp)

    async def display_characters(self, ctx):
        c_data = jsonmaster.JsonMaster.get_current_data(ctx)
        pass

    async def display_props(self, ctx):
        c_data = jsonmaster.JsonMaster.get_current_data(ctx)
        pass

    async def display_parties(self, ctx):
        c_data = jsonmaster.JsonMaster.get_current_data(ctx)
        pass

    async def display_board(self, ctx):
        c_data = await jsonmaster.JsonMaster.get_current_data(ctx)

        pass
