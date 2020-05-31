import os
import discord
import random
import copy
from dotenv import load_dotenv

# 45 civs
civList = [
    "America",
    "Arabia",
    "Australia",
    "Aztec",
    "Brazil",
    "Canada",
    "China",
    "Cree",
    "Netherlands",
    "Egypt",
    "England",
    "Ethiopia",
    "France",
    "Georgia",
    "German",
    "Gran Colombia",
    "Greece",
    "Hungary",
    "Inca",
    "India",
    "Indonesia",
    "Japan",
    "Khmer",
    "Kongo",
    "Korea",
    "Macedon",
    "Mali",
    "Maori",
    "Mapuche",
    "Maya",
    "Mongolia",
    "Norway",
    "Nubia",
    "Ottoman",
    "Persia",
    "Phoenicia",
    "Poland",
    "Rome",
    "Russia",
    "Scotland",
    "Scythia",
    "Spain",
    "Sumeria",
    "Sweden",
    "Zulu"
]

load_dotenv()

def draft_civ(taken):
    civ = random.choice(civList)
    print("drafted: " + civ)
    print("taken: " + str(taken))
    if civ in taken:
        print(civ + " already taken.")
        return draft_civ(taken)
    return civ


client = discord.Client()

@client.event
async def on_message(message):
    guild = message.guild
    print("Guild: " + str(guild.id))

    message.content = message.content.lower()
    if message.author == client.user:
        return
    if message.content.startswith("!draftme"):
        message_content = message.content.split(" | ")
        print(message_content)

        drafted = []
        taken = []

        if len(message_content) < 2:
            message_content.append(3)

        for i in range(0, int(message_content[1])):
            pick = draft_civ(taken)
            drafted.append(pick)
            taken.append(pick)

        reply = "<@" + str(message.author.id) + "> has drafted: "
        for i in range(0, len(drafted)):
            if i == len(drafted) - 2:
                reply = reply + drafted[i] + ", and "
            elif i == len(drafted) - 1:
                reply = reply + drafted[i] + "."
            else:
                reply = reply + drafted[i] + ", "

        await message.channel.send(reply)
        return

    elif message.content.startswith("!draftchannel"):
        message_content = message.content.split(" | ")
        print(message_content)

        if len(message_content) < 2:
            await message.channel.send("Error: Please specify a channel name.")
            return
        else:
            print("Channels: " + str(guild.voice_channels))
            for channel in guild.voice_channels:
                if channel.name.lower() == message_content[1]:
                    voice_channel = copy.copy(channel)

            try:
                voice_channel
            except NameError:
                await message.channel.send("Error: Channel not found.")
                return

        if len(message_content) < 3:
            message_content.append(3)
        else:
            message_content[2] = int(message_content[2])

        players = copy.copy(voice_channel.members)
        print("Players: " + str(players))

        if len(players) == 0:
            await message.channel.send("Error: Channel empty.")
            return

        taken = []
        player_drafts = []

        for player in players:
            player_drafts.append([])

        print(player_drafts)

        for draft_count in range(message_content[2]):
            for player_count in range(len(players)):
                pick = draft_civ(taken)
                player_drafts[player_count].append(pick)
                taken.append(pick)

        reply = "Draft Results:\n"
        for index, player in enumerate(player_drafts):
            reply = reply + "<@" + str(players[index].id) + "> drafted: "
            for i in range(len(player)):
                if i == len(player) - 2:
                    reply = reply + player[i] + ", and "
                elif i == len(player) - 1:
                    reply = reply + player[i] + ".\n"
                else:
                    reply = reply + player[i] + ", "

        await message.channel.send(reply)

        print(player_drafts)

        return

client.run(os.getenv('DISCORD_TOKEN'))
