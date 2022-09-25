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
     
    @commands.command(aliases=["abt"], help="Shows everything about me. Usage: `%about`")
    async def about(self, ctx):
        embed = discord.Embed(title=f"Informations about the Bot", description=f"Hello, i am {self.client.user.name}. I am a small side Project from me **Joniii#0159** the Developer. I am in the open alpha phase at the moment, and kinda bad. I am 1 Month old now and have already many commands.", color=discord.Colour.random())
        embed.add_field(name="Informations About the Developer", value="Hi! I am Jonas. I am 14 Years old and from germany. I like coding bots in python, i learned that all by myself and some YouTube Tutorials. I am currently in the 10th grade and will finish the school in about 1 year.", inline=False)
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(commands(client))
