from dotenv import load_dotenv
import os

load_dotenv()

CHOREO_EMAIL = os.getenv("CHOREO_EMAIL")
CHOREO_PASSWORD = os.getenv("CHOREO_PASSWORD")
GCP_CREDENTIALS_JSON = os.getenv("GCP_CREDENTIALS_JSON")

GCP_BUCKET_NAME = "gcp-tb-2025-a1"
GCP_OBJECT_NAME = "subfolder-a1/PINT_EMAIL_50k_GCP.csv"
LOCAL_DIRECTORY = "D:\\Python_Projects\\Custom_Audience_Upload\\files\\"
DOWNLOAD_FILENAME = "GCP_to_PINTEREST_20250129_A1.csv"
AUDIENCE_NAME_FOR_PINTEREST = "GCP_to_PINTEREST_20250129_A1"
AUDIENCE_DESCRIPTION_FOR_PINTEREST = "Test audience source from GCP"
BASE_URL = "https://ads.pinterest.com/"
TIMEOUT = 15