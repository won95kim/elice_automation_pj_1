import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.helpers import Utils
from selenium.common.exceptions import NoSuchElementException
from src.pages.history_page import MenuRecommendation, HistoryPage, ReviewPage
from dotenv import load_dotenv

load_dotenv("src/config/.env")
FILE = os.path.abspath("src/config/sky.jpg")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

@pytest.fixture
def setup(driver):
    menu_page = MenuRecommendation(driver)
    history_page = HistoryPage(driver)
    review_page = ReviewPage(driver)
    helpers = Utils(driver)
    #로그인
    helpers.utils_login(EMAIL, PASSWORD)
    return menu_page, history_page, review_page , helpers

#혼자 먹기
class TestMenuRecommendation:
    def test_menu_recommendation(self,driver,setup):
        menu_page, history_page, review_page , helpers = setup

        menu_page.click_eating("혼자 먹기") #홈에서 혼자 먹기 버튼 클릭
        menu_page.select_food() #음식 카테고리 랜덤 선택
        time.sleep(1)
        menu_page.click_select_complete() #선택 완료 버튼 클릭
        menu_page.accept_recommendation() #다른메뉴 추천받기
        WebDriverWait(driver, 10).until(EC.url_to_be("https://kdt-pt-1-pj-2-team03.elicecoding.com/history"))
        assert driver.current_url == "https://kdt-pt-1-pj-2-team03.elicecoding.com/history"
        #추천 수락하면 히스토리 창으로 자동 이동 확인

        #히스토리 페이지에서 이미지 이름 정상확인하기
        errors = history_page.check_menu_images()
        if errors:
            print("\n".join(errors))
        else:
            print("✅ 모든 메뉴 이미지가 정상적으로 표시됩니다!")

        #히스토리 페이지에서 혼밥 정상 표시
        assert history_page.check_food_category("혼밥"), "혼밥이 정상적으로 표시되지 않습니다!"
        time.sleep(1)
        history_page.click_recommendation_review()  #후기 등록 버튼 클릭

#회식 하기
class TestMenuRecommendationCompany:
    def test_menu_recommendation(self, driver, setup):
        menu_page, history_page, review_page , helpers = setup

        menu_page.click_eating("회식 하기") #홈에서 회식 하기 버튼 클릭
        menu_page.select_food() #음식 카테고리 랜덤 선택
        time.sleep(1)

        menu_page.click_select_complete() #선택 완료 버튼 클릭
        menu_page.accept_recommendation() #다른메뉴 추천받기
        WebDriverWait(driver, 10).until(EC.url_to_be("https://kdt-pt-1-pj-2-team03.elicecoding.com/history"))
        assert driver.current_url == "https://kdt-pt-1-pj-2-team03.elicecoding.com/history"
        #추천 수락하면 히스토리 창으로 자동 이동 확인
        
        #이미지 이름 정상 확인
        errors = history_page.check_menu_images()
        if errors:
            print("\n".join(errors))
        else:
            print("✅ 모든 메뉴 이미지가 정상적으로 표시됩니다!")

        #히스토리 페이지에서 회식 정상 표시
        assert history_page.check_food_category("회식"), "회식이 정상적으로 표시되지 않습니다!"
        time.sleep(1)
        history_page.click_recommendation_review()  #후기 등록 버튼 클릭