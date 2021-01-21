import os
import discord
from dotenv import load_dotenv
from urllib import request
import json
from random import randint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN_YOUTUBE = os.getenv('YOUTUBE_TOKEN')
ID_PLAYLISTS = eval(os.getenv('PLAYLIST_ID'))
client = discord.Client()


# Print in CLI when client is connected
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Main function
@client.event
async def on_message(message):
    # Exit if bot is calling himself
    if message.author == client.user:
        return

    # Print random youtube video
    if message.content == '!dopamine':
        videos = []

        # Loop in all playlists
        for i in ID_PLAYLISTS:
            page_token = ""

            # Loop in all pages
            while True:
                if page_token == "":
                    # First page
                    page = request.urlopen('https://www.googleapis.com/youtube/v3/playlistItems?maxResults=1000&part=snippet&playlistId='+i+'&key='+TOKEN_YOUTUBE)
                else:
                    # Second and more pages
                    page = request.urlopen(
                        'https://www.googleapis.com/youtube/v3/playlistItems?pageToken='+page_token+'&maxResults=1000&part=snippet&playlistId='+i+'&key='+TOKEN_YOUTUBE)

                # Decrypt the json
                my_bytes = page.read()
                result_json = my_bytes.decode('utf8')
                result = json.loads(result_json)

                # Get all URL from json
                for j in range(len(result["items"])):
                    videos.append(result["items"][j]["snippet"]["resourceId"]["videoId"])

                if "nextPageToken" in result:
                    # If not last page, get the next page token
                    page_token = result["nextPageToken"]
                else:
                    # If last page end the loop
                    break

        # Send the randomized URL from videos list
        await message.channel.send('https://www.youtube.com/watch?v='+videos[randint(0, len(videos)-1)])

# Run Barry, run !
client.run(TOKEN)

