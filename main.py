import time
from loguru import logger
from database.util import create_tables
from bot.util import start_bot
from bot.websocket import start_server


if __name__ == '__main__':
    create_tables()
    # start_bot()
    # logger.info('Wait for start, 5')
    # time.sleep(5)
    start_server()

