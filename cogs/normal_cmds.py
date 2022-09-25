import discord

from discord.ext import commands

class commands(commands.Cog, description="Normal user commands for everyone!"):
    def __init__(self, client):
        self.client: commands.Bot = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog wurde geladen\n-----")
     
    @commands.command(aliases=["p"], help="This command shows the ping of the bot. Usage: `%ping`")
    async def ping(self, ctx):
        embed = discord.Embed(description=f'**🏓 Pong** `{round(self.client.latency * 1000)}ms`', color=discord.Colour.random())
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(commands(client))
