import random
import string
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)  # 최대 10초 대기 설정

    ''' 로그인 페이지 진입 '''
    def open(self):
        # 로그인하기 버튼 클릭
        login_open_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='로그인하기']")))
        login_open_button.click()


    ''' 이메일 주소 입력 '''
    def login_input_email(self, email):
        # 이메일 입력
        input_email = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        input_email.send_keys(email)
        return input_email


    ''' 비밀번호 입력 '''
    def login_input_password(self, password):
        # 비밀번호 입력
        input_password = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        input_password.send_keys(password)
        return input_password


    ''' 계속하기(로그인) 버튼 클릭 '''
    def login_button_click(self):
        # 로그인 버튼 클릭
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='계속하기']")))
        login_button.click()


    ''' 비밀번호를 잊으셨나요? 클릭 '''
    def forget_password_click(self):
        # 비밀번호를 잊으셨나요? 링크 클릭
        forget_password_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "비밀번호를 잊으셨나요?")))
        forget_password_link.click()


    ''' 비밀번호를 잊으셨나요? 이메일 주소 입력 '''
    def forget_password_input_email(self, email):
        # 이메일 입력
        input_email = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        input_email.send_keys(email)
        return input_email


    ''' 비밀번호를 잊으셨나요? 계속 버튼 클릭 '''
    def forget_password_next_click(self):
        # 계속 버튼 클릭
        next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='계속']")))
        next_button.click()


    ''' 비밀번호를 잊으셨나요? Resend email 버튼 클릭 '''
    def forget_password_resend_email_click(self):
        # Resend email 버튼 클릭
        resend_email_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Resend email']")))
        resend_email_button.click()


    ''' 비밀번호를 잊으셨나요? 로그인 화면으로 돌아가기 클릭 '''
    def forget_password_back_to_login_click(self):
        # 로그인 화면으로 돌아가기 버튼 클릭
        back_login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '로그인 화면으로 돌아가기')]")))
        back_login_button.click()


    ''' 계정이 없으신가요? 회원가입 클릭 '''
    def signup_click(self):
        # 계정이 없으신가요? 회원가입 링크 클릭
        signup_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "회원가입")))
        signup_link.click()

    
    ''' 랜덤 이메일 주소 생성 '''
    def create_random_email(self, email_length):
        # 지정된 길이만큼 소문자 문자열 생성
        random_string = "".join(random.choices(string.ascii_lowercase, k=email_length))
        email = random_string + "_t3@team3ex.com"  # 3팀 테스트용 도메인 생성
        return random_string, email