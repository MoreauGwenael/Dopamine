import logging
import os
import threading


class Quota:
    def __init__(self, discord_user):
        self.discord_user = discord_user
        self.start_quota = os.getenv('START_USER_QUOTA', 3)
        self.quota_remaining = self.start_quota

    def refresh_quota(self):
        if self.quota_remaining < self.start_quota:
            self.quota_remaining += 1

        # Add one credit every 1800s == 30min
        threading.Timer(os.getenv('REFRESH_QUOTA_TIMER', 1800), self.refresh_quota).start()

    def use_quota(self):
        if self.quota_remaining > 0:
            self.quota_remaining = self.quota_remaining - 1
            logging.info(f'{self.quota_remaining} quota(s) remaining for {self.discord_user}!')
            return True
        else:
            # No quota ...
            return False
