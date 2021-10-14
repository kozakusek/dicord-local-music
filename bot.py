import discord 
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv
import os
from discord import FFmpegPCMAudio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FUNNY_MESSAGE = [os.getenv('FUNNY_1'), os.getenv('FUNNY_2')]

MUSIC_PATH = os.getev('MUSIC_PATH')

client = Bot("$")

class Emoji:
    poop = '\U0001F4A9'

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
async def join(ctx: Context) -> bool:
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        return True
    else:
        await ctx.send("You need to be in a voice channel to do that.")
        return False

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

@client.command()
async def play(ctx: Context, filename: str):
    if (ctx.author.voice and (ctx.voice_client or await join(ctx))):
        if filename in os.listdir(MUSIC_PATH):
            ctx.voice_client.play(FFmpegPCMAudio(f'{MUSIC_PATH}/{filename}'))
        else:
            await ctx.send(f"No such file {filename}")

if __name__ == "__main__":
    client.run(TOKEN)

