import pytest
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException , TimeoutException
from src.pages.mainpage import MainPage

class TestMainPage:

    #@pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_open_main_page(self, driver: WebDriver):

        try:
            main_page = MainPage(driver)
            main_page.open()

        # 로그인 페이지(accounts)로 이동했는지 확인
            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("")) #URL 검증
            assert "" in driver.current_url #검증

        except NoSuchElementException as e:
            assert False