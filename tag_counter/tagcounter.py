import sys
from gui_app import gui
from console_app import console
from loguru import logger


def tag_counter_main():
    if len(sys.argv) == 1:
        logger.info('Starting a gui app')
        gui()
    else:
        logger.info('Starting a console app')
        console()


if __name__ == '__main__':
    tag_counter_main()
