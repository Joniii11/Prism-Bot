import discord
import os
import pymongo
import dns
import motor.motor_asyncio
import utils.json_loader

from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from utils.mongo import Document

load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
connection_url = os.getenv('mongo')
#client.connection_url

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

client = commands.Bot(command_prefix=PREFIX, help_command=None, intents=discord.Intents.all())

client.muted_users = {}

@client.event
async def on_ready():
    print("-----\nEingelogt als: {} : {}\n-----\nMeine standart Prefix ist zurzeit: {}\n-----".format(client.user.name, client.user.id, PREFIX))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Prefix: {PREFIX} | For help: {PREFIX}help"))
    
    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(connection_url))
    client.db = client.mongo["prism"]
    client.config = Document(client.db, "config")
    client.mutes = Document(client.db, "mutes")
    
    print("Database init\n-----")
    
    for document in await client.config.get_all():
        print(document)
        
    currentMutes = await client.mutes.get_all()
    for mute in currentMutes:
        client.muted_users[mute["_id"]] = mute
        
    print(client.muted_users)


if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")


client.run(TOKEN, reconnect=True)
