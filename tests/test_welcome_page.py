import pytest
import json
import logging
import random
import os
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.utils.helpers import Utils
from src.pages.welcome_page import WelcomePage

''' 인적사항 작성 페이지 진입은 회원가입 후 혹은 처음 접속한 계정만 가능합니다. '''

# accounts.json에서 계정 정보 가져오기
JSON_PATH = os.path.join(os.getcwd(), "src/resources/testdata/account.json")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
    account = data.get("create_accounts", [])

# 처음 접속한 계정 정보 설정(가장 최근 회원가입 시 생성된 계정 가져오기

EMAIL = account[-1]["email"]
PASSWORD = account[-1]["password"]

# XPath 상수 정의
TEAM_DROPDOWN_XPATH = "//button[@role='combobox' and @aria-expanded='true']"
SELECT_TEAM_XPATH = "//span[@style='pointer-events: none;']"

# 테스트 데이터 정의
NAME = "QA1_3팀_테스터"
TEAM = ["개발 1팀", "개발 2팀", "디자인 1팀", "디자인 2팀"]
TASTE = ["단 맛", "짠 맛", "매운 맛"]
LIKE_UNLIKE = ["pros", "cons"]

''' 공통 데이터 셋팅 '''
@pytest.fixture
def setup(driver, request):
    # 로그 및 스크린샷 설정
    PAGE_NAME = "test_welcome_page"
    FUNC_NAME = request.node.name
    REPORT = Utils.utils_reports_setting(PAGE_NAME, FUNC_NAME)
    # 공통 모듈
    utils = Utils(driver)
    welcome_page = WelcomePage(driver)
    wait = ws(driver, 30)
    return REPORT, utils, welcome_page, wait


