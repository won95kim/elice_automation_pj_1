import time
import os
import logging
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL = "https://kdt-pt-1-pj-2-team03.elicecoding.com/signin"

class Utils:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)

    # 자동 로그인
    def utils_login(self, email, password):

        # 메인 페이지 진입
        self.driver.get(URL)
        self.wait.until(EC.url_contains(("signin")))

        # 로그인하기 버튼 클릭
        login_open_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='로그인하기']")))
        login_open_button.click()

        self.wait.until(EC.url_contains(("login")))

        # 이메일 주소/비밀번호 입력
        input_email = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        input_email.send_keys(email)
        input_password = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        input_password.send_keys(password)

        # 계속하기 버튼 클릭
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='계속하기']")))
        login_button.click()

        self.wait.until(EC.url_contains("")) #URL 검증
        assert "" in self.driver.current_url #검증
    
    #네비게이션 바 클릭
    def utils_nevigationbar(self,text):
        nev_btn = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[text()='{text}']")))
        nev_btn.click()
    

    # 로그, 스크린샷 설정
    def utils_reports_setting(page_name, func_name):
        LOG_DIR = f"reports/logs/{page_name}"
        SCREENSHOT_DIR = f"reports/screenshots/{page_name}"

        # 폴더 없을 시 생성
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

        # 로깅 설정
        logger = logging.getLogger()

        # 핸들러를 매번 초기화하고 새로 추가
        logger.handlers.clear()

        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(f"{LOG_DIR}/{page_name}.log", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"))
        logger.addHandler(file_handler)

        # 스크린샷 설정
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = os.path.join(SCREENSHOT_DIR, f"{timestamp}_{func_name}.jpg")

        return screenshot_name

    # 맨위에 <- 버튼 누르기 (이전으로 돌아가기)
    def go_back(self):
        svg_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg.rounded-full.cursor-pointer")))
        svg_element.click()

    # 수정 또는 후기 작성 도중에 X눌러서 종료하기
    def edit_cancel(self):
        cancel = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'cursor-pointer') and contains(@class, 'text-2xl')]")))
        cancel.click()