from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import utils.config as conf
from utils.DriverFactory import DriverFactory

class BasePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.wait = WebDriverWait(self.driver, conf.TIMEOUT)


    def click(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    def enter_text(self, by_locator, text):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, by_locator):
        return self.wait.until(EC.visibility_of_element_located(by_locator)).text

    def wait_for_element(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator))

    def switch_window(self,window_identifier):
        self.driver.switch_to.window(window_identifier)  # Switch to the new window

    def scroll_to_bottom_of_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")