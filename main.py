import nextcord
from nextcord.ext import commands
from pytube import YouTube
import os
import datetime
bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.slash_command(name='play', description='Play a song from YouTube')
async def play(interaction: nextcord.Interaction, url: str):
    user = interaction.user
    channel = user.voice.channel
    voice = await channel.connect()

    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename="song.mp3")

    def after():
        os.remove("song.mp3")
    voice.play(nextcord.FFmpegPCMAudio("song.mp3"), after=after)

    title = yt.title
    views = yt.views
    thumbnail = yt.thumbnail_url
    pd = yt.publish_date.strftime("%B %d, %Y")
    
    duration = str(datetime.timedelta(seconds=yt.length)).lstrip('0:')
    embed = nextcord.Embed(
        title=f"Joined",
        color=nextcord.Color.blue()
    )
    embed.add_field(name="Views", value=f"{views:,}")
    embed.add_field(name="Duration", value=duration)
    embed.add_field(name="Published in", value=pd)
    embed.add_field(name="Video Title", value=title)
    embed.set_image(url=thumbnail)

    await interaction.response.send_message(embed=embed)
@bot.slash_command(name='leave', description='Leave the voice channel')
async def leave(interaction: nextcord.Interaction):
    voice_channel = nextcord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice_channel.is_connected():
        await voice_channel.disconnect()
bot.run('bot-token')
