import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import random
from joke_api import get_dad_joke
import datetime
import asyncio
from db import init_db, get_highscore, update_highscore
from nasa_api import get_apod_data
import logging


load_dotenv()
# token = os.getenv('DISCORD_TOKEN')
token = os.environ.get("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN nie je načítaný! Skontroluj Environment Variables v Railway.")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

joke_channels = {}


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/commands | /vtip | /ovocko | /ovocko_highscore | /anketa "
                                                         "<otázka>-<možnosť1>-<možnosť2>-... "))
    daily_joke.start()
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.send(f'Vitaj na serveri Dónsky Kozák {member.name}')


random_quotes = ["Počul som slovo kozák? To je veľmi dobre, ja mám kozákov rád.", "Mmmmm, milujem kozákov.",
                 "Za kozákov aj život položím!", "Správny kozák vie ako sa chodí v dvojrade."]


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if ("kozak" in message.content.lower() or "kozák" in message.content.lower() or
            "kozaci" in message.content.lower() or "kozáci" in message.content.lower()):
        await message.channel.send(random.choice(random_quotes))

    await bot.process_commands(message)


@bot.command()
async def vtip(ctx):
    joke = get_dad_joke()
    if joke == "Prepáč, API call na získanie vtipu nefungoval.":
        await ctx.send(f"Sorry {ctx.author.mention}, momentálne neviem získať vtip.")
    else:
        await ctx.send(f"{ctx.author.mention} - Vtip od starého kozáka: {joke}")


@tasks.loop(minutes=1)
async def daily_joke():
    now = datetime.datetime.now()
    if now.hour == 20 and now.minute == 0:
        for guild_id, channel_id in joke_channels.items():
            guild = bot.get_guild(guild_id)
            if not guild:
                continue
            channel = guild.get_channel(channel_id)
            if not channel:
                continue
            joke = get_dad_joke()
            await channel.send(f"Pravidelný vtip od starého kozáka o 20:00: {joke}")
        await asyncio.sleep(60)


@bot.command()
@commands.has_permissions(administrator=True)
async def setvtipkanal(ctx, channel: discord.TextChannel):
    joke_channels[ctx.guild.id] = channel.id
    await ctx.send(f"Nastavený kanál pre denné vtipy o 20:00: {channel.mention}")


@bot.command()
async def anketa(ctx, *, args):
    parts = [x.strip() for x in args.split("-")]
    if len(parts) < 3:
        await ctx.send("Použitie: /anketa otázka-možnosť1-možnosť2-...")
        return

    question = parts[0]
    options = parts[1:]
    if len(options) > 5:
        await ctx.send("Maximálne 5 možností.")
        return

    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    embed = discord.Embed(title="Nová anketa", description=question, color=discord.Color.blue())
    for i, option in enumerate(options):
        embed.add_field(name=emojis[i], value=option, inline=False)

    poll_message = await ctx.send(embed=embed)

    for i in range(len(options)):
        await poll_message.add_reaction(emojis[i])


@bot.command()
async def ovocko(ctx):
    emojis = ["🍒", "🍋", "🍇", "🍉", "⭐", "🍌", "🍆", "🍑", "7️⃣", "🍊"]
    roll = [random.choice(emojis) for _ in range(5)]

    result = " | ".join(roll)
    await ctx.send(f"🎰: {result}")
    fruit_score = 6 - len(set(roll))

    score = roll.count("⭐") * 10 + fruit_score * 5
    if score > 0:
        update_highscore(ctx.guild.id, score)
        await ctx.send(f"🎉 Získal si {score} bodov!")


@bot.command()
async def ovocko_highscore(ctx):
    score = get_highscore(ctx.guild.id)
    embed = discord.Embed(title="Highscore", description=f"Najvyššie dosiahnuté skóre na tomto serveri je: {score}", color=discord.Color.blue())
    await ctx.send(embed=embed)


@bot.command()
async def nasa(ctx):
    data = get_apod_data()
    title = data.get("title", "NASA Picture of the Day")
    explanation = data.get("explanation", "Bez popisu")
    media_type = data.get("media_type", "")
    url = data.get("url", "")

    if len(explanation) > 2000:
        explanation = explanation[:1997] + "..."

    embed = discord.Embed(title=title, description=explanation, color=discord.Color.blue())
    if media_type == "image":
        embed.set_image(url=url)
    else:
        embed.add_field(name="Link", value=f"[Klikni sem]({url})")

    await ctx.send(embed=embed)


@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Dostupné príkazy:", description="/vtip \n/anketa <otázka>-<možnosť1>-<možnosť2>-... "
                                                                 "\n/ovocko \n/ovocko_highscore",
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

if __name__ == "__main__":
    init_db()
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)
