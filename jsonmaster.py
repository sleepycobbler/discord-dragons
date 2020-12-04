import json
import jsonpickle
import discord
from discord.ext import tasks, commands
import floorplan, board, entity, board, character, player, party, statsheet, prop


class JsonMaster:

    @staticmethod
    async def purge_current_data(ctx):
        data_channel = [x for x in ctx.guild.channels if
                        x.name == 'dnd_database_do_not_edit']
        await data_channel[0].purge()

    @staticmethod
    async def get_current_data(ctx):
        data_channel = [x for x in ctx.guild.channels if
                        x.name == 'dnd_database_do_not_edit']
        data = await data_channel[0].history(limit=200).flatten()
        if len(data) > 0:
            old_master_data_string = ''

            for section in await data_channel[0].history(limit=200).flatten():
                old_master_data_string = section.content + old_master_data_string

            return jsonpickle.decode(old_master_data_string)

    @staticmethod
    async def add(ctx, obj, obj_parent_id=-1):

        master_data = await JsonMaster.get_current_data(ctx)

        if isinstance(obj, floorplan.FloorPlan):
            obj.id = master_data['fp_current_id']
            master_data['fp_current_id'] += 1
            master_data['floor_plans'].append(obj)

        if isinstance(obj, board.Board):
            if obj_parent_id >= 0:
                obj.id = master_data['board_current_id']
                master_data['board_current_id'] += 1
                target_floor_plan = [x for x in (master_data['floor_plans']) if x.id == obj_parent_id][0]
                target_index = master_data['floor_plans'].index(target_floor_plan)
                master_data['floor_plans'][target_index].boards.append(obj)

        if isinstance(obj, character.Character):
            obj.id = master_data['char_current_id']
            master_data['char_current_id'] += 1
            master_data['characters'].append(obj)

        if isinstance(obj, prop.Prop):
            obj.id = master_data['props_current_id']
            master_data['props_current_id'] += 1
            master_data['props'].append(obj)
            pass

        if isinstance(obj, party.Party):
            pass

        if isinstance(obj, player.Player):
            master_data['registered_players'].append(obj)

        await JsonMaster.purge_current_data(ctx)
        await JsonMaster.send_current_data(ctx, master_data)

    @staticmethod
    async def remove_item(ctx, obj, obj_parent_id=-1):
        master_data = await JsonMaster.get_current_data(ctx)

        if isinstance(obj, floorplan.FloorPlan):
            if len(master_data['floor_plans']) > 1 and obj in master_data['floor_plans']:
                master_data['floor_plans'].remove(obj)

        if isinstance(obj, board.Board):
            if obj_parent_id >= 0 and obj in master_data['floor_plans'][obj_parent_id].boards:
                master_data['floor_plans'][obj_parent_id].boards.remove(obj)

        if isinstance(obj, character.Character):
            if obj in master_data['characters']:
                master_data['characters'].remove(obj)

        if isinstance(obj, prop.Prop):
            if obj in master_data['props']:
                master_data['props'].remove(obj)
            pass

        if isinstance(obj, party.Party):
            pass

        if isinstance(obj, player.Player):
            if obj in master_data['registered_players']:
                master_data['registered_players'].remove(obj)
        await JsonMaster.purge_current_data(ctx)
        await JsonMaster.send_current_data(ctx, master_data)
        pass

    @staticmethod
    async def edit_item(ctx, obj, obj_parent_id=-1):
        master_data = await JsonMaster.get_current_data(ctx)

        if isinstance(obj, floorplan.FloorPlan):
            if len(master_data['floor_plans']) > 0 and obj in master_data['floor_plans']:
                item_match = [x for x in (master_data['floor_plans']) if x.id == obj.id][0]
                item_index = master_data['floor_plans'].index(item_match)
                master_data['floor_plans'][item_index] = obj

        if isinstance(obj, board.Board):
            if obj_parent_id >= 0 and obj in master_data['floor_plans'][obj_parent_id].boards:
                item_match = [x for x in master_data['floor_plans'][obj_parent_id].boards if x.id == obj.id][0]
                item_index = master_data['floor_plans'][obj_parent_id].boards.index(item_match)
                master_data['floor_plans'][obj_parent_id].boards[item_index] = obj

        if isinstance(obj, character.Character):
            if obj in master_data['characters']:
                item_match = [x for x in master_data['characters'] if x.id == obj.id][0]
                item_index = master_data['characters'].index(item_match)
                master_data['characters'][item_index] = obj

        if isinstance(obj, prop.Prop):
            if obj in master_data['props']:
                item_match = [x for x in master_data['props'] if x.id == obj.id][0]
                item_index = master_data['props'].index(item_match)
                master_data['props'][item_index] = obj
            pass

        if isinstance(obj, party.Party):
            pass

        if isinstance(obj, player.Player):
            if obj in master_data['registered_players']:
                item_match = [x for x in master_data['registered_players'] if x.id == obj.id][0]
                item_index = master_data['registered_players'].index(item_match)
                master_data['registered_players'][item_index] = obj
        await JsonMaster.purge_current_data(ctx)
        await JsonMaster.send_current_data(ctx, master_data)

    @staticmethod
    async def send_current_data(ctx, data):
        data_channel = [x for x in ctx.guild.channels if
                        x.name == 'dnd_database_do_not_edit']

        encoded_data = jsonpickle.encode(data)

        n = 1999
        split_list_data = [encoded_data[x:x + n] for x in range(0, len(encoded_data), n)]

        for msg in split_list_data:
            await data_channel[0].send(msg)
