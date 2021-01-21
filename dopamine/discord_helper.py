import json
import logging
import os
import threading
from random import randint
from urllib import request


class DiscordHelper:
    def __init__(self):
        self.youtube_token = os.getenv('YOUTUBE_TOKEN')
        self.playlists_id = eval(os.getenv('PLAYLIST_ID'))
        self.videos_ids = None
        self.video_number = None
        self.update_videos()

        self.pinned_messages_updated = False
        self.pinned_messages = []

    def get_random_pinned_message(self):
        return self.pinned_messages[randint(0, len(self.pinned_messages) - 1)]

    async def update_pinned_messages(self, channels):
        if not self.pinned_messages_updated:
            all_pinned_messages = []
            # go through each channel
            for chan in channels:
                # get pins present in this channel
                all_pins = await chan.pins()
                # re-post all the pins
                for pin in all_pins:
                    mat = pin.attachments
                    if len(mat) == 0:
                        # message await message.channel.send(pin.content)
                        self.pinned_messages.append(pin.content)
                    else:
                        # await message.channel.send(mat[0].url)
                        self.pinned_messages.append(mat[0].url)

            self.pinned_messages_updated = True

    def update_videos(self):
        logging.info('Updating video list !')
        self.videos_ids = self.get_all_videos()
        if self.video_number is not None and self.video_number < len(self.videos_ids):
            logging.info(f'{len(self.videos_ids) - self.video_number} added since last refresh.')
        self.video_number = len(self.videos_ids)
        logging.info(f'{self.video_number} dopamine videos available !')
        threading.Timer(1800, self.update_videos).start()

    def get_all_videos(self):
        videos = []

        # Loop in all playlists
        for i in self.playlists_id:
            page_token = ""

            # Loop in all pages
            while True:
                if page_token == "":
                    # First page
                    page = request.urlopen(
                        f'https://www.googleapis.com/youtube/v3/playlistItems?maxResults=1000&part=snippet&playlistId={i}&key={self.youtube_token}')
                else:
                    # Second and more pages
                    page = request.urlopen(
                        f'https://www.googleapis.com/youtube/v3/playlistItems?pageToken={page_token}&maxResults=1000&part=snippet&playlistId={i}&key={self.youtube_token}')

                # Decrypt the json
                result = json.loads(page.read().decode('utf8'))

                # Get all URL from json
                for j in range(len(result["items"])):
                    videos.append(result["items"][j]["snippet"]["resourceId"]["videoId"])

                if "nextPageToken" in result:
                    # If not last page, get the next page token
                    page_token = result["nextPageToken"]
                else:
                    # If last page end the loop
                    break

        return videos

    def get_random_vid(self):
        return self.video_ids[randint(0, len(self.video_ids) - 1)]
