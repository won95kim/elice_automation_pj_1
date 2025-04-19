import random
import string
import json
import re
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# JSON 파일 경로 상수 정의
JSON_PATH = os.path.join(os.getcwd(), "src/resources/testdata/account.json")

class SignupPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)  # 최대 10초 대기 설정

    ''' 회원가입 페이지 진입 '''
    def open(self):
        # 회원가입 버튼 클릭
        signup_open_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='회원가입']")))
        signup_open_button.click()


    ''' 이메일 주소 입력 '''
    def signup_input_email(self, email):
        # 이메일 입력
        input_email_element = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        input_email_element.send_keys(email)
        return input_email_element
    

    ''' 비밀번호 입력 '''
    def signup_input_password(self, password):
        # 비밀번호 입력
        input_password_element = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        input_password_element.send_keys(password)
        return input_password_element


    ''' 계속하기(회원가입) 버튼 클릭 '''
    def signup_button_click(self):
        # 회원가입 버튼 클릭
        signup_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='계속하기']")))
        signup_button.click()


    ''' 이미 계정이 있으신가요? 로그인 클릭 '''
    def have_an_account_login_click(self):
        # 이미 계정이 있으신가요? 로그인 링크 클릭
        login_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "로그인")))
        login_link.click()


    ''' Authorize App Accept 버튼 클릭 (테스트용) '''
    def accept_click(self):
        # Accept 버튼 클릭
        accept_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']")))
        accept_button.click()


    ''' 랜덤 이메일 주소 생성 '''
    def create_random_email(self, email_length):
        # 지정된 길이만큼 소문자 문자열 생성
        random_string = "".join(random.choices(string.ascii_lowercase, k=email_length))
        email = random_string + "_test3@team3exm.com"  # 3팀 테스트용 도메인 생성
        return email


    ''' 랜덤 비밀번호 생성 '''
    def create_random_password(self, password_length):
        # 각 카테고리에서 최소 한 글자 선택
        lower_case = random.choice(string.ascii_lowercase)  # 소문자 랜덤 선택
        upper_case = random.choice(string.ascii_uppercase)  # 대문자 랜덤 선택
        digit = random.choice(string.digits)    # 숫자 랜덤 선택
        punctuation = random.choice(string.punctuation) # 특수문자 랜덤 선택

        # 최소 3개 카테고리 선택
        categories = [lower_case, upper_case, digit, punctuation]
        chosen_categories = random.sample(categories, k=3)

        # 나머지 길이를 소문자로 채움
        remaining_length = password_length - 3
        remaining_characters = random.choices(string.ascii_lowercase, k=remaining_length)

        # 비밀번호 조합 및 문자열로 변환
        password_list = chosen_categories + remaining_characters
        password = ''.join(password_list)
        return password


    ''' 테스트 케이스별 계정 정보 생성 '''
    def setup_test_cases(self, account_num):
        # JSON 파일에서 기존 계정 데이터 로드
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            account = data.get("accounts", [])

        # 테스트용 계정 정보 생성
        valid_email = self.create_random_email(6)   # 유효한 이메일
        unvalid_email = "test"  # 유효하지 않은 이메일
        exist_email = account[0]["email"]   # 이미 존재하는 이메일
        valid_password = self.create_random_password(8) # 유효한 비밀번호
        unvalid_password = "pass"   # 유효하지 않은 비밀번호

        # 테스트 케이스 정의
        TEST_CASES = [
            (valid_email, valid_password, "유효한 이메일과 유효한 비밀번호"),
            (valid_email, unvalid_password, "유효한 이메일과 유효하지 않은 비밀번호"),
            (unvalid_email, valid_password, "유효하지 않은 이메일과 유효한 비밀번호"),
            (unvalid_email, unvalid_password, "유효하지 않은 이메일과 유효하지 않은 비밀번호"),
            (exist_email, valid_password, "이미 존재하는 계정"),
        ]
        return TEST_CASES[account_num][0], TEST_CASES[account_num][1], TEST_CASES[account_num][2]


    ''' 이메일 유효성 검사 '''
    def is_email_valid(self, email):
        # 이메일 형식 정규식 패턴
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email))


    ''' 비밀번호 유효성 검사 '''
    def is_password_valid(self, password):
        if len(password) < 8:   # 최소 길이 확인
            return False
        # 카테고리별 포함 여부 확인
        conditions = [
            bool(re.search(r"[a-z]", password)),  # 소문자
            bool(re.search(r"[A-Z]", password)),  # 대문자
            bool(re.search(r"[0-9]", password)),  # 숫자
            bool(re.search(r"[!@#$%^&*()_+=[\]{}|;:'\",.<>/?]", password))  # 특수 문자
        ]
        return sum(conditions) >= 3 # 최소 3개 이상 포함 여부 확인


    ''' 유효한 계정 정보를 JSON 파일에 저장 '''
    def save_new_account(self, json_name, email, password):
        # JSON 파일에서 기존 계정 데이터 로드
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 새 계정 추가
        new_account = {"email": email, "password": password}
        data[f"{json_name}"].append(new_account)

        # JSON 파일에 저장
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)