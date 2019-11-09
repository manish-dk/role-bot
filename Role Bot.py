import discord
import asyncio
import json
import os.path

CLIENT = discord.Client()

# Loads in discord key from file.
if os.path.isfile('keys.json'):
    with open('keys.json', 'r') as file_handle:
        KEY = json.load(file_handle)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.bg_task = self.loop.create_task(self.assign_member_role())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def assign_member_role(self):
        await self.wait_until_ready()
        while not CLIENT.is_closed():
            try:
                games = {}
                server_roles = []
                ignore_games = ['Spotify', 'Custom Status']
                members = list(CLIENT.get_all_members())
                for member in members:
                    server = CLIENT.guilds[0]

                    #Get roles from server
                    for role in server.roles:
                        if role not in server_roles:
                            server_roles.append(role.name)

                    #Create list of games that members are playing
                    if member.activity == None or member.activity.name in ignore_games:
                        continue
                    if member.activity.name not in games:
                        games[member.activity.name] = [member]
                    if member in games[member.activity.name]:
                        continue
                    else:
                        games[member.activity.name].append(member)

                #Create server roles for games that 3+ members are playing
                for game in games:
                    if game not in server_roles and len(games[game]) > 2:
                        role = await server.create_role(name=game,mentionable=True)
                        if role.name not in server_roles:
                            server_roles.append(role.name)

                #Assign members to role
                for game in games:
                    if game in server_roles:
                        for member in games[game]:
                            role_objects = server.roles
                            for role_object in role_objects:
                                if game == role_object.name:
                                    await member.add_roles(role_object)
                await asyncio.sleep(20)
            except:
                await asyncio.sleep(120)
                continue


CLIENT = MyClient()

CLIENT.run('')
