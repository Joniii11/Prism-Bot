import discord

from discord.ext import commands

class commands(commands.Cog, description="Normal user commands for everyone!"):
    def __init__(self, client):
        self.client: commands.Bot = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog wurde geladen\n-----")
    
def setup(client):
    client.add_cog(commands(client))