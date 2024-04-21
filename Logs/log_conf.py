import logging
import os
from datetime import datetime

# Get the current time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Specify the filename
log_name = f"Log_{current_time}"

current_script_directory = os.path.dirname(os.path.abspath(__file__))
full_file_path = os.path.join(current_script_directory, log_name)

# Configure the logger
logging.basicConfig(level=logging.INFO)  # Adjust level as needed
logger = logging.getLogger(__name__)
