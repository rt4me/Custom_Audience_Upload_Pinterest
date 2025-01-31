import download_csv
from pages import upload_to_pinterest

from utils import utils
from utils.utils import *

#NAME_DOWNLOADED_FILE = f"GCP_Downloaded_file_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
# Path to the file
file_path = f"{utils.local_directory}/{utils.file_name}"
log = Utilities.create_logger()



download_csv.download_blob(utils.gcp_bucket_name, utils.gcp_object_name, utils.file_name)

# Wait for the file to be present and stable
if wait_for_file_stability(file_path):
    log.info(f"File downloaded from GCP is stable and ready to use: {utils.local_directory}")
    upload_to_pinterest.upload_to_pinterest(utils.file_name)
else:
    log.info(f"File downloaded from GCP is not stable after waiting. Please check: {utils.local_directory}")
