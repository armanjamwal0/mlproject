import logging
import os 
from datetime import datetime 
# any exception happend then we can log that exception in one file that help us to check what happend 

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  # this create a log file name from date 
# log_path = os.path.join(os.getcwd(),'logs',LOG_FILE)
# print(log_path)
logs_dir = os.path.join(os.getcwd(),'logs')

os.makedirs(logs_dir,exist_ok=True)

# print(LOG_FILE)

LOG_FILE_PATH = os.path.join(logs_dir,LOG_FILE)
# print(LOG_FILE_PATH)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format= '[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# if __name__ == '__main__':
#     logging.info('Logging has st')