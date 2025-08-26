import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='#', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.send(f'Vitaj na serveri Dónsky Kozák {member.name}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "kozak" in message.content.lower():
        await message.channel.send(f"Počul som slovo kozák? To je veľmi dobre, ja mám kozákov rád.")

    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
