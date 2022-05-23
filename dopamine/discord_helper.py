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
        self.video_ids = None
        self.video_number = None
        self.update_videos()

        self.pinned_messages_updated = False
        self.pinned_messages = []

    # Renvoie un message épinglé aléatoire
    def get_random_pinned_message(self):
        return self.pinned_messages[randint(0, len(self.pinned_messages) - 1)]

    # Met à jour la liste des messages épinglés
    async def update_pinned_messages(self, channels):
        if not self.pinned_messages_updated:
            # Parcoure tous les canaux
            for chan in channels:
                # Récupère les messages épinglés du canal
                all_pins = await chan.pins()
                
                # Ajoute tous les messages épinglés en mémoire
                for pin in all_pins:
                    mat = pin.attachments
                    if len(mat) == 0:
                        # message await message.channel.send(pin.content)
                        self.pinned_messages.append(pin.content)
                    else:
                        # await message.channel.send(mat[0].url)
                        self.pinned_messages.append(mat[0].url)

            self.pinned_messages_updated = True

    # Met à jour la liste des vidéos
    def update_videos(self):
        logging.info('Updating video list !')
        self.video_ids = self.get_all_videos()

        if self.video_number is not None and self.video_number < len(self.video_ids):
            logging.info(f'{len(self.video_ids) - self.video_number} added since last refresh.')
        self.video_number = len(self.video_ids)
        logging.info(f'{self.video_number} dopamine videos available !')

        # Lance le timer de mise à jour des vidéos tous les mois
        threading.Timer(2592000, self.update_videos).start()

    # Récupère toutes les vidéos sur toutes les playlists
    def get_all_videos(self):
        videos = []

        # Parcoure les playlists
        for i in self.playlists_id:
            page_token = ""

            # Parcoure les pages de la playlist
            while True:
                # Récupère la première page
                if page_token == "":
                    page = request.urlopen(
                        f'https://www.googleapis.com/youtube/v3/playlistItems?maxResults=1000&part=snippet&playlistId={i}&key={self.youtube_token}')

                # Récupère la page (deuxième ou plus)
                else:
                    page = request.urlopen(
                        f'https://www.googleapis.com/youtube/v3/playlistItems?pageToken={page_token}&maxResults=1000&part=snippet&playlistId={i}&key={self.youtube_token}')

                # Décrypte le json
                result = json.loads(page.read().decode('utf8'))

                # Récupère toutes les URLs du json
                for j in range(len(result["items"])):
                    videos.append(result["items"][j]["snippet"]["resourceId"]["videoId"])

                # Si la page actuelle n'est pas la dernière, récupère l'URL de la prochaine et boucle
                if "nextPageToken" in result:
                    page_token = result["nextPageToken"]

                # Sinon, quitte la boucle
                else:
                    break

        return videos

    # Renvoie une vidéo aléatoire
    def get_random_vid(self):
        # Réactualise la liste des vidéos si le tiers a été posté
        if len(self.video_ids) < self.video_number/3:
            self.update_videos()

        random_index = randint(0, len(self.video_ids) - 1)
        random_id = self.video_ids[random_index]

        # Supprime l'ID de la vidéo de la liste pour ne pas la reprendre
        logging.info(f'{random_id} removed from the list. It won\'t be picked again')
        self.video_ids.remove(random_id)
        logging.info(f'{len(self.video_ids)} videos remaining !')

        return random_id
