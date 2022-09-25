import discord
import os

from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


client = commands.Bot(command_prefix=PREFIX, help_command=None, intents=discord.Intents.all())

@client.event
async def on_ready():
    print("-----\nEingelogt als: {} : {}\n-----\nMeine standart Prefix ist zurzeit: {}\n-----".format(client.user.name, client.user.id, PREFIX))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Prefix: {PREFIX} | For help: {PREFIX}help"))
 
if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")


client.run(TOKEN, reconnect=True)
