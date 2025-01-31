from google.cloud import storage
from utils.utils import Utilities
import os
from pages.base_page import BasePage
import utils.config as conf

log = Utilities.create_logger()

class DownloadCsv(BasePage):

    def download_blob(bucket_name, source_blob_name, destination_file_path_and_name):
        """Downloads a blob from the bucket."""
        log.info(f"bucket_name = {bucket_name}, source_blob_name = {source_blob_name}, destination_file_name = {destination_file_path_and_name}")
        json_credentials_path = os.path.join(conf.LOCAL_DIRECTORY, conf.GCP_CREDENTIALS_JSON)
        log.info(f"JSON credentials path: {json_credentials_path}")
        # Remove all double quotes from the path
        json_credentials_path_cleaned = json_credentials_path.replace('"', '')
        log.info(f"Cleaned JSON credentials path: {json_credentials_path_cleaned}")

        # Verify the JSON file exists and is not empty
        if not os.path.isfile(json_credentials_path_cleaned):
            log.error(f"JSON credentials file does not exist: {json_credentials_path_cleaned}")
            return

        if os.path.getsize(json_credentials_path) == 0:
            log.error(f"JSON credentials file is empty: {json_credentials_path_cleaned}")
            return

        try:
            storage_client = storage.Client.from_service_account_json(json_credentials_path_cleaned)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_path_and_name)
            log.info(f"Downloaded {source_blob_name} to {destination_file_path_and_name}.")
        except Exception as e:
            log.error(f"Error occurred while downloading blob: {str(e)}")



def main():
    log.info("Running download_csv.py as a standalone program.")
    # download_file_name = f"GCP_Downloaded_file_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    DownloadCsv.download_blob(conf.GCP_BUCKET_NAME, conf.GCP_OBJECT_NAME, os.path.join(conf.LOCAL_DIRECTORY, conf.DOWNLOAD_FILENAME).replace('"', ''))


if __name__ == "__main__":
    main()