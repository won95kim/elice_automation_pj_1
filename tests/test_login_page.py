import pytest
import json
import time
import logging
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.pages.mainpage import MainPage
from src.pages.login_page import LoginPage
from src.utils.helpers import Utils

# accounts.json에서 계정 정보 가져오기
JSON_PATH = os.path.join(os.getcwd(), "src/resources/testdata/account.json")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    account = data.get("accounts", [])

''' 공통 데이터 셋팅 '''
@pytest.fixture
def setup(driver, request):
    # 로그 및 스크린샷 설정
    PAGE_NAME = "test_login_page"
    FUNC_NAME = request.node.name
    REPORT = Utils.utils_reports_setting(PAGE_NAME, FUNC_NAME)
    # 공통 모듈
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    wait = ws(driver, 10)
    return REPORT, main_page, login_page, wait


class TestLoginPage:
    ''' [단위] 로그인 페이지 진입 테스트 '''
    @pytest.mark.skip
    def test_open(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

        try:
            # 메인 페이지 진입
            main_page.open()

            # 메인 페이지 진입 확인
            wait.until(EC.url_contains("signin"))
            assert "signin" in driver.current_url
            logging.info("✔ 메인 페이지 진입에 성공하였습니다.")

            # 로그인하기 버튼 클릭
            login_page.open()
            time.sleep(1)

            # 로그인 페이지 진입 확인
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
            logging.info("✔ 로그인 페이지 진입에 성공하였습니다.")

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
            logging.info("[단위] 로그인 페이지 진입 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 이메일 주소와 비밀번호 입력 테스트 '''
    @pytest.mark.skip
    def test_input_email_password(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

        # 테스트용 계정 정보 가져오기
        EMAIL = account[0]["email"]
        PASSWORD = account[0]["password"]

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
            time.sleep(1)

            # 입력값 확인
            assert input_email.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 주소가 정상적으로 입력되었습니다. 이메일 주소: {EMAIL}")
            assert input_password.get_attribute("value") == PASSWORD
            logging.info(f"✔ 비밀번호가 정상적으로 입력되었습니다.")

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


    ''' [통합] 로그인 기능 테스트 '''
    @pytest.mark.parametrize("account_num", [0, 1, 2, 3])  # 0: 기존 계정, 1: 처음 접속 계정, 2: 유효하지 않은 계정, 3: 유효하지 않은 형식 계정
    def test_login(self, driver: WebDriver, setup, account_num):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

        # 테스트용 계정 정보 가져오기
        random_string, random_email = login_page.create_random_email(3)
        ACCOUNT_TYPE = account[account_num]["type"]
        EMAIL = account[account_num]["email"]
        PASSWORD = account[account_num]["password"]
        # 차단을 막기위한 random 생성
        if account_num == 2:
            EMAIL = random_email
        if account_num == 3:
            EMAIL = random_string

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

            time.sleep(3)

            # 로그인 결과 확인
            if ACCOUNT_TYPE == "True":
                logging.info("▶▶ 유효한 계정 로그인")
                if account_num == 1:
                    assert "welcome" in driver.current_url # 인적사항 작성 페이지 진입 확인
                    logging.info("✔ 로그인 완료 - 처음 접속한 계정, 인적사항 작성 페이지 진입에 성공하였습니다.")
                else:   # 홈 페이지 진입 확인
                    title = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='오늘 뭐먹지 ?']")))
                    assert title.is_displayed()
                    logging.info("✔ 로그인 완료 - 기존 계정, 홈 페이지 진입에 성공하였습니다.")
            else:
                logging.info("▶▶ 유효하지 않은 계정 로그인") 
                error_message = wait.until(EC.presence_of_element_located((By.ID, "error-element-password"))).text  
                if error_message:   # 안내 문구 노출 확인
                    assert "이메일 또는 비밀번호가 잘못되었습니다" in error_message
                    logging.info(f"⚠ 로그인 실패 - 안내 문구: {error_message}")

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
            logging.info(f"[통합] 로그인 기능 테스트 완료 {account_num}")
            logging.info("=" * 50)


    ''' [단위] 비밀번호를 잊으셨나요? 클릭 테스트 '''
    @pytest.mark.skip
    def test_forget_password_click(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

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

            # 비밀번호를 잊으셨나요? 링크 클릭
            login_page.forget_password_click()
            time.sleep(1)

            # 비밀번호 찾기 페이지 진입 확인
            wait.until(EC.url_contains("reset-password"))
            assert "reset-password" in driver.current_url
            logging.info("✔ 비밀번호 찾기 페이지 진입에 성공하였습니다.")

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
            logging.info("[단위] 비밀번호를 잊으셨나요? 클릭 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 비밀번호를 잊으셨나요? 이메일 입력 테스트 '''
    @pytest.mark.skip
    def test_forget_password_input_email(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

        # 계정 정보 가져오기
        EMAIL = account[0]["email"]

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

            # 비밀번호를 잊으셨나요? 링크 클릭
            login_page.forget_password_click()

            # 비밀번호 찾기 페이지 진입 확인
            wait.until(EC.url_contains("reset-password"))
            assert "reset-password" in driver.current_url
            logging.info("✔ 비밀번호 찾기 페이지 진입에 성공하였습니다.")

            # 이메일 입력
            input_email = login_page.forget_password_input_email(EMAIL)
            time.sleep(1)

            # 입력값 확인
            assert input_email.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 주소가 정상적으로 입력되었습니다. 이메일 주소: {EMAIL}")

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
            logging.info("[단위] 비밀번호를 잊으셨나요? 이메일 입력 테스트 완료")
            logging.info("=" * 50)


    ''' [통합] 비밀번호를 잊으셨나요? 비밀번호 재설정 테스트 '''
    @pytest.mark.parametrize("account_num", [0, 1, 2, 3])  # 0: 기존 계정, 1: 처음 접속 계정, 2: 유효하지 않은 계정, 3: 유효하지 않은 형식 계정
    def test_forget_password_next_click(self, driver: WebDriver, setup, account_num):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

        # 계정 정보 가져오기
        ACCOUNT_TYPE = account[account_num]["type"]
        EMAIL = account[account_num]["email"]

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

            # 비밀번호를 잊으셨나요? 링크 클릭
            login_page.forget_password_click()

            # 비밀번호 찾기 페이지 진입 확인
            wait.until(EC.url_contains("reset-password"))
            assert "reset-password" in driver.current_url
            logging.info("✔ 비밀번호 찾기 페이지 진입에 성공하였습니다.")

            # 이메일 입력
            input_email = login_page.forget_password_input_email(EMAIL)

            # 입력값 확인
            assert input_email.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 주소가 정상적으로 입력되었습니다. 이메일 주소: {EMAIL}")

            # 계속 버튼 클릭
            login_page.forget_password_next_click()
            logging.info("✔ 계속 버튼 클릭 완료")

            time.sleep(3)

            # 비밀번호 재설정 결과 확인
            if ACCOUNT_TYPE == "True":
                logging.info("▶▶ 유효한 계정 비밀번호 재설정")
                success_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Check Your Email']"))).text
                assert "Check Your Email" in success_message    # 비밀번호 재설정 완료 페이지 진입 확인
                logging.info("✔ 비밀번호 재설정 성공 - 이메일을 전송하였습니다.")
            else:
                logging.info("▶▶ 유효하지 않은 계정 비밀번호 재설정")
                error_message = wait.until(EC.presence_of_element_located((By.ID, "error-element-email"))).text
                assert "이메일이 유효하지 않습니다." in error_message   # 안내 문구 노출 확인
                logging.info(f"⚠ 비밀번호 재설정 실패 - 안내 문구: {error_message}")

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
            logging.info(f"[단위] 비밀번호를 잊으셨나요? 비밀번호 재설정 테스트 완료 {account_num}")
            logging.info("=" * 50)


    ''' [통합] 비밀번호를 잊으셨나요? 이메일 재전송 테스트 (유효한 계정만 진행) '''
    @pytest.mark.skip
    def test_forget_password_resend_email_click(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

        # 계정 정보 가져오기
        EMAIL = account[0]["email"]

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

            # 비밀번호를 잊으셨나요? 링크 클릭
            login_page.forget_password_click()

            # 비밀번호 찾기 페이지 진입 확인
            wait.until(EC.url_contains("reset-password"))
            assert "reset-password" in driver.current_url
            logging.info("✔ 비밀번호 찾기 페이지 진입에 성공하였습니다.")

            # 이메일 입력
            input_email = login_page.forget_password_input_email(EMAIL)

            # 입력값 확인
            assert input_email.get_attribute("value") == EMAIL
            logging.info(f"✔ 이메일 주소가 정상적으로 입력되었습니다. 이메일 주소: {EMAIL}")

            # 계속 버튼 클릭
            login_page.forget_password_next_click()
            logging.info("✔ 계속 버튼 클릭 완료")

            time.sleep(3)

            # 비밀번호 재설정 및 재전송 결과 확인
            logging.info("▶▶ 유효한 계정 비밀번호 재설정")
            success_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Check Your Email']"))).text
            assert "Check Your Email" in success_message    # 비밀번호 재설정 완료 페이지 진입 확인
            logging.info("✔ 비밀번호 재설정 성공 - 이메일을 전송하였습니다.")

            # Resend email 버튼 클릭
            login_page.forget_password_resend_email_click()
            logging.info("✔ Resend email 버튼 클릭 완료")
            time.sleep(1)

            # 비밀번호 찾기 페이지 재진입 확인
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='계속']")))
            assert "reset-password" in driver.current_url
            logging.info("✔ 비밀번호 찾기 페이지 재진입에 성공하였습니다.")
 
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
            logging.info(f"[통합] 비밀번호를 잊으셨나요? 이메일 재전송 테스트 완료")
            logging.info("=" * 50)


    ''' [통합] 비밀번호를 잊으셨나요? 로그인 화면으로 돌아가기 테스트 '''
    @pytest.mark.skip
    def test_forget_password_back_to_login_click(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

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

            # 비밀번호를 잊으셨나요? 링크 클릭
            login_page.forget_password_click()

            # 비밀번호 찾기 페이지 진입 확인
            wait.until(EC.url_contains("reset-password"))
            assert "reset-password" in driver.current_url
            logging.info("✔ 비밀번호 찾기 페이지 진입에 성공하였습니다.")
            time.sleep(1)

            # 로그인 화면으로 돌아가기 버튼 클릭
            login_page.forget_password_back_to_login_click()
            logging.info("✔ 로그인 화면으로 돌아가기 클릭 완료")
            time.sleep(1)

            # 로그인 페이지 재진입 확인
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
            logging.info("✔ 로그인 페이지 재진입에 성공하였습니다.")

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
            logging.info("[통합] 비밀번호를 잊으셨나요? 로그인 화면으로 돌아가기 테스트 완료")
            logging.info("=" * 50)


    ''' [통합] 계정이 없으신가요? 회원가입 클릭 테스트 '''
    @pytest.mark.skip
    def test_signup_click(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, main_page, login_page, wait = setup

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

            # 계정이 없으신가요? 회원가입 링크 클릭
            login_page.signup_click()
            time.sleep(1)
            
            # 회원가입 페이지 진입 확인
            wait.until(EC.url_contains("signup"))
            assert "signup" in driver.current_url
            logging.info("✔ 회원가입 페이지 진입에 성공하였습니다.")

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
            logging.info("[통합] 계정이 없으신가요? 회원가입 클릭 테스트 완료")
            logging.info("=" * 50)