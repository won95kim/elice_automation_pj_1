from selenium.webdriver.chrome.webdriver import WebDriver

class MainPage:
    URL = "https://kdt-pt-1-pj-2-team03.elicecoding.com/"

    def __init__(self,driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
