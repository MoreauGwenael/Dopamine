import logging
from random import randint

import discord

from dopamine.discord_helper import DiscordHelper
from dopamine.quota import Quota

from .tictactoe.board import Board
from .tictactoe.minimax import Minimax


class DopamineClient(discord.Client):
    def __init__(self):
        logging.info('Init discord client')
        self.discord_helper = DiscordHelper()
        self.available_commands_basic = ['!dopamine', '!pinned', '!connard', '!tttcommands']
        self.available_commands_admin = ['!reset', '!tg', '!debaillonnay', '!maintenance', '!op', '!deop']
        self.available_commands_tictactoe = ['!tttshow', '!tttstart', '!tttplay']
        self.admins = ['Shloumpf']
        self.muted = []
        self.mean = [
            'Culé de villageois, tu te crois tout permis ?',
            'Commence par la fermer toi, \'spèce de gueux',
            'C\'est non',
            'Tu te prends pour qui ? Retourne avec la plèbe d\'où tu viens',
        ]
        self.user_quotas = {}
        self.games = {}
        self.ia = Minimax()
        super().__init__()

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name} : {self.user.id}')

    async def on_message(self, message):
        try:
            # Exit si son propre message
            if message.author == self.user:
                return
            
            # Exit si le message ne commence pas par '!'
            if message.content[0] != '!':
                return

            # Si l'user n'est pas connu, le rajoute dans la liste + lui donne ses crédits
            if message.author not in self.user_quotas:
                self.user_quotas[message.author] = Quota(message.author)

            # Commande d'affichage des commandes
            if message.content == '!commands':
                # Affiche les commandes administrateurs + normales
                if message.author.name in self.admins:
                    commands_message = 'Bien sûr maître, les commandes sont ci-dessous, disposez-en à votre guise :\n'
                    for command in self.available_commands_basic:
                        commands_message += f'\t{command}\n'
                    for command in self.available_commands_admin:
                        commands_message += f'\t{command}\n'
                    commands_message += 'Allez, suce-toi quand même'
                # Affiche les commandes normales
                else:
                    commands_message = 'Enculé de Luigi, les commandes à ta disposition sont les suivantes :\n'
                    for command in self.available_commands_basic:
                        commands_message += f'\t{command}\n'
                    commands_message += 'Allez, suce-toi.'
                await message.channel.send(commands_message)

            # Commande d'affichage des commandes du TicTacToe
            if message.content == '!tttcommands':
                commands_message = 'Commandes de jeu :\n\ttttshow -> affiche ta grille\n\ttttstart -> ' \
                                   'lance une nouvelle partie\n\ttttplay #' \
                                   ' -> joue le coup à la case donnée'
                await message.channel.send(commands_message)

            # Si la commande lancée est une commande admin
            if message.content.split()[0] in self.available_commands_admin:
                # Si l'utilisateur est admin
                if message.author.name in self.admins:
                    # Message de prévention d'arrêt du bot
                    if message.content == '!maintenance':
                        await message.channel.send('Le serveur va partir en maintenance, préparez-vous au RIGGED')

                    # Réinitialise les quotas d'un autre utilisateur
                    if message.content.split()[0] == '!reset':
                        if len(message.content.split()) >= 2:
                            target = message.content.split()[1]
                            found = False
                            # Fait le tour des utilisateurs enregistrés pour trouver le bon
                            for user in self.user_quotas.keys():
                                # Si trouvé, appelle la fonction de réinitialisation des crédits
                                if user.name == target:
                                    logging.info('Resetting quota for ' + target)
                                    found = True
                                    self.user_quotas[user].reset_quota()
                                    await message.channel.send('Les quotas de ' + target + ' ont été réinitialisés, deboulonnay now')
                            # Si non-trouvé
                            if not found:
                                await message.channel.send('Utilisateur ' + target + ' non trouvé, faudrait apprendre à écrire')
                        else:
                            await message.channel.send('T\'as pas oublié quelqu\'un toi ?')
                    
                    # Baillonne un utilisateur de toutes les commandes non-admin
                    if message.content.split()[0] == '!tg':
                        if len(message.content.split()) >= 2:
                            target = message.content.split()[1]
                            if target not in self.muted:
                                logging.info('`voice_enable 0` for ' + target)
                                self.muted.append(target)
                            await message.channel.send('TG ' + target)
                        else:
                            await message.channel.send('Avant de vouloir faire taire quelqu\'un, commence par écrire correctement')

                    # Débaillonne un utilisateur des commandes non-admin
                    if message.content.split()[0] == '!debaillonnay':
                        if len(message.content.split()) >= 2:
                            target = message.content.split()[1]
                            if target in self.muted:
                                logging.info('`voice_enable 1` for ' + target)
                                self.muted.remove(target)
                            await message.channel.send('Aller vas-y tu peux parler ' + target)
                        else:
                            await message.channel.send('Désolé y\a pas de /deban all, précise un peu ou j\'te mute')
                    
                    # Ajoute un utilisateur dans la liste des administrateurs
                    if message.content.split()[0] == '!op':
                        if len(message.content.split()) >= 2:
                            target = message.content.split()[1]
                            logging.info('Opped' + target)
                            self.admins.append(target)
                            await message.channel.send(target + ' : --Développement de Âge des châteaux effectué(e)--')
                        else:
                            await message.channel.send('En fait tu sais pas lire les commandes c\'est ça ?')
                    
                    # Supprime un utilisateur de la liste des administrateurs (Attention: auto-suppression activée=)
                    if message.content.split()[0] == '!deop':
                        if len(message.content.split()) >= 2:
                            target = message.content.split()[1]
                            if target in self.admins:
                                logging.info('Deopped' + target)
                                self.admins.remove(target)
                            await message.channel.send(target + ' : Fin des données de la partie')
                        else:
                            await message.channel.send('En fait tu sais pas lire les commandes c\'est ça ?')
                # Si utilisateur non-admin
                else:
                    await message.channel.send(self.mean[randint(0, len(self.mean) - 1)])

            # Si l'utilisateur n'est pas baillonné
            elif message.author.name not in self.muted:
                # Commandes générales
                if message.content in self.available_commands_basic:
                    if self.user_quotas[message.author].use_quota():
                        # Envoie une vidéo aléatoire + suppression dans la liste
                        if message.content == '!dopamine':
                            logging.info('Dopamine request <3')
                            video_id = self.discord_helper.get_random_vid()

                            # Send the randomized URL from videos list
                            await message.channel.send('https://www.youtube.com/watch?v=' + video_id)

                        # Envoie un message épinglé aléatoire (RIGGED activé)
                        if message.content == '!pinned':
                            logging.info('PINNED message requested')
                            channels = message.guild.text_channels
                            await self.discord_helper.update_pinned_messages(channels)
                            await message.channel.send(self.discord_helper.get_random_pinned_message())
                        
                        # Connard -> Enculé
                        if message.content == '!connard':
                            logging.info('Demande insulte')
                            await message.channel.send('Enculé')

                    # Si l'utilisateur n'a plus de crédits
                    else:
                        await message.channel.send('T\'as plus aucun crédit enculé. T\'aurais pas abusé de la dopamine '
                                                   'un peu ? Va falloir attendre, enculé de Luigi.')

                # Commandes du TicTacToe
                if message.content.split()[0] in self.available_commands_tictactoe:
                    # Affiche la grille de l'utilisateur
                    if message.content == '!tttshow':
                        logging.info('Affichage de la grille de ' + message.author.name)
                        if message.author.name in self.games.keys():
                            await message.channel.send(str(self.games[message.author.name]))
                        else:
                            await message.channel.send('Aucune partie en cours, démarre une partie avec la commande '
                                                       '!tttstart')

                    # Démarre une nouvelle partie
                    if message.content == '!tttstart':
                        logging.info('Démarrage d\'une partie pour ' + message.author.name)
                        self.games[message.author.name] = Board()
                        if randint(0, 1) == 1:
                            self.games[message.author.name].insert(0, 0, 'O')
                        await message.channel.send(self.games[message.author.name].__str__())

                    # Joue un coup
                    if message.content.split()[0] == '!tttplay':
                        if message.author.name not in self.games.keys():
                            await message.channel.send('Aucune partie en cours, démarre une partie avec la commande '
                                                       '!tttstart')
                        else:
                            if len(message.content.split()) > 1:
                                if message.content.split()[1].isdigit():
                                    move = int(message.content.split()[1])
                                    if move not in self.games[message.author.name].available_moves:
                                        if 1 <= move <= 9:
                                            await message.channel.send('Tu sais pas lire wesh, la case est déjà prise')
                                        else:
                                            await message.channel.send('Si tu sais pas tirer dans la grille, lève au moins le viseur')
                                    else:
                                        show = True
                                        x, y = 2 - ((move - 1) // 3), (move - 1) % 3
                                        self.games[message.author.name].insert(x, y, 'X')
                                        self.games[message.author.name].available_moves.remove(move)
                                        logging.info(self.games[message.author.name].won()[0])
                                        logging.info(self.games[message.author.name].is_full())
                                        if not (self.games[message.author.name].won()[0] or self.games[message.author.name].is_full()):
                                            show = False
                                            _, ia_move = self.ia.max(self.games[message.author.name], 9)
                                            x, y = ia_move
                                            self.games[message.author.name].insert(x, y, 'O')
                                            self.games[message.author.name].available_moves.remove((2 - x) * 3 + y + 1)
                                            await message.channel.send(self.games[message.author.name].__str__())
                                        if self.games[message.author.name].won()[0]:
                                            if self.games[message.author.name].won()[1] == 'X':
                                                await message.channel.send(self.games[message.author.name].__str__())
                                                await message.channel.send('Wallah t\'as gagné, faudra que je corrige mon code parce que t\'es pas censé y arriver')
                                            else:
                                                await message.channel.send('T\'es claqué au sol')
                                            self.games.pop(message.author.name)
                                        elif self.games[message.author.name].is_full():
                                            if show: await message.channel.send(self.games[message.author.name].__str__())
                                            await message.channel.send('I play zi draw')
                                            self.games.pop(message.author.name)
                                else:
                                    await message.channel.send('https://dessinemoiunehistoire.net/ecriture-chiffres-maternelle/')
                            else:
                                await message.channel.send('T\'as oublié la moitié du message au spawn')

            # Si l'utilisateur est baillonné
            else:
                await message.channel.send('Les noobs ont pas le droit de parler')
        # Si j'ai mal codé <3
        except Exception as e:
            raise e

