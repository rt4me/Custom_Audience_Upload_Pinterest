from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
from pages.base_page import BasePage
from utils.utils import Utilities
import utils.config as conf
import choreo_login

log = Utilities.create_logger()

class UploadToPinterest(BasePage):

    PINTEREST_LOGIN_BUTTON_ELEMENT = (By.XPATH, "//div[contains(text(),'Log in')]")
    PINTEREST_LOGIN_CONT_W_GOOGLE_BUTTON_ELEMENT = (By.XPATH, "//span[contains(text(), 'Continue with Google')]")
    ADD_ACCOUNT_OVERVIEW_ELEMENT = (By.XPATH, "//h1[normalize-space()='Ad account overview']")
    AUDIENCE_SELECTION_ELEMENT = (By.XPATH, "//div[contains(text(),'Audiences')]")
    CREATE_AUDIENCE_BUTTON_ELEMENT = (By.XPATH, "//button[@name='createAudienceButton']")
    CUSTOMER_LIST_SELECTION_ELEMENT = (By.XPATH, "//label[@for='CUSTOMER_LIST']")
    AUDIENCE_NAME_BOX_ELEMENT = (By.ID, "audienceName")
    AUDIENCE_DESC_BOX_ELEMENT = (By.ID, "audienceDescription")
    SUBMIT_FILE_BUTTON_ELEMENT = (By.XPATH, "//button[@data-test-id='submitFile']")
    CONFIRM_SUBMIT_FILE_BUTTON_ELEMENT = (By.XPATH, "//button[@type='submit']")
    SUCCESS_MESSAGE_ELEMENT = (By.XPATH, "//success-message-locator")

    def __init__(self):
        super().__init__()

    def upload_to_pinterest(self):
        log.debug(f"Using URL: {conf.BASE_URL}")
        log.debug(f"Driver type: {type(self.driver)}")
        self.driver.get(conf.BASE_URL)

        log.debug(f"Window Handles: {self.driver.window_handles}")
        log.info("Logging into Pinterest")
        self.click(self.PINTEREST_LOGIN_BUTTON_ELEMENT)
        self.click(self.PINTEREST_LOGIN_CONT_W_GOOGLE_BUTTON_ELEMENT)
        log.debug(f"Window Handles: {self.driver.window_handles}")

        log.info("Call choreo_login.choreo_authentication")
        choreo_login.ChoreoLogin.perform_login()

        print("On Next screen, probably need to select the Resend Code option to get a new verification number.")
        print("Then manually select Continue")

        #Switch back to main window
        WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(1))
        log.debug("Switching back to Main window.")
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Navigate to the Create Audience page
        log.info("Navigating to Create Audience page via menus.")
        self.click(self.ADD_ACCOUNT_OVERVIEW_ELEMENT)
        self.click(self.AUDIENCE_SELECTION_ELEMENT)
        self.click(self.CREATE_AUDIENCE_BUTTON_ELEMENT)

        # Select "Customer list"
        log.info("Selecting Customer List option")
        self.click(self.CUSTOMER_LIST_SELECTION_ELEMENT)

        # Fill in the Audience name and description
        log.info(f"Filling in audience name as {conf.AUDIENCE_NAME_FOR_PINTEREST}")
        self.enter_text(self.AUDIENCE_NAME_BOX_ELEMENT,conf.AUDIENCE_NAME_FOR_PINTEREST)
        log.info("Filling in description.")
        self.enter_text(self.AUDIENCE_DESC_BOX_ELEMENT,conf.AUDIENCE_DESCRIPTION_FOR_PINTEREST)


        # Click on the Choose file button and give file location
        log.info("Selecting file to upload from ")
        self.click(self.SUBMIT_FILE_BUTTON_ELEMENT)
        file_path = fr"{conf.LOCAL_DIRECTORY}{conf.DOWNLOAD_FILENAME}"
        log.debug(f"Full file path being used: {file_path}")



        log.debug("Using code from Creative Studio AI Chat")
        # Click the button to open the file dialog
        # file_input.click()

        # Give the OS some time to open the file dialog
        time.sleep(2)  # Adjust as needed

        # Use pyautogui to type the file path and press Enter
        pyautogui.write(file_path)
        pyautogui.press('enter')





        # Click the submit button
        self.click(self.CONFIRM_SUBMIT_FILE_BUTTON_ELEMENT)

        # Optionally, wait for a success message or any indication that the process is complete
        self.wait_for_element(self.SUCCESS_MESSAGE_ELEMENT)

        # Add a sleep time to let the file upload
        time.sleep(10)
        log.info("Closing browser window")
        #driver.quit()


# Call the upload function
# upload_to_pinterest()
def main():
    log.info("Running upload_to_pinterest.py as a standalone program.")
    uploader = UploadToPinterest()
    uploader.upload_to_pinterest()


if __name__ == "__main__":
    main()