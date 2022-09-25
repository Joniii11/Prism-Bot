import discord
import aiohttp
import random

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

    # Reddit/meme command
    @commands.command(help="This command will send a funny meme. Usage: `%meme`", pass_context=True)
    async def meme(self, ctx):
        embed = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed = discord.Embed(colour=discord.Colour.random())
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)           
        
    @commands.command(help="Flip a coin", aliases=["coinflip", "flipcoin", "cf"])
    async def flip(self, ctx):
        if random.randint(1, 10) <= 5:

            embed = discord.Embed(description="I flipped a coin for you, it is **Head**!", colour=discord.Colour.random())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="I flipped a coin for you, it is **Tails**!", colour=discord.Colour.random())
        
    # ------- Discord together ---------
    @commands.command(help="With that command you can watch with your friends YouTube videos in Voice Channels. Usage: `%yt`", aliases=["youtube", "yt"])
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def youtubetogether(self, ctx):
        try:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        except:
            embed = discord.Embed(description="**:x: Error! Please join a Voice Channel first.**", color=discord.Colour.red())
            return await ctx.send(embed=embed)

        embed=discord.Embed(
            title="Youtube Together", 
            description=f"[Click here]({link})", 
            color=discord.Colour.random()
        )
        await ctx.send(embed=embed)
    
        
def setup(client):
    client.add_cog(Fun(client))
