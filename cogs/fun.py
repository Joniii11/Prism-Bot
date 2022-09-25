import discord

from discord_together import DiscordTogether
from discord.ext import commands

PREFIX = "%"

class Fun(commands.Cog, description="Some fun commands - Everyone likes a little bit of fun right?"):
    def __init__(self, client):
        self.client: commands.Bot = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.togetherControl = await DiscordTogether(self.client.http.token)
        print(f"{self.__class__.__name__} cog wurde geladen\n-----")
        
    @commands.command(help=f"Beam command. You can Bean with the command some people. Usage: `{PREFIX}beam @Joniii He was not nice to me :C`")
    @commands.guild_only()
    async def beam(self, ctx, user: commands.MemberConverter, *, reason=None):
        embed = discord.Embed(
            title="✅ Member beamed.",
            colour=discord.Colour.random(),
            description=f"The member {user.mention} got beamed by {ctx.author.mention}."
        )
        embed.add_field(name="Reason:", value=reason)
        await ctx.send(embed=embed)
        
    @commands.command(help=f"Smite command. You can smite people with this. Usage: `{PREFIX}smite @Joniii`")
    @commands.guild_only()
    async def smite(self, ctx, user: commands.MemberConverter):
        embed = discord.Embed(
            title=":zap: The Smite was successfull",
            color=discord.Colour.gold(),
            description=f"The user {user.mention} got Smitten by {ctx.author.mention}."
        )
        embed.set_image(url="https://tenor.com/view/thor-hammer-lightning-marvel-gif-14081443")
        await ctx.send(embed=embed)
    
        
def setup(client):
    client.add_cog(Fun(client))