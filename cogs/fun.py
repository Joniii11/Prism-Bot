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
            await ctx.send(embed=embed)
            
    @commands.command(help="Question the magical 8-ball a question. Usage: `%8ball Am i beatiful?`", name="8ball", aliases=["8ball", "8-ball"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eightball(self, ctx, *, question: str):
        icon_url = 'https://i.imgur.com/XhNqADi.png'
        # Antworten von Wikipedia :p
        responses = [
            # Yes answers
            "It is save.",
            "It's decided, like that.",
            "Without doubt.",
            "Yes, in any case.",
            "You can rely on it.",
            "The way I see it, yes.",
            "Most likely.",
            "Good prospects.",
            "Yes.",
            "The signs point to yes.",
            # Non-binding answers
            "Answers are blurry, try again.",
            "Ask again later.",
            "I better not tell you now.",
            "Can't predict now.",
            "Concentrate and just ask again.",
            # Negative answers
            "Don't count on it.",
            "My answer is no.",
            "My sources say no.",
            "Outlook is not that good.",
            "Very doubtful.",
        ]
        fortune = random.choice(responses)

        embed = discord.Embed(colour=16776960)
        embed.set_author(name='Magical 8-ball', icon_url=icon_url)
        embed.add_field(name=f'*{ctx.author.name}, My ball says:*', value=f'**{fortune}**')
        await ctx.send(embed=embed)     
       
        
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
