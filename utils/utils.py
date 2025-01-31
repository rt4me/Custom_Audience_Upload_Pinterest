import logging
import time
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ColoredFormatter(logging.Formatter):
    # Define color codes
    COLORS = {
        'DEBUG': '\033[94m',   # Blue
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[95m' # Magenta
    }
    RESET = '\033[0m'  # Reset to default color

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{self.RESET}"



class Utilities(metaclass=Singleton):

    def __init__(self):
        self.logger = self.create_logger()

    @staticmethod
    def create_logger():
        # Create Logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Check if logger already has handlers to prevent duplicate logs
        if not logger.handlers:
            # Create Console Handler or file handler and set log level
            ch = logging.StreamHandler() #Directs log messages to the Console
            fh = logging.FileHandler("../logs/FileHandler_logging.log") # Directs log messages to a file.

            # Create formatter to output in specific colors and information.
            formatter_with_color = ColoredFormatter(
                '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s')
            formatter_plain = logging.Formatter(
                '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s')

            # Add formatter to console or file handler
            ch.setFormatter(formatter_with_color)
            fh.setFormatter(formatter_plain)

            # Add console handler to logger
            logger.addHandler(ch)
            logger.addHandler(fh)

        return logger

    # @staticmethod
    # def og_logger(log_level=logging.DEBUG):
    #     logger = logging.getLogger(__name__)
    #     logger.setLevel(log_level)
    #     return logger

def wait_for_file_stability(file_path, wait_time=2, max_attempts=10):
    """
    Wait until the file is present and stable (not changing in size).

    :param file_path: Path to the file to monitor.
    :param wait_time: Time in seconds between size checks.
    :param max_attempts: Maximum number of checks before giving up.
    :return: True if the file is stable and ready to use, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"Waiting for file to be created: {file_path}")

    # Wait until the file is created
    while not os.path.exists(file_path):
        time.sleep(wait_time)

    print(f"File created: {file_path}")
    last_size = -1
    attempts = 0

    # Wait until the file size is stable
    while attempts < max_attempts:
        current_size = os.path.getsize(file_path)
        if current_size == last_size:
            return True
        last_size = current_size
        time.sleep(wait_time)
        attempts += 1

    return False
