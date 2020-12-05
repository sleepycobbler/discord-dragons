import discord
from discord.ext import commands
import jsonmaster
import floorplan
import board
import character
import prop
import player


class DimensionsConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return argument.split('x')
        except Exception:
            await ctx.send('Dimensions must be in the format WidthxLength.')
            return


class Add(commands.Cog):
    @commands.group()
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify what you would like to add: floorplan, board, character, prop, or player")

    @add.command()
    async def floorplan(self, ctx, *name: str):
        await jsonmaster.JsonMaster.add(ctx, floorplan.FloorPlan(name))

    @add.command()
    async def board(self, ctx, dimensions: DimensionsConverter(), name=None, *mods):

        width = int(dimensions[0])
        length = int(dimensions[0])

        if (width * 2 + 5) * (length + 4) > 2000:
            await ctx.channel.send("Dimensions too large")
            return

        if width > 52:
            await ctx.channel.send("Width is too long; cannot exceed 52. Try switching the length and width.")
            return

        board_mods = []
        board_name = None

        if name is not None and name[0] == '-':
            board_mods.append(name)
            board_mods.extend(list(mods))
            board_name = None
        elif name is not None:
            board_mods = mods
            board_name = name

        new_board = board.Board(width, length, name=board_name)

        arg_marker = 0
        for mod in board_mods:
            if mod[0] == '-':
                base_mod = mod.strip('-')
                if base_mod == 'f' or 'fill':
                    try:
                        new_board.fill = board_mods[arg_marker + 1]
                        assert len(new_board.fill) == 1
                    except Exception:
                        await ctx.send('There must be a single character after the -f or -fill modifier.')
                        return
                elif base_mod == 'w' or 'wall':
                    try:
                        new_board.wall = board_mods[arg_marker + 1]
                        assert len(new_board.wall) == 1
                    except Exception:
                        await ctx.send('There must be a single character after the -w or -wall modifier.')
                        return
                elif base_mod == 'nl' or 'no_labels':
                    new_board.no_labels = True
            arg_marker += 1

        async with ctx.channel.typing():
            current_data = await jsonmaster.JsonMaster.get_current_data(ctx)
            await ctx.channel.send("Here is the new board named \"" + name + "\"")
            board_string = new_board.display_square()
            my_msg = await ctx.channel.send(board_string)
            await jsonmaster.JsonMaster.add(ctx, new_board, obj_parent_id=current_data['target_floor_plan_id'])
            target_floor_plan = \
            [x for x in (current_data['floor_plans']) if x.id == current_data['target_floor_plan_id']][0]
            target_index = current_data['floor_plans'].index(target_floor_plan)
            await ctx.channel.send(
            "Board saved to floor plan \"" + current_data['floor_plans'][target_index].name + "\"")

    @add.command()
    async def character(self, ctx, name: str, player_name: discord.Member, max_health: int, armor_class: int, speed: int, *stats: int):

        if max_health < 1:
            await ctx.send('Max health cannot be less than 1.')
            return
        if armor_class < 0:
            await ctx.send('Armor class cannot be less than 0.')
            return
        if speed < 0:
            await ctx.send('Speed cannot be less than 0.')
            return

        current_data = await jsonmaster.JsonMaster.get_current_data(ctx)

        if str(player_name) not in current_data['registered_players']:
            await ctx.send('Player is not registered for this campaign.')
            return

        new_character = character.Character(name, str(player_name), max_health, armor_class, speed, list(stats))

        current_data['characters'].append(new_character)

        player_match = [x for x in current_data['registered_players'] if x.id == str(player_name)]

        player_match_index = current_data['registered_players'].index(player_match)

        current_data['registered_players'][player_match_index].characters.append(new_character)

        await jsonmaster.JsonMaster.purge_current_data(ctx)
        await jsonmaster.JsonMaster.send_current_data(ctx, current_data)
        await ctx.send('\"' + name + '\" has been added to characters under ' + str(player_name))

    @add.command()
    async def prop(self):
        pass

    @add.command()
    async def player(self):
        pass

    @commands.command()
    async def register(self, ctx):
        current_data = await jsonmaster.JsonMaster.get_current_data(ctx)
        current_players = current_data['registered_players']

        if len([x for x in current_players if x.id == str(ctx.author)]) > 0:
            await ctx.channel.send('player is already registered.')
            return

        await jsonmaster.JsonMaster.add(ctx, player.Player(ctx.author.name, str(ctx.author)))
        await ctx.channel.send('player Registered!')
