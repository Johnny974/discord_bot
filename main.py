import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from joke_api import get_dad_joke
import yt_dlp

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


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/commands | /vtip | /banger <link> | /stop | /anketa <otázka> "))
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


@bot.command()
async def anketa(ctx, *, question):
    embed = discord.Embed(title="Nová anketa", description=question, color=discord.Color.green())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍🏿")
    await poll_message.add_reaction("👎🏿")


@bot.command()
async def banger(ctx, *, link):
    print("[DEBUG] banger command bol spustený")
    if ctx.author.voice is None:
        print("[DEBUG] User nie je v kanáli")
        await ctx.send("Musíš byť v hlasovom kanáli, aby som ti mohol pustiť hudbu 🎶")
        return

    channel = ctx.author.voice.channel
    print(f"[DEBUG] User je v kanáli: {channel}")
    if ctx.voice_client is None:
        print("[DEBUG] Bot nie je pripojený, pripájam sa...")
        vc = await channel.connect()
        print("[DEBUG] Bot sa pripojil do voice")
    else:
        vc = ctx.voice_client
        print("[DEBUG] Bot už bol pripojený, presúvam...")
        await vc.move_to(channel)
        print("[DEBUG] Bot bol presunutý")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        print("[DEBUG] Sťahujem info z linku...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url2 = info['url']
        print(f"[DEBUG] Načítané info: {info['title']}, stream url získané")
    except Exception as e:
        await ctx.send("❌ Nepodarilo sa načítať pesničku. Skontroluj, či je link správny.")
        print(f"[YT-DLP ERROR] {e}")
        return

    try:
        print("[DEBUG] Stopujem predchádzajúci audio stream (ak nejaký beží)")
        vc.stop()

        print("[DEBUG] Spúšťam FFmpegPCMAudio...")
        vc.play(
            discord.FFmpegPCMAudio(url2),
            after=lambda d: print("[DEBUG] Done callback spustený:", d)
        )
        print("[DEBUG] vc.play bolo zavolané")

        await ctx.send(f"▶️ Teraz hrá: **{info['title']}**")
        print("[DEBUG] Správa o prehrávaní poslaná na text channel")
    except Exception as e:
        print(f"[FFMPEG/VC ERROR] {e}")
        await ctx.send("❌ Nepodarilo sa spustiť prehrávanie.")

    # await ctx.send(f"▶️ Teraz hrá: **{info['title']}**")


@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Hudba zastavená a bot odpojený.")


@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Dostupné príkazy:", description="/vtip \n/anketa <otázka> \n/banger <yt-link> \n/stop")
    await ctx.send(embed=embed)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