class TestWelcomePage:
    ''' [단위] 인적사항 작성 페이지 진입 테스트 '''
    @pytest.mark.skip
    def test_open(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, utils, _, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)
            time.sleep(1)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

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
            logging.info("[단위] 인적사항 작성 페이지 진입 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 이름 입력 기능 테스트 '''
    @pytest.mark.skip
    def test_welcome_input_name(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            # 이름 입력
            input_name_element = welcome_page.welcome_input_name(NAME)
            time.sleep(1)

            # 입력값 확인
            assert input_name_element.get_attribute("value") == NAME
            logging.info(f"✔ 이름 입력 성공: {NAME}")

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
            logging.info("[단위] 이름 입력 기능 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 팀 선택 드롭다운 클릭 테스트 '''
    @pytest.mark.skip
    def test_click_team_dropdown(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            # 드롭다운 클릭
            welcome_page.click_team_dropdown()
            time.sleep(1)

            # 드롭다운 노출 확인
            team_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, TEAM_DROPDOWN_XPATH)))
            assert team_dropdown.is_displayed()
            logging.info("✔ 팀 드롭다운 노출 성공")

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
            logging.info("[단위] 팀 선택 드롭다운 클릭 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 팀 선택 드롭다운 옵션 선택 테스트 '''
    @pytest.mark.skip
    @pytest.mark.parametrize("team_num", [0, 1, 2, 3])  # 0: 개발 1팀, 1: 개발 2팀, 2: 디자인 1팀, 3: 디자인 2팀
    def test_select_team(self, driver: WebDriver, setup, team_num):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            # 드롭다운 클릭
            welcome_page.click_team_dropdown()

            # 드롭다운 노출 확인
            team_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, TEAM_DROPDOWN_XPATH)))
            assert team_dropdown.is_displayed()
            logging.info("✔ 팀 드롭다운 노출 성공")

            # 팀 옵션 선택
            welcome_page.select_team(team_num + 1)  # HTML에서 1-based 인덱스 사용
            time.sleep(1)

            # 선택된 팀 확인
            wait.until(EC.text_to_be_present_in_element((By.XPATH, SELECT_TEAM_XPATH), TEAM[team_num]))
            selected_team = driver.find_element(By.XPATH, SELECT_TEAM_XPATH).text
            assert selected_team == TEAM[team_num]
            logging.info(f"✔ 팀 선택 성공: {TEAM[team_num]}")

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
            logging.info(f"[단위] 팀 선택 드롭다운 옵션 선택 테스트 완료 {team_num}")
            logging.info("=" * 50)


    ''' [단위] 음식 성향 슬라이더 이동 테스트 '''
    @pytest.mark.skip
    def test_move_taste_slider(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            # 단 맛/짠 맛/매운 맛 슬라이더 이동 및 확인
            for taste in TASTE:
                # 슬라이더 이동 실행
                random_move = welcome_page.move_taste_slider(taste)
                time.sleep(1)

                # 이동된 슬라이더 값 확인
                slider = driver.find_element(By.XPATH, f"//span[text()='{taste}']/following::span[@role='slider']")
                slider_value = round(float(slider.get_attribute("aria-valuenow")), 1)
                tolerance = round(abs(slider_value - random_move), 1)
                assert tolerance < 0.2   # 오차 범위 0.2까지는 넘어감
                logging.info(f"✔ {taste} 의 슬라이더가 정상 이동되었습니다. 입력된 값: {random_move} / 실제 이동 거리: {slider_value} / 오차 범위: {tolerance}")

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
            logging.info("[단위] 음식 성향 슬라이더 이동 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 추가 음식 성향 입력 테스트 '''
    @pytest.mark.skip
    def test_input_taste_preference(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            # 좋아요/싫어요 추가 음식 성향 입력
            for like_unlike in LIKE_UNLIKE:
                # 추가 음식 성향 랜덤 입력
                input_text = welcome_page.generate_random_food_preferences()
                input_element = welcome_page.input_taste_preference(like_unlike, input_text)
                time.sleep(1)

                # 입력값 확인
                assert input_element.text == input_text
                logging.info(f"✔ {like_unlike} 입력 성공: {input_text}")

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
            logging.info("[단위] 추가 음식 성향 입력 테스트 완료")
            logging.info("=" * 50)


    ''' [단위] 미입력 시 오류 메시지 확인 테스트 '''
    @pytest.mark.skip
    def test_get_all_error_messages(self, driver: WebDriver, setup):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            # 제출 버튼 클릭
            welcome_page.click_submit()
            time.sleep(1)

            # 오류 메시지 수집
            error_types, error_messages, expected_messages = welcome_page.get_all_error_messages()
            assert "welcome" in driver.current_url
            logging.info("⚠ 미입력 항목 존재 - 페이지 이동 실패")

            # 오류 메시지 확인
            for i in range(len(error_types)):
                assert expected_messages[i] in error_messages[i]
                logging.info(f"⚠ {error_types[i]}: {error_messages[i]}")

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
            logging.info("[단위] 미입력 시 오류 메시지 확인 테스트 완료")
            logging.info("=" * 50)


    ''' [통합] 인적사항 작성 후 제출 테스트 '''
    @pytest.mark.parametrize("test_num", [0, 1])  # 0: 초기 상태(미입력)로 제출, 1: 정상 입력 후 제출
    def test_welcome_submit(self, driver: WebDriver, setup, test_num):
        # 공통 데이터 불러오기
        REPORT, utils, welcome_page, wait = setup

        team_num = random.randrange(4)  # 랜덤 팀 선택

        try:
            # 로그인 수행
            utils.utils_login(EMAIL, PASSWORD)

            # 인적사항 작성 페이지 진입 확인
            wait.until(EC.url_contains("welcome"))
            assert "welcome" in driver.current_url
            logging.info(f"✔ 로그인 완료 - 인적사항 작성 페이지 진입 성공. 이메일 주소: {EMAIL}")

            if test_num == 0:
                logging.info("▶▶ 미입력 테스트 진행")

                # 제출 버튼 클릭
                welcome_page.click_submit()

                # 오류 메시지 수집
                error_types, error_messages, expected_messages = welcome_page.get_all_error_messages()
                assert "welcome" in driver.current_url
                logging.info("⚠ 미입력 항목 존재 - 페이지 이동 실패")

                # 오류 메시지 확인
                for i in range(len(error_types)):
                    assert expected_messages[i] in error_messages[i]
                    logging.info(f"⚠ {error_types[i]}: {error_messages[i]}")

            if test_num == 1:
                logging.info("▶▶ 정상 입력 테스트 진행") 

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
            logging.info(f"[통합] 인적사항 작성 후 제출 테스트 완료 {test_num}")
            logging.info("=" * 50)