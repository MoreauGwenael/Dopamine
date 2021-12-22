import logging
from random import randint

import discord

from dopamine.discord_helper import DiscordHelper
from dopamine.quota import Quota


class DopamineClient(discord.Client):
    def __init__(self):
        logging.info('Init discord client')
        self.discord_helper = DiscordHelper()
        self.available_commands_basic = ['!dopamine', '!pinned']
        self.available_commands_admin = ['!reset', '!tg', '!debaillonay', '!maintenance', '!op', '!deop']
        self.admins = ['Shloumpf#6792', 'mesh33#2225']
        self.muted = []
        self.mean = [
            'Culé de villageois, tu te crois tout permis ?',
            'Commence par la fermer toi, \'spèce de gueux',
            'C\'est non',
            'Tu te prends pour qui ? Retourne dans la plèbe',
        ]
        self.user_quotas = {}
        super().__init__()

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name} : {self.user.id}')

    async def on_message(self, message):
        try:
            # Exit if bot is calling himself
            if message.author == self.user or message.content[0] != '!':
                return

            if message.content == '!commands':
                if str(message.author) in self.admins:
                    commands_message = 'Bien sûr maître, les commandes sont ci-dessous, disposez-en à votre guise :'
                    for command in self.available_commands_basic:
                        commands_message += f'\t{command}\n'
                    for command in self.available_commands_admin:
                        commands_message += f'\t{command}\n'
                    commands_message += 'Allez, suces-toi quand même'
                else:
                    commands_message = 'Enculé de Luigi, les commandes à ta disposition sont les suivantes :\n'
                    for command in self.available_commands_basic:
                        commands_message += f'\t{command}\n'
                    commands_message += 'Allez, suces-toi.'
                    await message.channel.send(commands_message)

            if message.author not in self.user_quotas:
                self.user_quotas[message.author] = Quota(message.author)

            if message.content.split()[0] in self.available_commands_admin:
                if str(message.author) in self.admins:
                    if message.content() == '!maintenance':
                        await message.channel.send('Le serveur va partir en maintenance, préparez-vous au RIGGED')

                    if message.content.split()[0] == '!reset':
                        if len(message.content) >= 2:
                            target = message.content.split()[1]
                            if target in self.user_quotas:
                                logging.info('Resetting quota for ' + target)
                                users = list(map(str, self.user_quotas.keys()))
                                real_target = self.user_quotas.keys()[users.index(target)]
                                self.user_quotas[real_target].reset_quota()
                            await message.channel.send('Les quotas de ' + target + ' ont été réinitialisés, deboulonnay now')
                        else:
                            await message.channel.send('T\'as pas oublié quelqu\'un toi ?')
                    
                    if message.content.split()[0] == '!tg':
                        if len(message.content) >= 2:
                            target = message.content.split()[1]
                            if target not in self.muted:
                                logging.info('`voice_enable 0` for ' + target)
                                self.muted.append(target)
                            await message.channel.send('TG ' + target)
                        else:
                            await message.channel.send('Avant de vouloir faire taire quelqu\'un, commence par écrire correctement')

                    if message.content.split()[0] == '!debaillonay':
                        if len(message.content) >= 2:
                            target = message.content.split()[1]
                            if target not in self.muted:
                                logging.info('`voice_enable 1` for ' + target)
                                self.muted.remove(target)
                            await message.channel.send('Aller vas-y tu peux parler ' + target)
                        else:
                            await message.channel.send('Désolé y\a pas de /deban all, précise un peu ou j\'te mute')
                    
                    if message.content.split()[0] == '!op':
                        if len(message.content) >= 2:
                            target = message.contnet.split()[1]
                            logging.info('Opped' + target)
                            self.admins.append(target)
                            await message.channel.send(target + ' : --Développement de Âge des châteaux effectué(e)--')
                        else:
                            await message.channel.send('En fait tu sais pas lire les commandes c\'est ça ?')
                    
                    if message.content.split()[0] == '!deop':
                        if len(message.content) >= 2:
                            target = message.contnet.split()[1]
                            logging.info('Deopped' + target)
                            self.admins.remove(target)
                            await message.channel.send(target + ' : Fin des données de la partie')
                        else:
                            await message.channel.send('En fait tu sais pas lire les commandes c\'est ça ?')
                else:
                    await message.channel.send(self.mean[randint(0, len(self.mean) - 1)])

            elif str(message.author) not in self.muted:
                if message.content in self.available_commands_basic:
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
            else:
                await message.channel.send('Les noobs ont pas le droit de parler')
        except Exception as e:
            raise e
