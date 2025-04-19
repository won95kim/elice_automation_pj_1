import pytest
import logging
import time
import json
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.pages.mainpage import MainPage
from src.pages.signup_page import SignupPage
from src.utils.helpers import Utils

# JSON 파일에서 계정 데이터 로드
JSON_PATH = os.path.join(os.getcwd(), "src/resources/testdata/account.json")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    check_account = data.get("accounts", [])

''' 공통 데이터 셋팅 '''
@pytest.fixture
def setup(driver, request):
    # 로그 및 스크린샷 설정
    PAGE_NAME = "test_signup_page"
    FUNC_NAME = request.node.name
    REPORT = Utils.utils_reports_setting(PAGE_NAME, FUNC_NAME)
    # 공통 모듈
    main_page = MainPage(driver)
    signup_page = SignupPage(driver)
    wait = ws(driver, 10)
    return REPORT, main_page, signup_page, wait


class TestSignupPage:
    ''' [단위] 회원가입 페이지 진입 테스트 '''
    @pytest.mark.skip
    def test_open(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, signup_page, wait = setup

        try:
            # 메인 페이지 진입
            main_page.open()

            # 메인 페이지 진입 확인
            wait.until(EC.url_contains("signin"))
            assert "signin" in driver.current_url
            logging.info("✔ 메인 페이지 진입 성공")

            # 회원가입 버튼 클릭
            signup_page.open()
            time.sleep(1)

            # 회원가입 페이지 진입 확인
            wait.until(EC.url_contains("signup"))
            assert "signup" in driver.current_url
            logging.info("✔ 회원가입 페이지 진입 성공")

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
            logging.info("[단위] 회원가입 페이지 진입 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 이메일 주소와 비밀번호 입력 테스트 '''
    @pytest.mark.skip
    def test_signup_input_email_password(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, signup_page, wait = setup

        # 랜덤으로 이메일과 비밀번호 생성
        EMAIL = signup_page.create_random_email(5)
        PASSWORD = signup_page.create_random_password(8)

        try:
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
            time.sleep(1)

            # 입력값 확인
            assert input_email_element.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 입력 성공: {EMAIL}")
            assert input_password_element.get_attribute("value") == PASSWORD
            logging.info("✔ 비밀번호 입력 성공")

            # 비밀번호 규칙 목록 노출 확인
            password_rules = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ca2e186ce")))
            assert password_rules.is_displayed()
            logging.info("✔ 비밀번호 규칙 목록 노출 성공")

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
            logging.info("[단위] 이메일 주소와 비밀번호 입력 테스트 완료")
            logging.info("=" * 50)


    ''' [통합] 회원가입 테스트 '''
    @pytest.mark.parametrize("account_num", [0, 1, 2, 3, 4])  # 0: 이메일O/비밀번호O, 1: 이메일O/비밀번호X, 2: 이메일X/비밀번호O, 3: 이메일X/비밀번호X, 4: 이미 존재하는 계정
    def test_signup(self, driver: WebDriver, setup, account_num):
        # 공통 데이터 불러오기
        REPORT, main_page, signup_page, wait = setup

        # 가입 정보 가져오기
        EMAIL, PASSWORD, CASE_DESCRIPTION = signup_page.setup_test_cases(account_num)

        try:
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

            # 테스트 케이스 로깅
            logging.info(f"▶▶▶ 테스트 케이스: {CASE_DESCRIPTION}")

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

            # 유효성 검사
            is_email_valid = signup_page.is_email_valid(EMAIL)
            is_password_valid = signup_page.is_password_valid(PASSWORD)

            # 회원가입 결과 확인
            if is_email_valid and is_password_valid:
                logging.info("▶▶ 정상적인 이메일과 비밀번호 조합")
                if check_account[0]["email"] == EMAIL:  # 이미 존재하는 계정
                    # 안내 문구 노출 확인
                    error_message = wait.until(EC.presence_of_element_located((By.ID, "error-element-email"))).text
                    assert "이미 가입된 이메일 주소입니다." in error_message
                    logging.info(f"⚠ 회원가입 실패 - 안내 문구: {error_message}")
                else:  # 유효한 계정
                    # Accept 버튼 클릭
                    signup_page.accept_click()

                    # 인적사항 입력 페이지 진입 확인
                    wait.until(EC.url_contains("welcome"))
                    assert "welcome" in driver.current_url
                    logging.info(f"✔ 회원가입 성공! 이메일: {EMAIL}")

                    # JSON에 계정 저장
                    signup_page.save_new_account("create_accounts", EMAIL, PASSWORD)

                    # JSON 다시 로드해서 account.json 파일 업데이트
                    with open(JSON_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        check_new_account = data.get("create_accounts", [])

                    # JSON 저장 확인
                    assert check_new_account[-1]["email"] == EMAIL and check_new_account[-1]["password"] == PASSWORD
                    logging.info(f"✔ {EMAIL} 계정이 정상적으로 json에 저장되었습니다.")

            else:
                logging.info("▶▶ 비정상적인 이메일 또는 비밀번호 조합")
                if not is_email_valid and is_password_valid:  # 이메일 유효하지 않음
                    # 안내 문구 노출 확인
                    error_message = wait.until(EC.presence_of_element_located((By.ID, "error-element-email"))).text
                    assert "이메일이 유효하지 않습니다." in error_message
                    logging.info(f"⚠ 회원가입 실패 - 안내 문구: {error_message}")
                elif not is_password_valid:  # 비밀번호 유효하지 않음
                    # 안내 문구 노출 확인
                    assert "signup" in driver.current_url
                    logging.info("⚠ 비밀번호 유효하지 않음 - 페이지 이동 없음")

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
            logging.info(f"[통합] 회원가입 테스트 완료 {account_num}")
            logging.info("=" * 50)


    ''' [통합] 이미 계정이 있으신가요? 로그인 클릭 테스트 '''
    @pytest.mark.skip
    def test_have_an_account_login_click(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, signup_page, wait = setup

        try:
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

            # 이미 계정이 있으신가요? 로그인 링크 클릭
            signup_page.have_an_account_login_click()
            time.sleep(1)

            # 로그인 페이지 URL 확인
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
            logging.info("✔ 로그인 페이지 재진입 성공")

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
            logging.info("[통합] 이미 계정이 있으신가요? 로그인 클릭 테스트 완료")
            logging.info("=" * 50)