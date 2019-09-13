import sys
from tag_counter.gui_app import gui
from tag_counter.console_app import console
from loguru import logger


def main():
    if len(sys.argv) == 1:
        logger.info('Starting a gui app')
        gui()
    else:
        logger.info('Starting a console app')
        console()
