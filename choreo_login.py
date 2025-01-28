from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utils
from utils import Utilities

log = Utilities.create_logger()

def choreo_authentication(driver):

    log.info("Wait for the Authentication window to open and switch to it")
    WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))  # Wait until the number of windows is 2
    new_window_handle = driver.window_handles[-1]  # Get the handle of the new window
    driver.switch_to.window(new_window_handle)  # Switch to the new window
    log.debug(f"The title of the active window is: {driver.title}")
    log.debug(f"The active window handle is: {driver.current_window_handle}")


    # Now you can perform actions in the new window
    # Log into new window with Google authentication (Choreo email)
    log.info("Login with Google Authentication")
    log.debug(f"Attempting to find Email and enter {utils.choreo_email}")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'identifierId'))).send_keys(utils.choreo_email)
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()

    #New window opens for Microsoft login (Choreo email)
    log.info("Logging into Microsoft login page")
    log.debug(f"The title of the active window is: {driver.title}")
    log.debug(f"The active window handle is: {driver.current_window_handle}")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, "loginfmt"))).send_keys(utils.choreo_email + Keys.RETURN)
    #driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()

    #WPP Sign In (Choreo email pre-populated)
    log.info("WPP login. Email should be pre-populated")
    log.info("Waiting for full page to load")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Username')]")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))).click()

    #WPP password
    log.info("Entering Choreo password automatically (pulled from config.txt file)")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "credentials.passcode"))).send_keys(utils.choreo_password + Keys.RETURN)

    #Select Continue
    log.info("Selecting Continue button after Choreo password was entered")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]"))).click()

    print("Check phone for Okta validation.")