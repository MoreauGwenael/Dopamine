import logging

import discord

from dopamine.discord_helper import DiscordHelper
from dopamine.quota import Quota


class DopamineClient(discord.Client):
    def __init__(self):
        logging.info('Init discord client')
        self.discord_helper = DiscordHelper()
        self.available_commands = ['!dopamine', '!pinned']
        self.user_quotas = {}
        super().__init__()

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name} : {self.user.id}')

    async def on_message(self, message):
        try:
            # Exit if bot is calling himself
            if message.author == self.user:
                return
            if message.content == '!commands':
                commands_message = 'Enculé de Luigi, les commandes à ta disposition sont les suivantes:\n'
                for command in self.available_commands:
                    commands_message += f'\t{command}\n'
                commands_message += 'Allez, suce toi.'
                await message.channel.send(commands_message)

            if message.content in self.available_commands:
                if message.author not in self.user_quotas:
                    self.user_quotas[message.author] = Quota(message.author)

                if self.user_quotas[message.author].use_quota():
                    # Print random youtube video
                    if message.content == '!dopamine':
                        logging.info('Dopamine request <3')
                        video_id = self.discord_helper.get_random_vid()

                        # Send the randomized URL from videos list
                        await message.channel.send('https://www.youtube.com/watch?v=' + video_id)

                    if message.content == '!pinned':
                        logging.info('PINNED message requested')
                        channels = message.guild.text_channels
                        await self.discord_helper.update_pinned_messages(channels)
                        await message.channel.send(self.discord_helper.get_random_pinned_message())
                else:
                    await message.channel.send('T\'as plus aucun crédit enculé. T\'aurais pas abusé de la dopamine un peu ? Va falloir attendre, enculé de Luigi.')
        except Exception as e:
            raise e
