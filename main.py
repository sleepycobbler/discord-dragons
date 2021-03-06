import discord
import logging
from PIL import Image, ImageDraw, ImageFont
from discord.ext import tasks, commands
import board
import statsheet
import character
import player
import floorplan
import entity
import prop
import party
import os
import emoji
import inflect
import json
import jsonpickle
import jsonmaster
import add
import lister
import manager

bot_token = os.environ['BOT_TOKEN']

number_converter = inflect.engine()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.add_cog(add.Add(bot))
bot.add_cog(lister.Lister(bot))
bot.add_cog(manager.Manager(bot))

floor_plans = []
registered_players = []
characters = []
props = []
master_list_template = {
    'floor_plans': floor_plans,
    'fp_current_id': 0,
    'target_floor_plan_id': 0,
    'registered_players': registered_players,
    'characters': characters,
    'char_current_id': 0,
    'props': props,
    'props_current_id': 0,
    'board_current_id': 0
}


@tasks.loop(seconds=1.0, count=6)
async def slow_count(my_msg):
    current_loop = slow_count.current_loop
    if current_loop != 0:
        new_msg = my_msg.content[0:len(my_msg.content) - 1] + '{seconds}'.format(seconds=(current_loop - 5) * -1)
        await my_msg.edit(content=new_msg)
    if current_loop == 5:
        await my_msg.delete()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("with Max's sanity")
    await bot.change_presence(activity=game, status=discord.Status.online)


@bot.command(name="menu")
async def display_menu():
    pass

@bot.command(name="reset")
@commands.has_permissions(manage_channels=True)
async def reset_server(ctx):
    matches = [x for x in ctx.guild.channels if x.category is not None]
    my_matches = [x for x in matches if x.category.name == 'DISCORD & DRAGONS BOT']
    for match in my_matches:
        await match.delete()
    await my_matches[0].category.delete()
    await create_channels(ctx)


@bot.command(name="initialize")
@commands.has_permissions(manage_channels=True)
async def create_channels(ctx):

    matches = [x for x in ctx.guild.channels if x.category is not None]

    my_matches = [x for x in matches if x.category.name == 'DISCORD & DRAGONS BOT']

    if len(my_matches) < 3:
        my_category = await ctx.guild.create_category('DISCORD & DRAGONS BOT')
        await ctx.guild.create_text_channel('board', category=my_category)
        await ctx.guild.create_text_channel('manager', category=my_category)
        await ctx.guild.create_text_channel('dnd_database_do_not_edit', category=my_category)
        database_channel = [x for x in ctx.guild.channels if x.name == 'dnd_database_do_not_edit']
        manager_channel = [x for x in ctx.guild.channels if x.name == 'manager' and x.category == my_category]
        await database_channel[0].send(jsonpickle.encode(master_list_template))
        await jsonmaster.JsonMaster.add(ctx, floorplan.FloorPlan('Floor 1'))
        manager_message = await manager_channel[0].send(manager.display_main_manager())
        await manager_message.add_reaction(emoji.emojize(':up_arrow:'))
        await manager_message.add_reaction(emoji.emojize(':down_arrow:'))
        await manager_message.add_reaction(emoji.emojize(':question_mark:'))
        await manager_message.add_reaction(emoji.emojize(':eye:'))
    else:
        my_msg = await ctx.channel.send('This server has already been initialized.\n This message will be deleted in 5')
        await slow_count.start(my_msg)


# @bot.command(name="register")
# async def register_player(ctx):
#     current_data = await jsonmaster.JsonMaster.get_current_data(ctx)
#     current_players = current_data['registered_players']
#
#     if len([x for x in current_players if x.id == str(ctx.author)]) > 0:
#         await ctx.channel.send('player is already registered.')
#         return
#
#     await jsonmaster.JsonMaster.add(ctx, player.Player(ctx.author.name, str(ctx.author)))
#     await ctx.channel.send('player Registered!')


@bot.command(name="players")
async def list_players(ctx):
    users = ''
    current_data = await jsonmaster.JsonMaster.get_current_data(ctx)
    current_users = current_data['registered_players']
    for user in current_users:
        users += '\n' + user.id + ' '
    await ctx.channel.send('Users are:' + users)


@bot.command(name="floorplan")
async def handle_floor_plan(ctx, name, action='add'):
    current_data = await jsonmaster.JsonMaster.get_current_data(ctx)

    if action == 'add':
        await jsonmaster.JsonMaster.add(ctx, floorplan.FloorPlan(name))
        await ctx.send('Floor plan \"' + name + "\" has been created and saved!")

    if action == 'target':
        target_floor_plan = [x for x in (current_data['floor_plans']) if x.name == name][0]
        target_index = current_data['floor_plans'].index(target_floor_plan)
        current_data['target_floor_plan_id'] = current_data['floor_plans'][target_index].id
        await jsonmaster.JsonMaster.purge_current_data(ctx)
        await jsonmaster.JsonMaster.send_current_data(ctx, current_data)
        await ctx.send('Floor plan \"' + name + "\" has been targeted for work!")


@bot.command(name="board")
async def handle_board(ctx, *args):
    async with ctx.channel.typing():
        current_data = await jsonmaster.JsonMaster.get_current_data(ctx)

        width = int(args[0].split('x')[0])
        length = int(args[0].split('x')[1])
        if len(args) > 1 and args[1] not in ['-f', '-w', '-mf', '-nl']:
            name = args[1]
        else:
            name = 'Board ' + str(current_data['board_current_id'] + 1)

        if (width * 2 + 5) * (length + 4) > 2000:
            await ctx.channel.send("Dimensions too large")
            return

        if width > 52:
            await ctx.channel.send("Width is too long; cannot exceed 52. Try switching the length and width.")
            return

        def f(fill):
            new_board.fill = fill

        def w(wall):
            new_board.wall = wall

        def mf(friend):
            new_board.mobile_friendly = True

        def nl(no_labels):
            new_board.axis_is_labeled = False

        switcher = {
            'f': f,
            'w': w,
            'mf': mf,
            'nl': nl
        }

        new_board = board.Board(width, length, name=name)

        arg_marker = 0
        for arg in args:
            if arg[0] == '-':
                func = switcher.get(arg.strip('-'), "nothing")
                if len(args) + 1 > arg_marker:
                    func(args[arg_marker + 1])
                else:
                    func()
            arg_marker += 1
        async with ctx.channel.typing():
            await ctx.channel.send("Here is the new board named \"" + name + "\"")

        board_string = new_board.display_square()
        async with ctx.channel.typing():
            my_msg = await ctx.channel.send(board_string)
        async with ctx.channel.typing():
            await jsonmaster.JsonMaster.add(ctx, new_board, obj_parent_id=current_data['target_floor_plan_id'])

        target_floor_plan = [x for x in (current_data['floor_plans']) if x.id == current_data['target_floor_plan_id']][0]
        target_index = current_data['floor_plans'].index(target_floor_plan)
        async with ctx.channel.typing():
            await ctx.channel.send("Board saved to floor plan \"" + current_data['floor_plans'][target_index].name + "\"")

bot.run(bot_token)
