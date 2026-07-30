import logging
import os 
from datetime import datetime 
# any exception happend then we can log that exception in one file that help us to check what happend 

LOG_FILE = f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'  # this create a log file name from date 
log_path = os.path.join(os.getcwd(),'logs',LOG_FILE)
os.makedirs(log_path,exist_ok=True)


LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE,
    format= '[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

# if __name__ == '__main__':
#     logging.info('Logging has st')