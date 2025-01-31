from selenium import webdriver

class DriverFactory:
    _driver = None

    @staticmethod
    def get_driver():
        if DriverFactory._driver is None:
            DriverFactory._driver = webdriver.Chrome()  # Or any other browser
        return DriverFactory._driver

    @staticmethod
    def quit_driver():
        if DriverFactory._driver:
            DriverFactory._driver.quit()
            DriverFactory._driver = None
