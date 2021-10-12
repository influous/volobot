import discord
import requests
import json
import os
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
client = Bot("!")

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


def get_metar(station):
    response = requests.get(
        "https://avwx.rest/api/metar/{}".format(station),
        headers={"Authorization": API_KEY},
    )
    response2 = requests.get(
        "https://avwx.rest/api/station/{}".format(station),
        headers={"Authorization": API_KEY},
    )
    metar_raw = json.loads(response.text)["raw"]
    airport_name = json.loads(response2.text)["name"]
    return [metar_raw, airport_name]


@client.command()
async def displayembed(ctx):
    embed = discord.Embed()
    embed.add_field(name="undefined", value="undefined", inline=False)
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    print("My name is {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    msg = message.content
    if msg.startswith("/hi"):
        await message.channel.send("Hello!")

    if msg.startswith("/metar"):
        station = msg.split()[1]
        metar = get_metar(station)
        embedVar = discord.Embed(
            title="METAR for {}".format(metar[1]), description=metar[0], color=0x00FF00
        )
        embedVar.add_field(name="Additional Info", value="Placeholder", inline=False)
        embedVar.add_field(name="Runways In Use", value="Placeholder", inline=False)
        embedVar.set_thumbnail(url="https://i.imgur.com/Vw04Buz.jpeg")
        await message.channel.send(embed=embedVar)

    await client.process_commands(message)


client.run(BOT_TOKEN)
