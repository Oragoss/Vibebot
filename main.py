from config import *
import random
import discord
from discord.ext import commands
import youtube_dl

TOKEN = token
GUILD = guild

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="?", intents=intents)

#https://www.youtube.com/watch?v=ml-5tXRmmFk
#https://www.youtube.com/watch?v=jHZlvRr9KxM&t=296s
#http://unicode.org/emoji/charts/full-emoji-list.html


@client.command(name="play", help="play from a random radio. play <url> play the specific song/video from YouTube")
async def play(ctx, url: str = ""):
    # song_there = os.path.isfile("song.mp3")
    # try:
    #     if song_there:
    #         os.remove("song.mp3")
    # except PermissionError:
    #     await ctx.send("Wait for the current playing music to end or use the 'stop' command")
    #     return
    default_channels = [
        "https://www.youtube.com/watch?v=DWcJFNfaw9c",
        "https://www.youtube.com/watch?v=5qap5aO4i9A",
        "https://www.youtube.com/watch?v=tCs48OFv7xA"
    ]
    if not url:
        url = random.choice(default_channels)

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    # voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    await ctx.send("▶ Playing...")

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    ydl_opts = {'format': 'bestaudio/best'}
    # ydl_opts = {
    #     'format': 'bestaudio/best',
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192',
    #     }],
    # }
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([url])
    # for file in os.listdir("./"):
    #     if file.endswith(".mp3"):
    #         os.rename(file, "song.mp3")
    # voice.play(discord.FFmpegPCMAudio("song.mp3"))

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
        ctx.voice_client.play(source)


@client.command(name="leave", help="I will leave the voice chat.")
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        goodbye_message = ["Later 🤘", "Peace out ✌", "Bye! 👋"]
        await ctx.send(random.choice(goodbye_message))
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command(name="pause", help="Pause the current song.")
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("⏸ Paused")
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command(name="resume", help="Resume the current song.")
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("⏯ Resumed")
    else:
        await ctx.send("The audio is not paused.")


@client.command(name="stop", help="This will stop the song I am currently playing.")
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("⏹ I have stopped the song, you'll need to tell me what song you'll want to play next.")


# @client.command()
# async def instruction(ctx):
#     member = ctx.auther
#     print(ctx.auther)
#     await member.create_dm()
#     await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!\n Here are a list of my commands:')
#     await member.dm_channel.send('!play, play from a random radio.')
#     await member.dm_channel.send('!play <youtube url here>, play the specific song from YouTube.')
#     await member.dm_channel.send('!stop, this will stop the song Vibe Bot is currently playing.')
#     await member.dm_channel.send('!pause, pause the current song.')
#     await member.dm_channel.send('!resume, continue the paused song.')


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print("=============================")
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    print(f'{client.user} is ready!')
    print("=============================")

    # for member in guild.members:
    #     # members = '\n - '.join([member.name for member in guild.members])
    #     print(f'Guild Members:\n - {member.name}')


@client.event
async def on_member_join(member):
    print(f'{member}')
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!\n Here are a list of my commands:')
    await member.dm_channel.send('!play, play from a random radio.')
    await member.dm_channel.send('!play <youtube url here>, play the specific song from YouTube.')
    await member.dm_channel.send('!stop, this will stop the song Vibe Bot is currently playing.')
    await member.dm_channel.send('!pause, pause the current song.')
    await member.dm_channel.send('!resume, continue the paused song.')
    await member.dm_channel.send('!leave, I will leave the voice chat.')


client.run(TOKEN)
