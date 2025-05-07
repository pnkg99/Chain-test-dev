#!/usr/bin/python3.9
import logging
import time

class Logger:
    
    __instance = None
    __log_name = None

    def __init__(self):
        """Don't call this directly. Use Chain.get_instance()."""
        raise RuntimeError('This is a Singleton, invoke get_instance() instead.')

    @classmethod
    def get_instance(cls, verbose=False):
        if cls.__instance is None:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

            cls.__instance = logging.getLogger()
            cls.__instance.setLevel(level=logging.INFO)
            cls.__log_name = f'{timestamp}_chain.log'

            # Avoid duplicate handlers if reused in multiple scripts
            if not cls.__instance.handlers:
                cls._add_file_handler()
                if verbose:
                    cls._add_console_handler()

        return cls.__instance
    
    @classmethod
    def _add_file_handler(cls):
        file_handler = logging.FileHandler(cls.__log_name, mode='w')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        cls.__instance.addHandler(file_handler)

    @classmethod
    def _add_console_handler(cls):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        cls.__instance.addHandler(console_handler)

    @classmethod
    def get_name(cls):
        return cls.__log_name