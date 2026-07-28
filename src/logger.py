import logging
import os
from datetime import datetime

LOGFILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_file_path = os.path.join(os.getcwd(),"logs",LOGFILE)

os.makedirs(logs_file_path, exist_ok=True)

logging.basicConfig(
    filename=logs_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)",
    level=logging.INFO,)