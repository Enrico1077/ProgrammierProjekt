""" this file provides global configuration for logging """

import logging

def setup_logging():
    """this function configures the logger """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
