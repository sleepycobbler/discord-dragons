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

bot_token = os.environ['BOT_TOKEN']

number_converter = inflect.engine()

print(bot_token)

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='!')

floor_plans = [floorplan.FloorPlan("Floor 1")]
selections = [board.Board(1, 1, "dummy"), floor_plans[0], character.Character("dummy"), prop.Prop("dummy"), player.Player("dummy", "dummy")]
registered_players = []
characters = []
props = []
master_list = {
    'floor_plans': floor_plans,
    'registered_players': registered_players,
    'characters': characters,
    'props': props
}


@tasks.loop(seconds=1.0, count=6)
async def slow_count(my_msg):
    current_loop = slow_count.current_loop
    if current_loop != 0:
        new_msg = my_msg.content[0:len(my_msg.content) - 1] + '{seconds}'.format(seconds=(current_loop - 5) * -1)
        await my_msg.edit(content=new_msg)
    if current_loop == 5:
        await my_msg.delete()
    # keycap = number_converter.number_to_words(current_loop)
    # if current_loop == 0:
    #     for my_num in range(5):
    #         other_num = number_converter.number_to_words(my_num + 1)
    #         await my_msg.add_reaction(emoji.emojize(':keycap_digit_{num}:'.format(num=other_num)))
    #         await my_msg.edit(content="newcontent")
    # else:
    #     await my_msg.remove_reaction(emoji.emojize(':keycap_digit_{num}:'.format(num=keycap)), bot.user)
    #     if current_loop == 5:
    #         await my_msg.delete()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("with Max's sanity")
    await bot.change_presence(activity=game, status=discord.Status.online)

@bot.command(name="menu")
async def display_menu():
    pass


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
        await database_channel[0].send(jsonpickle.encode(master_list))
    else:
        my_msg = await ctx.channel.send('This server has already been initialized.\n This message will be deleted in 5')
        await slow_count.start(my_msg)


@bot.command(name="register")
async def register_player(command):
    for player_test in registered_players:
        if str(command.author) == player_test.id:
            await command.channel.send('player is already registered.')
            return

    registered_players.append(player.Player(command.author.name, str(command.author)))
    await command.channel.send('player Registered!')


@bot.command(name="players")
async def list_players(command):
    users = ''
    for user in registered_players:
        users += '\t' + str(user) + '\n'
    await command.channel.send('Users are:\n' + users)


@bot.command(name="list")
async def list_items(ctx):
    list = ''

    list += 'Floor plans:\n'
    for plan in floor_plans:
        list += "\t" + plan.name + ':\n'
        for plan_board in plan.boards:
            list += '\t\t' + plan_board.name + '\n'

    list += '\nPlayers:\n'

    for my_player in registered_players:
        list += '\t' + str(my_player.id) + '\n'

    list += '\nCurrent selections:\n'

    count = 0

    selections_list = {
        0: "Board",
        1: "Floor plan",
        2: "Character",
        3: "Prop",
        4: "Player"
    }

    for selection in selections:
        if selection.name != "dummy":
            list += '\t' + selections_list.get(count) + "\n\t\t" + selection.name + "\n"
        else:
            list += '\t' + selections_list.get(count) + "\n\t\tNone\n"
        count += 1

    await ctx.send(list)


@bot.command(name="floorplan")
async def handle_floor_plan(ctx, arg):
    floor_plans.append(floorplan.FloorPlan(str(arg)))
    await ctx.send("The floor plan \"" + arg + "\" has been added.")


@bot.command(name="board")
async def handle_board(ctx, *args):

    width = int(args[0].split('x')[0])
    length = int(args[0].split('x')[1])
    if len(args) > 1 and args[1] != ['-f', '-w', '-mf', '-nl']:
        name = args[1]
    else:
        name = 'Board ' + str(len(floor_plans[0].boards) + 1)

    if width * length >= 2000:
        await ctx.channel.send("Dimensions too large")
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
            func(args[arg_marker + 1])
        arg_marker += 1

    await ctx.channel.send("Here is the new board named \"" + name + "\"")

    board_string = new_board.display()

    floor_plans[0].boards.append(new_board)

    my_msg = await ctx.channel.send(board_string)

    await ctx.channel.send("Board saved to floor plan \"" + floor_plans[0].name + "\"")

    data_channel = [x for x in ctx.guild.channels if x.name == 'dnd_database_do_not_edit']

    if len(await data_channel[0].history(limit=200).flatten()) > 0:
        old_master_data_string = ''

        for section in await data_channel[0].history(limit=200).flatten():
            old_master_data_string = section.content + old_master_data_string
            await section.delete()

        data_channel[0].purge()

        old_master_data = jsonpickle.decode(old_master_data_string)

        old_master_data['floor_plans'][0].boards.append(new_board)

        json_store = jsonpickle.encode(old_master_data)

        n = 1999
        split_list_data = [json_store[i:i + n] for i in range(0, len(json_store), n)]

        for msg in split_list_data:
            await data_channel[0].send(msg)

bot.run(bot_token)

# @bot.command(name="select")
# async def handle_select(ctx, *args):
#
#     if len(args) == 0:
#         await ctx.send("Please say what you would like to select (e.g. board, floorplan, character, prop, player)")
#         return
#
#     if len(args) == 1:
#         await ctx.send("Please state the name of the thing you would like to select")
#         return
#
#     target = args[0].lower()
#     name = args[1].lower()
#
#     async def select_board(name):
#         board_match = [x for x in selections[1].boards if x.name == name]
#         if len(board_match) < 1:
#             await ctx.send("Board \"" + name + "\" was not found within the selected \"" + selections[1].name + "\"
#             floor plan.")
#             return
#         else:
#             selections.pop(0)
#             selections.insert(0, board_match[0])
#
#     async def select_floor_plan(name):
#         floor_plan_match = [x for x in floor_plans if x.name == name]
#         if len(floor_plan_match) < 1:
#             await ctx.send("Floor plan \"" + name + "\" was not found.")
#             return
#         else:
#             selections.pop(1)
#             selections.insert(1, floor_plan_match[0])
#
#     async def select_character(name):
#         character_match = [x for x in characters if x.name == name]
#         if len(character_match) < 1:
#             await ctx.send("\"" + name + "\" was not found among the characters.")
#             return
#         else:
#             selections.pop(2)
#             selections.insert(2, [x for x in characters if x.name == name][0])
#
#     async def select_prop(name):
#         selections.pop(3)
#         selections.insert(3, [x for x in props if x.name == name][0])
#
#     async def select_player(name):
#         player_match = [x for x in registered_players if x.name == name]
#         if len(player_match) < 1:
#             await ctx.send("\"" + name + "\" was not found among the players.")
#             return
#         else:
#             selections.pop(4)
#             selections.insert(4, player_match[0])
#
#     switcher = {
#         "board": select_board,
#         "floorplan": select_floor_plan,
#         "character": select_character,
#         "prop": select_prop,
#         "player": select_player
#     }
#
#     await switcher.get(target)(name)
#
#     selection_list = ''
#
#     count = 0
#
#     selections_list = {
#         0: "Board",
#         1: "Floor plan",
#         2: "Character",
#         3: "Prop",
#         4: "Player"
#     }
#
#     for selection in selections:
#         if selection.name != "dummy":
#             selection_list += '\t' + selections_list.get(count) + "\n\t\t" + selection.name + "\n"
#         else:
#             selection_list += '\t' + selections_list.get(count) + "\n\t\tNone\n"
#         count += 1
#
#     await ctx.send("Current selections:\n" + selection_list)
