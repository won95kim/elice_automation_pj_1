import pytest
import logging
import time
import json
import random
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.pages.mainpage import MainPage
from src.pages.signup_page import SignupPage
from src.pages.welcome_page import WelcomePage
from src.pages.login_page import LoginPage
from src.utils.helpers import Utils

# XPath 상수 정의
TEAM_DROPDOWN_XPATH = "//button[@role='combobox' and @aria-expanded='true']"
SELECT_TEAM_XPATH = "//span[@style='pointer-events: none;']"

# JSON 파일 경로 상수 정의
JSON_PATH = os.path.join(os.getcwd(), "src/resources/testdata/account.json")

# 테스트 데이터 정의
NAME = "QA1_3팀_테스터"
TEAM = ["개발 1팀", "개발 2팀", "디자인 1팀", "디자인 2팀"]
TASTE = ["단 맛", "짠 맛", "매운 맛"]
LIKE_UNLIKE = ["pros", "cons"]

''' 공통 데이터 셋팅 '''
@pytest.fixture
def setup(driver, request):
    # 로그 및 스크린샷 설정
    PAGE_NAME = "test_scenario-001"
    FUNC_NAME = request.node.name
    REPORT = Utils.utils_reports_setting(PAGE_NAME, FUNC_NAME)
    # 공통 모듈
    main_page = MainPage(driver)
    signup_page = SignupPage(driver)
    welcome_page = WelcomePage(driver)
    login_page = LoginPage(driver)
    wait = ws(driver, 10)
    return REPORT, main_page, signup_page, welcome_page, login_page, wait


