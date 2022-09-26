import discord
import datetime

from discord.ext import commands

class commands_mod(commands.Cog, description="Normal user commands for everyone!"):
    def __init__(self, client):
        self.client: commands.Bot = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog wurde geladen\n-----")
    
    @commands.command(help="Kick command, to kick users. Usage: `%kick @Joniii Insulting` or `%kick @Joniii`")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No Reason Provided"):
        if user.id == self.client.user.id:
            embed = discord.Embed(description=":x: Why did you try to kick me? Do you hate me so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user == ctx.author:
            embed = discord.Embed(description=":x: Why do you want to kick yourself? Do you hate yourself so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user.guild_permissions.kick_members:
            embed = discord.Embed(description=":x: You can't kick that member, because he has the permission (`kick_members`).", color=discord.Colour.red()).ctx.send(embed=embed)
            return await ctx.send(embed=embed)
                
        embed_kicked_dm = discord.Embed(title=f"You got kicked from {ctx.guild.name}!", description=f"Kicked by: **{ctx.author.mention}**", color=discord.Colour.red()).add_field(name="Reason:", value=f"{reason}", inline=False)    
        embed_kicked_dm.timestamp=datetime.datetime.utcnow()
          
        try:     
            await user.send(embed=embed_kicked_dm)
        except Exception:
            embed_error = discord.Embed(description=":x: **Cannot send the message to the user, he blocked me or disabled his dms.**", color=discord.Colour.red())
            await ctx.send(embed=embed_error)
            pass
        
        await ctx.guild.kick(user, reason=reason)
        embed_kicked = discord.Embed(title="Kicked!", description=f"The user {user.mention} got kicked successfully from the server.", color=discord.Colour.red()).add_field(name="Reason:", value=f"{reason}", inline=False)
        embed_kicked.timestamp=datetime.datetime.utcnow()
        await ctx.send(embed=embed_kicked)
        
    @commands.command(aliases=["b"],help="Ban command, to ban users. Usage: `%ban @Joniii He spammed to much`")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No Reason Provided"):
        if user.id == self.client.user.id:
            embed = discord.Embed(description=":x: Why did you try to ban me? Do you hate me so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user == ctx.author:
            embed = discord.Embed(description=":x: Why do you want to ban yourself? Do you hate yourself so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user.guild_permissions.ban_members:
            embed = discord.Embed(description=":x: You can't ban that member, because he has the permission (`ban_members`).", color=discord.Colour.red()).ctx.send(embed=embed)
            return await ctx.send(embed=embed)
        
        embed_banned_dm = discord.Embed(title=f"You got banned from {ctx.guild.name}!", description=f"Banned by: **{ctx.author.mention}**", color=discord.Colour.red()).add_field(name="Reason:", value=f"{reason}", inline=False)
        embed_banned_dm.timestamp=datetime.datetime.utcnow()
        
        try:                        
            await user.send(embed=embed_banned_dm)   
        except Exception:            
            embed_error = discord.Embed(description=":x: **Cannot send the message to the user, he blocked me or disabled his dms.**", color=discord.Colour.red())
            await ctx.send(embed=embed_error)            
            pass
        
        await ctx.guild.ban(user, reason=reason)
        embed_banned = discord.Embed(title="Banned!", description=f"The user {user.mention} got banned successfully from the server.", color=discord.Colour.red()).add_field(name="Reason:", value=f"{reason}", inline=False)
        embed_banned.timestamp=datetime.datetime.utcnow()
        await ctx.send(embed=embed_banned)    
            
        
              
    
def setup(client):
    client.add_cog(commands_mod(client))
