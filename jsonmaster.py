import json
import jsonpickle
import discord
from discord.ext import tasks, commands
import floorplan, board, entity, board, character, player, party, statsheet, prop


class JsonMaster:

    @staticmethod
    def get_current_data(ctx):
        data_channel = [x for x in ctx.guild.channels if
                        x.name == 'dnd_database_do_not_edit' and x.category == 'DISCORD & DRAGONS BOT']

        if len(await data_channel[0].history(limit=200).flatten()) > 0:
            old_master_data_string = ''

            for section in await data_channel[0].history(limit=200).flatten():
                old_master_data_string = section.content + old_master_data_string
                await section.delete()

            data_channel[0].purge()

            return jsonpickle.decode(old_master_data_string)
        else:
            pass

    @staticmethod
    def add(ctx, obj, obj_parent_id=-1):

        master_data = JsonMaster.get_current_data(ctx)

        if isinstance(obj, floorplan.FloorPlan):
            obj.id = len(master_data['floor_plans'])
            master_data['floor_plans'].append(obj)

        if isinstance(obj, board.Board):
            if obj_parent_id >= 0:
                obj.id = len(master_data['floor_plans'][obj_parent_id].boards)
                master_data['floor_plans'][obj_parent_id].boards.append(obj)

        if isinstance(obj, character.Character):
            obj.id = len(master_data['characters'])
            master_data['characters'].append(obj)

        if isinstance(obj, prop.Prop):
            obj.id = len(master_data['props'])
            master_data['props'].append(obj)
            pass

        if isinstance(obj, party.Party):
            pass

        if isinstance(obj, player.Player):
            obj.id = len(master_data['registered_players'])
            master_data['registered_players'].append(obj)

        JsonMaster.send_current_data(ctx, master_data)

    @staticmethod
    def remove_item(ctx, obj, obj_parent_id=-1):
        master_data = JsonMaster.get_current_data(ctx)

        if isinstance(obj, floorplan.FloorPlan):
            obj.id = len(master_data['floor_plans'])
            master_data['floor_plans'].append(obj)

        if isinstance(obj, board.Board):
            if obj_parent_id >= 0:
                obj.id = len(master_data['floor_plans'][obj_parent_id].boards)
                master_data['floor_plans'][obj_parent_id].boards.append(obj)

        if isinstance(obj, character.Character):
            obj.id = len(master_data['characters'])
            master_data['characters'].append(obj)

        if isinstance(obj, prop.Prop):
            obj.id = len(master_data['props'])
            master_data['props'].append(obj)
            pass

        if isinstance(obj, party.Party):
            pass

        if isinstance(obj, player.Player):
            obj.id = len(master_data['registered_players'])
            master_data['registered_players'].append(obj)

        JsonMaster.send_current_data(ctx, master_data)
        pass

    @staticmethod
    def send_current_data(ctx, data):
        data_channel = [x for x in ctx.guild.channels if
                        x.name == 'dnd_database_do_not_edit' and x.category == 'DISCORD & DRAGONS BOT']

        encoded_data = jsonpickle.encode(data)

        n = 1999
        split_list_data = [encoded_data[x:x + n] for x in range(0, len(encoded_data), n)]

        for msg in split_list_data:
            await data_channel[0].send(msg)