''' scenario-001 회원가입 후 인적사항 작성 제출한 후에 재로그인 진행 '''
class TestScenario_001:
    def test_create_new_account(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, signup_page, welcome_page, _, wait = setup

        # 랜덤으로 이메일과 비밀번호 생성
        EMAIL = signup_page.create_random_email(4)
        PASSWORD = signup_page.create_random_password(8)
        team_num = random.randrange(4)  # 랜덤 팀 선택
        
        try:
            ''' TC-001 유효한 형식의 이메일 주소, 비밀번호 입력 후 회원가입 진행 확인 '''
            # 메인 페이지 진입
            main_page.open()

            # 메인 페이지 진입 확인
            wait.until(EC.url_contains("signin"))
            assert "signin" in driver.current_url
            logging.info("✔ 메인 페이지 진입 성공")

            # 회원가입 버튼 클릭
            signup_page.open()

            # 회원가입 페이지 진입 확인
            wait.until(EC.url_contains("signup"))
            assert "signup" in driver.current_url
            logging.info("✔ 회원가입 페이지 진입 성공")

            # 이메일과 비밀번호 입력
            input_email_element = signup_page.signup_input_email(EMAIL)
            input_password_element = signup_page.signup_input_password(PASSWORD)

            # 입력값 확인
            assert input_email_element.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 입력 성공: {EMAIL}")
            assert input_password_element.get_attribute("value") == PASSWORD
            logging.info("✔ 비밀번호 입력 성공")

            # 비밀번호 규칙 목록 노출 확인
            password_rules = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ca2e186ce")))
            assert password_rules.is_displayed()
            logging.info("✔ 비밀번호 규칙 목록 노출 성공")

            # 회원가입 버튼 클릭
            signup_page.signup_button_click()
            logging.info("✔ 계속하기 버튼 클릭 완료")

            time.sleep(3)

            # Accept 버튼 클릭
            signup_page.accept_click()

            # 인적사항 입력 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 회원가입 성공! 이메일: {EMAIL}")

            # JSON에 계정 저장
            signup_page.save_new_account("scenario_accounts", EMAIL, PASSWORD)

            # JSON 다시 로드해서 account.json 파일 업데이트
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                accounts = data.get("scenario_accounts", [])

            # JSON 저장 확인
            assert accounts[-1]["email"] == EMAIL and accounts[-1]["password"] == PASSWORD
            logging.info(f"✔ {EMAIL} 계정이 정상적으로 json에 저장되었습니다.")

            ''' TC-002 인적사항 부분 정상 작성 후 인적사항 제출 진행 확인 '''
            # 이름 입력
            input_name_element = welcome_page.welcome_input_name(NAME)

            # 입력값 확인
            assert input_name_element.get_attribute("value") == NAME
            logging.info(f"✔ 이름 입력 성공: {NAME}")

            # 드롭다운 클릭
            welcome_page.click_team_dropdown()

            # 드롭다운 노출 확인
            team_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, TEAM_DROPDOWN_XPATH)))
            assert team_dropdown.is_displayed()
            logging.info("✔ 팀 드롭다운 노출 성공")

            # 팀 옵션 선택
            welcome_page.select_team(team_num + 1)  # HTML에서 1-based 인덱스 사용

            # 선택된 팀 확인
            wait.until(EC.text_to_be_present_in_element((By.XPATH, SELECT_TEAM_XPATH), TEAM[team_num]))
            selected_team = driver.find_element(By.XPATH, SELECT_TEAM_XPATH).text
            assert selected_team == TEAM[team_num]
            logging.info(f"✔ 팀 선택 성공: {TEAM[team_num]}")

            # 단 맛/짠 맛/매운 맛 슬라이더 이동 및 확인
            for taste in TASTE:
                # 슬라이더 이동 실행
                random_move = welcome_page.move_taste_slider(taste)

                # 이동된 슬라이더 값 확인
                slider = driver.find_element(By.XPATH, f"//span[text()='{taste}']/following::span[@role='slider']")
                slider_value = round(float(slider.get_attribute("aria-valuenow")), 1)
                tolerance = round(abs(slider_value - random_move), 1)
                assert tolerance < 0.2   # 오차 범위 0.2까지는 넘어감
                logging.info(f"✔ {taste} 의 슬라이더가 정상 이동되었습니다. 입력된 값: {random_move} / 실제 이동 거리: {slider_value} / 오차 범위: {tolerance}")

            # 좋아요/싫어요 추가 음식 성향 입력
            for like_unlike in LIKE_UNLIKE:
                # 추가 음식 성향 랜덤 입력
                input_text = welcome_page.generate_random_food_preferences()
                input_element = welcome_page.input_taste_preference(like_unlike, input_text)

                # 입력값 확인
                assert input_element.text == input_text
                logging.info(f"✔ {like_unlike} 입력 성공: {input_text}")

            # 제출 버튼 클릭
            welcome_page.click_submit()
            time.sleep(1)

            # 홈 페이지 진입 확인
            title = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='오늘 뭐먹지 ?']")))
            assert title.is_displayed()
            logging.info("✔ 인적사항 제출 성공")

        except NoSuchElementException:
            logging.error("✖ 요소를 찾을 수 없습니다. NoSuchElementException")
            driver.save_screenshot(REPORT)
            raise
        except TimeoutException:
            logging.error("✖ 시간 초과 발생. TimeoutException")
            driver.save_screenshot(REPORT)
            raise
        except Exception as e:
            logging.error(f"✖ 예외 발생: {e}")
            driver.save_screenshot(REPORT)
            raise
        finally:
            logging.info("=" * 50)
            logging.info("회원가입 후 인적사항 작성 제출 테스트 완료")
            logging.info("=" * 50)


    ''' TC-003 기존 계정의 이메일 주소, 비밀번호 입력 후 로그인 진행 확인 '''
    def test_login(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, _, _, login_page, wait = setup

        # JSON 다시 로드해서 account.json 파일 업데이트
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            accounts = data.get("scenario_accounts", [])

        EMAIL = accounts[-1]["email"]
        PASSWORD = accounts[-1]["password"]

        try:
            # 메인 페이지 진입
            main_page.open()

            # 메인 페이지 진입 확인
            wait.until(EC.url_contains("signin"))
            assert "signin" in driver.current_url
            logging.info("✔ 메인 페이지 진입에 성공하였습니다.")

            # 로그인하기 버튼 클릭
            login_page.open()

            # 로그인 페이지 진입 확인
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
            logging.info("✔ 로그인 페이지 진입에 성공하였습니다.")

            # 이메일과 비밀번호 입력
            input_email = login_page.login_input_email(EMAIL)
            input_password = login_page.login_input_password(PASSWORD)

            # 입력값 확인
            assert input_email.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 주소가 정상적으로 입력되었습니다. 이메일 주소: {EMAIL}")
            assert input_password.get_attribute("value") == PASSWORD
            logging.info(f"✔ 비밀번호가 정상적으로 입력되었습니다.")

            # 로그인 버튼 클릭
            login_page.login_button_click()
            logging.info("✔ 계속하기 버튼 클릭 완료")
            time.sleep(1)

            time.sleep(3)

            # 가입한 계정으로 로그인 확인
            title = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='오늘 뭐먹지 ?']")))
            assert title.is_displayed()
            logging.info("✔ 로그인 완료 - 기존 계정, 홈 페이지 진입에 성공하였습니다.")

        except NoSuchElementException:
            logging.error("✖ 요소를 찾을 수 없습니다. NoSuchElementException")
            driver.save_screenshot(REPORT)
            raise
        except TimeoutException:
            logging.error("✖ 시간 초과 발생. TimeoutException")
            driver.save_screenshot(REPORT)
            raise
        except Exception as e:
            logging.error(f"✖ 예외 발생: {e}")
            driver.save_screenshot(REPORT)
            raise
        finally:
            logging.info("=" * 50)
            logging.info("재로그인 테스트 완료")
            logging.info("=" * 50)