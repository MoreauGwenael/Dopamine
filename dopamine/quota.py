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

    def refresh_quota(self):
        logging.info(f'[Quota] Refreshing quota for {self.discord_user}')
        if self.quota_remaining < self.start_quota and not self.muted:
            self.quota_remaining += 1

        # Add one credit every 1800s == 30min
        threading.Timer(int(os.getenv('REFRESH_QUOTA_TIMER', 1800)), self.refresh_quota).start()

    def use_quota(self):
        if self.quota_remaining > 0:
            self.quota_remaining = self.quota_remaining - 1
            logging.info(f'[Quota] {self.quota_remaining} quota(s) remaining for {self.discord_user}!')
            return True
        else:
            # No quota ...
            return False

    def reset_quota(self):
        self.quota_remaining = self.start_quota
