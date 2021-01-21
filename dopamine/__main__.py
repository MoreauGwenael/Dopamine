import logging
import os

from dopamine.dopamine_client import DopamineClient

if __name__ == '__main__':
    try:
        logging.info('Client starting !')
        DopamineClient().run(os.getenv('DISCORD_TOKEN'))
    except Exception as main_exception:
        logging.exception(f'Unexpected exception on main handler\n-------\n\n{main_exception}\n\n-------')
        raise main_exception
