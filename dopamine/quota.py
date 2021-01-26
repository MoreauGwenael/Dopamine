import logging
import os
import threading


class Quota:
    def __init__(self):
        self.start_quota = os.getenv('START_USER_QUOTA', 5)
        self.quota_remaining = self.start_quota

    def refresh_quota(self):
        if self.quota_remaining < self.start_quota:
            self.quota_remaining += 1

        # Add one credit every 1800s == 30min
        threading.Timer(os.getenv('REFRESH_QUOTA_TIMER', 1800), self.refresh_quota).start()

    def use_quota(self):
        if self.quota_remaining > 0:
            self.quota_remaining = self.quota_remaining - 1
            logging.debug(f'{self.quota_remaining} quota remaining !')
            return True
        else:
            # No quota ...
            return False
