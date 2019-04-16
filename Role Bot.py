import discord
import asyncio
import json
import os.path

CLIENT = discord.Client()

# Loads in discord key from file.
if os.path.isfile('keys.json'):
    with open('keys.json', 'r') as file_handle:
        KEY = json.load(file_handle)

async def assign_member_role():
    await CLIENT.wait_until_ready()
    while not CLIENT.is_closed:
        try:
            games = {}
            server_roles = []
            ignore_games = ['Spotify']
            members = list(CLIENT.get_all_members())
            for member in members:
                server = member.server

                #Get roles from server
                for role in server.roles:
                    if role not in server_roles:
                        server_roles.append(role.name)

                #Create list of games that members are playing
                if member.game == None or member.game.name in ignore_games:
                    continue
                if member.game.name not in games:
                    games[member.game.name] = [member]
                if member in games[member.game.name]:
                    continue
                else:
                    games[member.game.name].append(member)

            #Create server roles for games that 3+ members are playing
            for game in games:
                if game not in server_roles and len(games[game]) > 2:
                    role = await CLIENT.create_role(server,name=game,mentionable=True)
                    if role.name not in server_roles:
                        server_roles.append(role.name)

            #Assign members to role
            for game in games:
                if game in server_roles:
                    for member in games[game]:
                        role_objects = server.roles
                        for role_object in role_objects:
                            if game == role_object.name:
                                await CLIENT.add_roles(member,role_object)
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(120)
            continue


CLIENT.loop.create_task(assign_member_role())

CLIENT.run(KEY['discord'])
