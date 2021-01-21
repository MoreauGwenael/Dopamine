import logging

import discord

from dopamine.discord_helper import DiscordHelper


class DopamineClient(discord.Client):
    def __init__(self):
        logging.info('Init discord client')
        self.discord_helper = DiscordHelper()
        super().__init__()

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name} : {self.user.id}')

    async def on_message(self, message):
        try:
            # Exit if bot is calling himself
            if message.author == self.user:
                return

            # Print random youtube video
            if message.content == '!dopamine':
                video_id = self.discord_helper.get_random_vid()

                # Send the randomized URL from videos list
                await message.channel.send('https://www.youtube.com/watch?v=' + video_id)

            if message.content == '!pinned':
                channels = message.guild.text_channels
                await self.discord_helper.update_pinned_messages(channels)
                await message.channel.send(self.discord_helper.get_random_pinned_message())

        except Exception as e:
            raise e
