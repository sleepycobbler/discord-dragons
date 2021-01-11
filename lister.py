import discord
from discord.ext import commands
import jsonmaster
import floorplan
import board
import character
import prop
import player

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


def list_floor_plans(ctx):

    plans = ctx['floor_plans']

    list_fp = ''

    body = ''

    list_fp += '**Floor plans:**\n'
    list_fp += '```'
    col_size = max(len(p.name) for p in plans) + 1
    nhs = ' ' * (col_size - 3)
    list_fp += tl_corn + (hor * (col_size + 1)) + t_down + (hor * 13) + tr_corn + '\n'
    list_fp += vert + nhs[:int(len(nhs) / 2)] + 'Name' + nhs[int(len(nhs) / 2):] + vert + ' Board Count ' + vert + '\n'
    list_fp += t_right + (hor * (col_size + 1)) + cross + (hor * 13) + t_left + '\n'
    for plan in plans:
        body += vert + ' ' + plan.name + (' ' * (col_size - len(plan.name))) + vert + ' ' + str(len(plan.boards)) + \
                (11 * ' ') + vert + '\n'
    list_fp += body
    list_fp += bl_corn + (hor * (col_size + 1)) + t_up + (hor * 13) + br_corn + '\n'
    list_fp += '```'
    return list_fp


def list_boards(plan):
    list_b = '**Boards: ' + plan.name + '**\n```'
    if len(plan.boards) < 1:
        return list_b + 'This Floor plan has no boards```'
    col_size = max(len(b.name) for b in plan.boards) + 1
    list_b += tl_corn + hor * col_size + t_down
    list_b += hor * 7 + t_down + hor * 8 + t_down + hor * 6 + t_down + hor * 6 + tr_corn + '\n'
    nhs = ' ' * (col_size - 4)
    name_pl = nhs[:int(len(nhs) / 2)]
    name_pr = nhs[int(len(nhs) / 2):]
    list_b += vert + name_pl + 'Name' + name_pr
    list_b += vert + '  WxL  ' + vert + ' Prop # ' + vert + ' Fill ' + vert + ' Wall ' + vert + '\n'
    list_b += t_right + hor * col_size + cross
    list_b += hor * 7 + cross + hor * 8 + cross + hor * 6 + cross + hor * 6 + t_left + '\n'
    for board in plan.boards:
        list_b += vert + board.name + (' ' * (col_size - len(board.name))) + vert
        dim = str(board.width) + 'x' + str(board.length)
        dim_space = ' ' * (6 - len(dim))
        list_b += ' ' + dim + dim_space + vert
        prop_amount = str(len([ent for ent in board.entities if isinstance(ent, prop)]))
        pa_space = ' ' * (7 - len(prop_amount))
        list_b += ' ' + prop_amount + pa_space + vert
        list_b += ' \'' + board.fill + '\'  ' + vert
        list_b += ' \'' + board.wall + '\'  ' + vert + '\n'
    list_b += bl_corn + hor * col_size + t_up
    list_b += hor * 7 + t_up + hor * 8 + t_up + hor * 6 + t_up + hor * 6 + br_corn + '```\n'
    return list_b


def list_props(ctx):
    props = ctx['props']
    pass


def list_players(ctx):
    players = ctx['registered_players']
    pass


def list_characters(ctx):
    chracters = ctx.characters
    pass


class Lister(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def list(self, ctx):
        current_data = await jsonmaster.JsonMaster.get_current_data(ctx)

        await ctx.send(list_floor_plans(current_data))
        for plan in current_data['floor_plans']:
            await ctx.send(list_boards(plan))
        await ctx.send(list_players(current_data))
        await ctx.send(list_characters(current_data))
        await ctx.send(list_props(current_data))

        # for plan_board in plan.boards:
        #    list += '\t\t' + plan_board.name + '\n'

        # list += '\nPlayers:\n'

        # for user in current_data['registered_players']:
        # list += '\t' + str(user.id) + '\n'

        # list += '\nCharacters:\n'

        # for char in current_data['characters']:
        #     list += '\t' + char.name + '\n'
