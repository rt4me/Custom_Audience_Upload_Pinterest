from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import choreo_login
import time
import datetime
from utils import Utilities

log = Utilities.create_logger()



def upload_to_pinterest(filename):
    options = Options()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://ads.pinterest.com/")

    log.debug(f"Window Handles: {driver.window_handles}")
    # Log in to Pinterest
    log.info("Logging into Pinterest")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Log in')]"))).click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Continue with Google')]"))).click()
    log.debug(f"Window Handles: {driver.window_handles}")

    log.info("Call choreo_login.choreo_authentication")
    choreo_login.choreo_authentication(driver)



    print("On Next screen, probably need to select the Resend Code option to get a new verification number.")
    print("Then manually select Continue")

    #Switch back to main window
    log.debug("Switching back to Main window.")
    driver.switch_to.window(driver.window_handles[0])

    # Navigate to the Create Audience page
    log.info("Navigating to Create Audience page via menues.")
    WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.XPATH, "//h1[normalize-space()='Ad account overview']"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Audiences')]"))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create audience')]"))).click()

    # Select "Customer list"
    log.info("Selecting Customer List option")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='CUSTOMER_LIST']"))).click()

    # Fill in the Audience name and description
    log.info(f"Filling in audience name as {AUDIENCE_NAME}")
    driver.find_element(By.ID, "audienceName").send_keys(AUDIENCE_NAME)
    log.info("Filling in description.")
    driver.find_element(By.ID, "audienceDescription").send_keys("Uploaded file from GCP via Selenium.")

    # Click on the Choose file button and give file location
    # driver.find_element(By.XPATH, "//button[@data-test-id='submitFile']").send_keys("files/GCP_Downloaded_file.csv")
    log.info("Selecting file to upload from ")
    file_input = driver.find_element(By.XPATH, "//button[@data-test-id='submitFile']")
    file_path = fr"D:\Python_Projects\Custom_Audience_Upload\files\{filename}"
    file_input.send_keys(file_path)

    # Click the submit button
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Optionally, wait for a success message or any indication that the process is complete
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//success-message-locator")))

    # Add a sleep time to let the file upload
    time.sleep(10)
    log.info("Closing browser window")
    #driver.quit()


# Call the upload function
# upload_to_pinterest()
def main():
    log.info("Running upload_to_pinterest.py as a standalone program.")
    upload_to_pinterest("GCP_Downloaded_file_20250128_113413.csv")


if __name__ == "__main__":
    main()