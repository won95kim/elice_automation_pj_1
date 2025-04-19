from time import sleep
import pytest
import json

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC

from src.utils.helpers import Utils
from src.pages.team_page import TeamPage
from tests.conftest import driver 

with open("src/resources/testdata/account.json", "r", encoding = "utf-8") as f:
    data = json.load(f)
    account = data.get("accounts", [])

EMAIL = account[0]["email"]
PASSWORD = account[0]["password"]



class TestTeamPage:

    def login_as_user(self, driver: webdriver):
        login = Utils(driver)
        login.utils_login(EMAIL, PASSWORD)
        sleep(5)

        team_page = TeamPage(driver)
        team_page.click_team_feed_tab()
        sleep(2)

    def test_team_feed_elements_visible(self, driver: WebDriver):
        # 로그인 + 팀피드 진입까지 재사용
        self.login_as_user(driver)

        team_page = TeamPage(driver)

        # 요소 검증 함수 호출
        assert team_page.is_team_menu_and_category_visible(), "❌ 메뉴 타이틀/카테고리 요소 없음"
        assert team_page.is_food_preference_section_visible(), "❌ 음식 성향 요소 없음"
        assert team_page.is_pie_chart_visible(), "❌ 원형 그래프 요소 없음"
        assert team_page.is_bar_chart_visible(), "❌ 바형 그래프 요소 없음"

        print("✅ 팀 피드 주요 요소 모두 정상적으로 로딩됨")  

        sleep(5)

        # 카테고리 클릭 함수 호출
        team_page.select_teams_by_index()

        sleep(5)

        # 팀 피드 연필모양 클릭(선동님 코드)
        team_page.pencil_icon()

        sleep(2)
        # 슬라이더 이동 함수 호출
        team_page.move_flavor_sliders(direction="right", distance=15)
        sleep(1)

        team_page.move_flavor_sliders(direction="left", distance=15)
        sleep(1)
        # 그냥 통과 확인용
        assert True
        # 이런 음식 좋아요! 랜덤 텍스트 입력 함수 호출
        team_page.input_random_favorite_food()
        sleep(2)
        # 이런 음식 싫어요! 랜덤 텍스트 입력 함수 호출
        team_page.input_random_hated_food()
        sleep(2)

        # 프로필 수정 완료 버튼 클릭
        team_page.submit_btn("프로필 수정 완료")
        print("✅ '프로필 수정 완료' 버튼 클릭 완료")

        sleep(3)

        driver.quit()
        print("✅ 팀 피드 페이지 테스트 완료")
