from google.cloud import storage
import utils
from utils import Utilities
import datetime
import os

log = Utilities.create_logger()

def download_blob(bucket_name, source_blob_name, destination_file_path_and_name):
    """Downloads a blob from the bucket."""
    log.info(f"bucket_name = {bucket_name}, source_blob_name = {source_blob_name}, destination_file_name = {destination_file_path_and_name}")
    json_credentials_path = os.path.join(utils.local_directory, utils.gcp_credentials_json)
    log.info(f"JSON credentials path: {json_credentials_path}")
    # Remove all double quotes from the path
    json_credentials_path = json_credentials_path.replace('"', '')
    log.info(f"Cleaned JSON credentials path: {json_credentials_path}")

    # Verify the JSON file exists and is not empty
    if not os.path.isfile(json_credentials_path):
        log.error(f"JSON credentials file does not exist: {json_credentials_path}")
        return

    if os.path.getsize(json_credentials_path) == 0:
        log.error(f"JSON credentials file is empty: {json_credentials_path}")
        return

    try:
        storage_client = storage.Client.from_service_account_json(json_credentials_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_path_and_name)
        log.info(f"Downloaded {source_blob_name} to {destination_file_path_and_name}.")
    except Exception as e:
        log.error(f"Error occurred while downloading blob: {str(e)}")



def main():
    log.info("Running download_csv.py as a standalone program.")
    # download_file_name = f"GCP_Downloaded_file_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    download_blob(utils.gcp_bucket_name, utils.gcp_object_name, os.path.join(utils.local_directory, utils.file_name))


if __name__ == "__main__":
    main()