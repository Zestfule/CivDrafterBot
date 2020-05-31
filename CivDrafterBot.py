import os
import discord
import random
import copy
from dotenv import load_dotenv

# 45 civs
civList = [
    "America (Teddy)",
    "Arabia (Saladin)",
    "Australia (John)",
    "Aztec (Montezuma)",
    "Brazil (Pedro)",
    "Canada (Wilfrid)",
    "China (Qin)",
    "Cree (Poundmaker)",
    "Netherlands (Wilhelmina)",
    "Egypt (Cleopatra)",
    "England (Victoria or Eleanor)",
    "France (Catherine or Eleanor)",
    "Georgia (Tamar)",
    "Germany (Frederick)",
    "Gran Colombia (Simon)",
    "Greece (Pericles or Gorgo)",
    "Hungary (Matthias)",
    "Inca (Pachacuti)",
    "India (Gandhi or Chandragupta)",
    "Indonesia (Gitarja)",
    "Japan (Hojo)",
    "Khmer (Jaravarman)",
    "Kongo (Mvemba)",
    "Korea (Seondeok)",
    "Macedon (Alexander)",
    "Mali (Mansa Musa)",
    "Maori (Kupe)",
    "Mapuche (Lautaro)",
    "Maya (Lady Six Sky)",
    "Mongolia (Genghis)",
    "Norway (Harald)",
    "Nubia (Amanitore)",
    "Ottoman (Suleiman)",
    "Persia (Cyrus)",
    "Phoenicia (Dido)",
    "Poland (Jadwiga)",
    "Rome (Trajan)",
    "Russia (Peter)",
    "Scotland (Robert)",
    "Scythia (Tomyris)",
    "Spain (Philip)",
    "Sumeria (Gilgamesh)",
    "Sweden (Kristina)",
    "Zulu (Shaka)"
]

# Load a separate file with our top secret Discord token.
load_dotenv()


# Define a function that picks a random civ from the main list.
# It takes one argument which is a list of already picked civs.
# If the random civ is in the taken list then call this function again.
# Called a recursive function.
# There would be a bug here where if you drafted all 45 civs it would just go forever.
def draft_civ(taken):
    civ = random.choice(civList)
    print("drafted: " + civ)
    print("taken: " + str(taken))
    if civ in taken:
        print(civ + " already taken.")
        return draft_civ(taken)
    return civ


# Connect to the Discord API
client = discord.Client()

# Listen for the event of a message being sent in a connected Discord server (guild).
@client.event
async def on_message(message):
    # Get the server (guild) that the message was in.
    guild = message.guild

    # Set the message content to all lowercase to avoid capitalization issues.
    message.content = message.content.lower()

    # Is the author of the message this Bot?
    if message.author == client.user:
        # Bail out!  Don't respond to yourself!
        return

    # Check if the message starts with "!draftme".
    if message.content.startswith("!draftme"):
        # If it does, split the message up into a "list" of parts delineated by " | ".
        message_content = message.content.split(" | ")

        # Define these two variables as lists.
        drafted = []
        taken = []

        # Check if the list only has 1 item in it.
        if len(message_content) < 2:
            # If it is, add an item on the end equaling three (3), the default civs to be drafted.
            message_content.append(3)

        # Repeat this for the amount of drafts specified.
        for i in range(int(message_content[1])):
            # Call the recursive function to get the pick.
            pick = draft_civ(taken)
            # Add the pick to the drafted list.
            drafted.append(pick)
            # Add the pick to the taken list, to be passed each time to the function to remove duplicates.
            taken.append(pick)

        # Start building the reply message.
        reply = "<@" + str(message.author.id) + "> has drafted: "
        # Loop through all the draft picks.
        for i in range(len(drafted)):
            # Are we on the second to last item on the list?  If so let's go Oxford Comma!
            if i == len(drafted) - 2:
                reply = reply + drafted[i] + ", and "
            # Are we on the last item?  Stick a nice period on the end.
            elif i == len(drafted) - 1:
                reply = reply + drafted[i] + "."
            # If neither of those are true stick a comma on the end.
            else:
                reply = reply + drafted[i] + ", "

        # Send the fully built reply.
        await message.channel.send(reply)
        # End.
        return

    # Check if the message starts with "!draftchannel".
    elif message.content.startswith("!draftchannel"):
        # If it does, split the message up into a "list" of parts delineated by " | ".
        message_content = message.content.split(" | ")

        # If the list is only one long they didn't specify a channel.
        if len(message_content) < 2:
            # Complain to them.
            await message.channel.send("Error: Please specify a channel name.")
            # Bail out!
            return
        # If they did put a channel.
        else:
            # Go through each of the the voice channels on the server (guild).
            for channel in guild.voice_channels:
                # Does the current channel have the same name as the specified one?
                # Also note: since we lowercased the message, need to lowercase the channel name.
                if channel.name.lower() == message_content[1]:
                    # If it is the one make a copy of the channel object for use later.
                    voice_channel = copy.copy(channel)

            # Try accessing the voice_channel variable.
            # If the previous loop through the channels in the server never found a matching channel
            #   the variable wont actually exist and will throw an error we'll catch.
            try:
                voice_channel
            # Catch the NameError exception if the variable isn't set.
            except NameError:
                # Complain to the user.
                await message.channel.send("Error: Channel not found.")
                # Bail out!
                return

        # Like before, check if they specified an amount of civs to draft.
        if len(message_content) < 3:
            # If they didn't default to three (3).
            message_content.append(3)
        # If they did though.
        else:
            # Convert from the string "3" to the int 3.
            # Probably a bug here if they input something that can't be converted from string to int.
            message_content[2] = int(message_content[2])

        # Copy the users in the channel specified.
        players = copy.copy(voice_channel.members)

        # Check if the list of people in the channel is zero (0).
        if len(players) == 0:
            # Complain if there's no one there.
            await message.channel.send("Error: Channel empty.")
            # Bail out!
            return

        # Declare the lists.
        taken = []
        player_drafts = []

        # Add a list for each player in the channel to the list.
        # This would be a multidimensional list (a list of lists).
        for player in players:
            player_drafts.append([])

        # Do a loop for how many draft picks are required.
        # Doing this by a draft round format instead of just doing each player individually will ensure that each pick
        #   has a balanced pool to pick from.
        for draft_count in range(message_content[2]):
            # For each draft "round" go through each player.
            for player_count in range(len(players)):
                # Get the pick and save it.
                pick = draft_civ(taken)
                # Add the pick to this players list.
                player_drafts[player_count].append(pick)
                # Also add the pick to the taken list to avoid duplicates.
                taken.append(pick)

        # Start building the reply message.
        reply = "Draft Results:\n"
        # Loop through all the players in the list, also keep track of where we are in the list via "index" so we can
        #   align the picks to a specific player.
        for index, player in enumerate(player_drafts):
            # Mention the current player.
            reply = reply + "<@" + str(players[index].id) + "> drafted: "
            # Same as before, only difference being on the last pick we want a linebreak at the end to prettify the
            #   reply.
            for i in range(len(player)):
                if i == len(player) - 2:
                    reply = reply + player[i] + ", and "
                elif i == len(player) - 1:
                    reply = reply + player[i] + ".\n"
                else:
                    reply = reply + player[i] + ", "

        # Send the reply.
        await message.channel.send(reply)

        # And exit.
        return

# Connect to Discord.
client.run(os.getenv('DISCORD_TOKEN'))
