import logging
import os
from datetime import datetime


class LogGen:
    @staticmethod
    def loggen(origin_name='TestSuite'):
        logger = logging.getLogger(origin_name)
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        # Format: logger-01-05-2026_15-30-00-filename.log
        log_file_name = f"logger-{timestamp}-{origin_name}.log"
        filepath = os.path.join(log_dir, log_file_name)

        file_handler = logging.FileHandler(filepath, mode='w')
        # Standard format
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)8s - %(message)s (%(filename)s:%(lineno)d)')
        print(f"Formatter = {formatter}")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        return logger