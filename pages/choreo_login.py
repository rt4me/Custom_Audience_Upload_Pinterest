from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import Utilities
import utils.config as conf
from pages.base_page import BasePage



log = Utilities.create_logger()

class ChoreoLogin(BasePage):

    GOOGLE_AUTHENTICATOR_CHOREO_EMAIL_ELEMENT = (By.ID, 'identifierId')
    MICROSOFT_CHOREO_EMAIL_ELEMENT = (By.NAME, "loginfmt")
    GOOGLE_AUTHENTICATOR_NEXT_BUTTON_ELEMENT = (By.XPATH, "//span[contains(text(), 'Next')]")
    CHOREO_PASSWORD_ELEMENT = (By.ID, "credentials.passcode")
    WPP_USERNAME_ELEMENT = (By.XPATH, "//span[contains(text(), 'Username')]")
    WPP_LOGIN_NEXT_BUTTON_ELEMENT = (By.XPATH, "//button[contains(text(), 'Next')]")
    CHOREO_LOGIN_CONTINUE_BUTTON = (By.XPATH, "//span[contains(text(), 'Continue')]")

    def __init__(self):
        super().__init__()

    def perform_login(self):
        log.info("Wait for the Authentication window to open and switch to it")

        WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(2))  # Wait until the number of windows is 2
        new_window_handle = self.driver.window_handles[-1]  # Get the handle of the new window
        self.switch_window(new_window_handle)

        log.debug(f"The title of the active window is: {self.driver.title}")
        log.debug(f"The active window handle is: {self.driver.current_window_handle}")


        # Now you can perform actions in the new window
        # Log into new window with Google authentication (Choreo email)
        log.info("Login with Google Authentication")
        log.debug(f"Attempting to find Email and enter {conf.CHOREO_EMAIL}")

        self.enter_text(self.GOOGLE_AUTHENTICATOR_CHOREO_EMAIL_ELEMENT,conf.CHOREO_EMAIL)
        self.click(self.GOOGLE_AUTHENTICATOR_NEXT_BUTTON_ELEMENT)


        #New window opens for Microsoft login (Choreo email)
        log.info("Logging into Microsoft login page")
        log.debug(f"The title of the active window is: {self.driver.title}")
        log.debug(f"The active window handle is: {self.driver.current_window_handle}")

        self.enter_text(self.MICROSOFT_CHOREO_EMAIL_ELEMENT,conf.CHOREO_EMAIL + Keys.RETURN)


        #WPP Sign In (Choreo email pre-populated)
        log.info("WPP login. Email should be pre-populated")
        log.info("Waiting for full page to load")

        #WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Username')]")))
        self.wait_for_element(self.WPP_USERNAME_ELEMENT)
        self.scroll_to_bottom_of_page()
        self.click(self.WPP_LOGIN_NEXT_BUTTON_ELEMENT)

        #WPP password
        log.info("Entering Choreo password automatically (pulled from config.py file)")

        self.enter_text(self.CHOREO_PASSWORD_ELEMENT, conf.CHOREO_PASSWORD + Keys.RETURN)

        #Select Continue
        log.info("Selecting Continue button after Choreo password was entered")

        self.click(self.CHOREO_LOGIN_CONTINUE_BUTTON)

        print("Check phone for Okta validation.")
        return True