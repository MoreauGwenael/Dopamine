import logging
import os
import threading


class Quota:
    def __init__(self, discord_user):
        self.discord_user = discord_user
        self.start_quota = int(os.getenv('START_USER_QUOTA', 3))
        self.quota_remaining = self.start_quota
        self.muted = False
        self.refresh_quota()

    # Timer régulier d'ajout de crédit
    def refresh_quota(self):
        # Rajoute un crédit si manquant & non-muté
        if self.quota_remaining < self.start_quota and not self.muted:
            logging.info(f'[Quota] Refreshing quota for {self.discord_user}')
            self.quota_remaining += 1

        # Relance un nouveau timer pour s'autoappeler après 1800s (30m)
        threading.Timer(int(os.getenv('REFRESH_QUOTA_TIMER', 1800)), self.refresh_quota).start()

    # Vérifie si crédit disponible, et le consume
    def use_quota(self):
        # Si crédit disponible, en enlève 1 et renvoie True
        if self.quota_remaining > 0:
            self.quota_remaining = self.quota_remaining - 1
            logging.info(f'[Quota] {self.quota_remaining} quota(s) remaining for {self.discord_user}!')
            return True
        # Sinon, renvoie False
        else:
            return False

    # Réinitialise les crédits de l'utilisateur, utilisé par !reset par un admin
    def reset_quota(self):
        self.quota_remaining = self.start_quota
