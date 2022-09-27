import re
import discord
import datetime
import asyncio

from copy import deepcopy
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta

nrp = "No Reason Provided"

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)



class commands_mod(commands.Cog, description="Normal user commands for everyone!"):
    def __init__(self, client):
        self.client: commands.Bot = client
        self.mute_task = self.check_current_mutes.start()
        
    def cog_unload(self):
        self.mute_task.cancel()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog wurde geladen\n-----")
        
    @tasks.loop(minutes=5)
    async def check_current_mutes(self):
        currentTime = datetime.datetime.now()
        mutes = deepcopy(self.client.muted_users)
        for key, value in mutes.items():
            if value['muteDuration'] is None:
                continue
            
            unmuteTime = value['mutedAt'] + relativedelta(seconds=value['muteDuration'])
            
            if currentTime >= unmuteTime:
                guild = self.client.get_guild(value['guildId'])
                user = guild.get_member(value['_id'])
                
                role = discord.utils.get(guild.roles, name="Muted")
                if role in user.roles:
                    await user.remove_roles(role)
                    print(f"Unmuted {user.display_name}")
                    
                await self.client.mutes.delete(user.id)
                
                try:
                    self.client.muted_users.pop(user.id)
                except KeyError:
                    pass
                
    @check_current_mutes.before_loop
    async def before_check_current_mutes(self):
        await self.client.wait_until_ready()            
    
    
    @commands.command(help="Kick command, to kick users. Usage: `%kick @Joniii Insulting` or `%kick @Joniii`")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=nrp):
        if user.id == self.client.user.id:
            embed = discord.Embed(description=":x: Why did you try to kick me? Do you hate me so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user == ctx.author:
            embed = discord.Embed(description=":x: Why do you want to kick yourself? Do you hate yourself so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user.guild_permissions.kick_members:
            embed = discord.Embed(description=":x: You can't kick that member, because he has the permission (`kick_members`).", color=discord.Colour.red())
            return await ctx.send(embed=embed)
                
        embed_kicked_dm = discord.Embed(title=f"You got kicked from {ctx.guild.name}!", description=f"Kicked by: **{ctx.author.mention}**", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)    
        embed_kicked_dm.timestamp=datetime.datetime.utcnow()
          
        try:     
            await user.send(embed=embed_kicked_dm)
        except Exception:
            embed_error = discord.Embed(description=":x: **Cannot send the message to the user, he blocked me or disabled his dms.**", color=discord.Colour.red())
            await ctx.send(embed=embed_error, delete_after=5)
            pass
        
        await ctx.guild.kick(user, reason=reason)
        embed_kicked = discord.Embed(title="Kicked!", description=f"The user {user.mention} got kicked successfully from the server.", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
        embed_kicked.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed_kicked)
        
    @commands.command(aliases=["b"], help="Ban command, to ban users. Usage: `%ban @Joniii He spammed to much`")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=nrp):
        if user.id == self.client.user.id:
            embed = discord.Embed(description=":x: Why did you try to ban me? Do you hate me so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user == ctx.author:
            embed = discord.Embed(description=":x: Why do you want to ban yourself? Do you hate yourself so much?", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        if user.guild_permissions.ban_members:
            embed = discord.Embed(description=":x: You can't ban that member, because he has the permission (`ban_members`).", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        
        embed_banned_dm = discord.Embed(title=f"You got banned from {ctx.guild.name}!", description=f"Banned by: **{ctx.author.mention}**", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
        embed_banned_dm.timestamp = datetime.datetime.utcnow()
        
        try:                        
            await user.send(embed=embed_banned_dm)   
        except Exception:            
            embed_error = discord.Embed(description=":x: **Cannot send the message to the user, he blocked me or disabled his dms.**", color=discord.Colour.red())
            await ctx.send(embed=embed_error, delete_after=5)            
            pass
        
        await ctx.guild.ban(user, reason=reason)
        embed_banned = discord.Embed(title="Banned!", description=f"The user {user.mention} got banned successfully from the server.", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
        embed_banned.timestamp=datetime.datetime.utcnow()
        await ctx.send(embed=embed_banned)
    
    @commands.command(help="Unban command, to unban a user. Usage: `%unban [id] second chance`")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=nrp):
        user = await self.client.fetch_user(int(member))
        
        if user.id == self.client.user.id:
            embed = discord.Embed(description=":x: Why did you try to unban me? I am not banned.", color=discord.Colour.red())
            return await ctx.send(embed=embed)     
        if user == ctx.author:
            embed = discord.Embed(description=":x: Why do you want to unban yourself? You are not banned.", color=discord.Colour.red())
            return await ctx.send(embed=embed)
        
        embed_unbanned_dm = discord.Embed(title=f"You got unbanned from {ctx.guild.name}!", description=f"Unbanned by: **{ctx.author.mention}**", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
        embed_unbanned_dm.timestamp = datetime.datetime.utcnow()

        try:
            await user.send(embed=embed_unbanned_dm)
        except Exception:
            embed_error = discord.Embed(description=":x: **Cannot send the message to the user, he blocked me or disabled his dms.**", color=discord.Colour.red())
            await ctx.send(embed=embed_error, delete_after=5)
            pass
        
        await ctx.guild.unban(user, reason=reason)
        embed_unbanned = discord.Embed(title="Unbanned!", description=f"The user {user.mention} got unbanned successfully from the server.", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
        embed_unbanned.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed_unbanned)
        
    @commands.command(help="Mute command, to mute a user. Usage: `%mute @Joniii 2d Spam` or `%mute @Joniii` (perm)")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time: TimeConverter=None, *, reason=nrp):
        guild = ctx.guild
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await guild.create_role(name="Muted")
            
            for channel in guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False)
            
        try:
            if self.client.muted_users[user.id]:
                usera_embed = discord.Embed(description=f"The user {user.mention} is already muted.", color=discord.Colour.red())
                usera_embed.timestamp = datetime.datetime.utcnow()
                return await ctx.send(embed=usera_embed)
        except KeyError:
            pass
        
        data = {
            '_id': user.id,
            'mutedAt': datetime.datetime.utcnow(),
            'muteDuration': time or None,
            'mutedBy': ctx.author.id,
            'guildId': ctx.guild.id,
        }
        await self.client.mutes.upsert(data)
        self.client.muted_users[user.id] = data
        
        await user.add_roles(role)
        
        if not time:
            muted = discord.Embed(title="Muted!", description=f"The user {user.mention} got permanently muted.", color=discord.Colour.red())
            muted.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=muted)
        else:
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            
            if int(hours):
                hmuted = discord.Embed(title="Muted!", description=f"The user {user.mention} got muted by {ctx.author.id} for {hours} hours, {minutes} minutes and {seconds} seconds.", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
                hmuted.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=hmuted)
            elif int(minutes):
                mmuted = discord.Embed(title="Muted!", description=f"The user {user.mention} got muted by {ctx.author.id} for {minutes} minutes and {seconds} seconds.", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
                mmuted.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=mmuted)
            elif int(seconds):
                smuted = discord.Embed(title="Muted!", description=f"The user {user.mention} got muted by {ctx.author.id} for {seconds} seconds.", color=discord.Colour.red()).add_field(name="Reason:", value=reason, inline=False)
                smuted.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=smuted)
                
        if time and time < 300:
            await asyncio.sleep(time)
            
            if role in user.roles:
                await user.remove_roles(role)
                unmuted = discord.Embed(title="Unmuted!", description=f"You got unmuted in the server {ctx.guild}")
                
                try:
                    await user.send(embed=unmuted)
                except Exception:
                    pass
            
            await self.client.mutes.delete(user.id)
            
            try:
                self.client.muted_users.pop(user.id)
            except KeyError:
                pass
                
        
    @commands.command(description="Unmute command, to unmute users. Usage: `%unmute @Joniii`",)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        guild = ctx.guild
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("Please execute the command again. I am creating at the moment the muted role and synchronice everything.")
            role = await guild.create_role(name="Muted")
            
            for channel in guild.channels:
                return await channel.set_permissions(role, speak=False, send_messages=False)
        
        await self.client.mutes.delete(user.id)
        try:
            self.client.muted_users.pop(user.id)
        except KeyError:
            pass

        if role not in user.roles:
            usern_embed = discord.Embed(description=f"The user {user.mention} is not muted.", color=discord.Colour.red())
            usern_embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=usern_embed)
            return

        await user.remove_roles(role)
        unmuted_dm = discord.Embed(title="Unmuted!", description=f"You got unmuted in the server {ctx.guild}")
        unmuted_dm.timestamp = datetime.datetime.utcnow()
        unmuted = discord.Embed(title="Unmuted!", description=f"The user {user.mention} got successfully unmuted.")
        unmuted.timestamp = datetime.datetime.utcnow()        
        try:
            await user.send(embed=unmuted_dm)
        except Exception:
            pass
              
    
def setup(client):
    client.add_cog(commands_mod(client))
