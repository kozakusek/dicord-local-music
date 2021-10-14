import discord 
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv
import os
from logs import setup_logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FUNNY_MESSAGE = [os.getenv('FUNNY_1'), os.getenv('FUNNY_2')]

MUSIC_PATH = "./music"

client = Bot("$")
logger = setup_logging()

class Emoji:
    poop = '\U0001F4A9'

@client.event
async def on_ready():
    logger.info("The DCLMB is ready.")


@client.command()
async def hello(ctx: Context):
    await ctx.send("Hi, have a nice day :)")

@client.event
async def on_message(message: discord.Message):
    if (FUNNY_MESSAGE[0] in message.content.lower() 
        and FUNNY_MESSAGE[1] in str(message.content).lower()):
        await message.add_reaction(Emoji.poop)
    
    await client.process_commands(message)

@client.command(pass_context=True)
async def join(ctx: Context):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to do that.")

@client.command(pass_context=True)
async def leave(ctx: Context) -> bool:
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        return True
    else:
        await ctx.send("I am not in a voice channel.")
        return False

@client.command(pass_context=True)
async def switch(ctx: Context):
    if (ctx.author.voice):
        if (await leave(ctx)):
            await join(ctx)
    else:
        await ctx.send("You need to be in a voice channel to do that.")

@client.command()
async def list(ctx: Context):
    await ctx.send(os.listdir(MUSIC_PATH))

if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except Exception as e:
        logger.error("DCLMD encountered an error. Restarting.")
        logger.error(e)
    