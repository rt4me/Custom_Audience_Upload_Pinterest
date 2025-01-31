import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.upload_to_pinterest import UploadToPinterest

# @pytest.fixture(scope="function")
# def driver():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.maximize_window()
#     yield driver  # Test runs here
#     driver.quit()  # Cleanup after test

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Pass the WebDriver instance to the page object
upload_page = UploadToPinterest(driver)
upload_page.upload_to_pinterest()
