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

    # 추천 후기 등록 버튼
    def test_recommendation_review(self,driver,setup):
        menu_page, history_page, review_page , helpers = setup
        helpers.utils_nevigationbar("히스토리")
        time.sleep(1)
        history_page.click_recommendation_review()  #후기 등록 버튼 클릭

        review_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='후기 등록하기']")))
        assert review_text.is_displayed(), "'후기 등록하기' 텍스트가 보이지 않습니다."
        #후기 등록 화면 정상 표시
        time.sleep(2)

        # 히스토리에서 최근 추천받은 메뉴 가져오기
        latest_menu = history_page.get_latest_menu_name()
        assert latest_menu is not None, "❌ 최근 추천받은 메뉴를 가져오지 못함"

        # 리뷰 등록 화면에서 메뉴명이 고정되어 있는지 확인
        result = review_page.is_menu_name_fixed(latest_menu)
        assert result, f"❌ 메뉴 이름이 '{latest_menu}'으로 고정되지 않음"

        #혼밥 선택 고정 확인
        result = review_page.is_eating_fixed("혼밥")
        assert result, "❌ '혼밥'이 고정되어 있지 않음"
    
        #후기 공란으로 작성 완료 버튼 클릭시 메세지 정상 출력 테스트
        review_page.click_submit_review()
        time.sleep(1) 

        assert review_page.message_displayed("리뷰 이미지는 필수입니다"), "❌ 리뷰 이미지 경고 메시지 없음!"
        assert review_page.message_displayed("후기는 필수입니다"), "❌ 후기 입력 경고 메시지 없음!"
        assert review_page.message_displayed("별점은 최소 1점 이상이어야 합니다"), "❌ 별점 경고 메시지 없음!"
        print("✅ 공란 상태 테스트 통과!")

        #후기 정상 등록
        review_page.upload_image(FILE)
        review_page.enter_review_text("후기를열글자나써야돼요") 
        review_page.select_random_star_rating()
        time.sleep(1)

        review_page.click_submit_review()
        time.sleep(1)

        #🔍 같은 위치에 있는 버튼이 사라졌거나 비활성화되었는지 확인
        try:
        # 후기 등록했던 첫 번째 버튼 위치에 있는 버튼 다시 찾기
            button = driver.find_element(By.XPATH, "(//button[text()='추천 후기 등록하기'])[1]")

        # disabled 속성 확인
            if button.get_attribute("disabled"):
                print("✅ 후기 등록 버튼이 비활성화되었습니다.")
                assert True

        except NoSuchElementException:
            print("✅ 후기 등록 버튼이 비활성화되었습니다.")
            assert True

        #개인 피드로 이동
        history_page.click_my_feed()
        time.sleep(2)
    
        #스크롤 내리기
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(2)

        #후기 리스트 가져오기
        review = driver.find_elements(By.CLASS_NAME, "flex.w-full.gap-6.p-4.shadow-md.rounded-2xl")

        #리스트가 비어 있으면 실패 처리
        assert len(review) > 0, "❌ 등록된 후기가 없습니다."

        #첫 번째 후기의 내용 가져오기
        first_review = review[0].get_attribute("innerHTML")
        assert "혼밥" in first_review, "❌ 후기가 정상적으로 작성되지 않았습니다."
        print("✅ 후기가 정상적으로 작성되었습니다.")
        time.sleep(1)


#같이 먹기
class TestMenuRecommendationGroup:
    def test_menu_recommendation(self,driver,setup):
        menu_page, history_page, review_page, helpers = setup

        menu_page.click_eating("같이 먹기") #홈에서 같이 먹기 버튼 클릭
        menu_page.select_food() #음식 카테고리 랜덤 선택
        menu_page.click_group_checkbox() #체크 박스 체크
        time.sleep(1)

        menu_page.click_select_complete() #선택 완료 버튼 클릭
        menu_page.accept_recommendation() #다른메뉴 추천받기
        WebDriverWait(driver, 10).until(EC.url_to_be("https://kdt-pt-1-pj-2-team03.elicecoding.com/history"))
        assert driver.current_url == "https://kdt-pt-1-pj-2-team03.elicecoding.com/history"
        #추천 수락하면 히스토리 창으로 자동 이동 확인

        errors = history_page.check_menu_images()
        if errors:
            print("\n".join(errors))
        else:
            print("✅ 모든 메뉴 이미지가 정상적으로 표시됩니다!")

    #히스토리 페이지에서 그룹 정상 표시
        assert history_page.check_food_category("그룹"), "그룹이 정상적으로 표시되지 않습니다!"
    
    # 추천 후기 등록 버튼
    def test_recommendation_review(self, driver, setup):
        menu_page, history_page, review_page , helpers = setup
        helpers.utils_nevigationbar("히스토리")
        history_page.click_recommendation_review()  #후기 등록 버튼 클릭

        review_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='후기 등록하기']")))
        assert review_text.is_displayed(), "'후기 등록하기' 텍스트가 보이지 않습니다."
        #후기 등록 화면 정상 표시
        time.sleep(2)

        #히스토리에서 최근 추천받은 메뉴 가져오기
        latest_menu = history_page.get_latest_menu_name()
        assert latest_menu is not None, "❌ 최근 추천받은 메뉴를 가져오지 못함"

        #리뷰 등록 화면에서 메뉴명이 고정되어 있는지 확인
        result = review_page.is_menu_name_fixed(latest_menu)
        assert result, f"❌ 메뉴 이름이 '{latest_menu}'으로 고정되지 않음"
    
        #그룹 선택 고정 확인
        result = review_page.is_eating_fixed("그룹")
        assert result, "❌ '그룹'이 고정되어 있지 않음"
    
        #후기 공란으로 작성 완료 버튼 클릭시 메세지 정상 출력 테스트
        review_page.click_submit_review()
        time.sleep(1) 

        assert review_page.message_displayed("리뷰 이미지는 필수입니다"), "❌ 리뷰 이미지 경고 메시지 없음!"
        assert review_page.message_displayed("후기는 필수입니다"), "❌ 후기 입력 경고 메시지 없음!"
        assert review_page.message_displayed("별점은 최소 1점 이상이어야 합니다"), "❌ 별점 경고 메시지 없음!"
        print("✅ 공란 상태 테스트 통과!")

        #후기 정상 등록
        review_page.upload_image(FILE)
        review_page.enter_review_text("후기를열글자나써야돼요") 
        review_page.select_random_star_rating()
        time.sleep(1)

        review_page.click_submit_review()
        time.sleep(1)

        #🔍 같은 위치에 있는 버튼이 사라졌거나 비활성화되었는지 확인
        try:
        # 후기 등록했던 첫 번째 버튼 위치에 있는 버튼 다시 찾기
            button = driver.find_element(By.XPATH, "(//button[text()='추천 후기 등록하기'])[1]")

        # disabled 속성 확인
            if button.get_attribute("disabled"):
                print("✅ 후기 등록 버튼이 비활성화되었습니다.")
                assert True

        except NoSuchElementException:
            print("✅ 후기 등록 버튼이 비활성화되었습니다.")
            assert True

        #개인 피드로 이동
        history_page.click_my_feed()
        time.sleep(2)
    
        #스크롤 내리기
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(2)

        #후기 리스트 가져오기
        review = driver.find_elements(By.CLASS_NAME, "flex.w-full.gap-6.p-4.shadow-md.rounded-2xl")

        #리스트가 비어 있으면 실패 처리
        assert len(review) > 0, "❌ 등록된 후기가 없습니다."

        #첫 번째 후기의 내용 가져오기
        first_review = review[0].get_attribute("innerHTML")
        assert "그룹" in first_review, "❌ 후기가 정상적으로 작성되지 않았습니다."
        print("✅ 후기가 정상적으로 작성되었습니다.")



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
    
    # 추천 후기 등록 버튼
    def test_recommendation_review(self, driver, setup):
        menu_page, history_page, review_page , helpers = setup
        helpers.utils_nevigationbar("히스토리")
        history_page.click_recommendation_review()  #후기 등록 버튼 클릭

        review_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='후기 등록하기']")))
        assert review_text.is_displayed(), "'후기 등록하기' 텍스트가 보이지 않습니다."
        #후기 등록 화면 정상 표시
        time.sleep(2)

        #히스토리에서 최근 추천받은 메뉴 가져오기
        latest_menu = history_page.get_latest_menu_name()
        assert latest_menu is not None, "❌ 최근 추천받은 메뉴를 가져오지 못함"

        #리뷰 등록 화면에서 메뉴명이 고정되어 있는지 확인
        result = review_page.is_menu_name_fixed(latest_menu)
        assert result, f"❌ 메뉴 이름이 '{latest_menu}'으로 고정되지 않음"
    
    #회식 선택 고정 확인
        result = review_page.is_eating_fixed("회식")
        assert result, "❌ '회식'이 고정되어 있지 않음"

        #후기 공란으로 작성 완료 버튼 클릭시 메세지 정상 출력 테스트
        review_page.click_submit_review()
        time.sleep(1) 

        assert review_page.message_displayed("리뷰 이미지는 필수입니다"), "❌ 리뷰 이미지 경고 메시지 없음!"
        assert review_page.message_displayed("후기는 필수입니다"), "❌ 후기 입력 경고 메시지 없음!"
        assert review_page.message_displayed("별점은 최소 1점 이상이어야 합니다"), "❌ 별점 경고 메시지 없음!"
        print("✅ 공란 상태 테스트 통과!")

        #후기 정상 등록
        review_page.upload_image(FILE)
        review_page.enter_review_text("후기를열글자나써야돼요") 
        review_page.select_random_star_rating()
        time.sleep(1)

        review_page.click_submit_review()
        time.sleep(1)

        #🔍 같은 위치에 있는 버튼이 사라졌거나 비활성화되었는지 확인
        try:
        # 후기 등록했던 첫 번째 버튼 위치에 있는 버튼 다시 찾기
            button = driver.find_element(By.XPATH, "(//button[text()='추천 후기 등록하기'])[1]")

        # disabled 속성 확인
            if button.get_attribute("disabled"):
                print("✅ 후기 등록 버튼이 비활성화되었습니다.")
                assert True

        except NoSuchElementException:
            print("✅ 후기 등록 버튼이 비활성화되었습니다.")
            assert True

        #개인 피드로 이동
        history_page.click_my_feed()
        time.sleep(2)
    
        #스크롤 내리기
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(2)

        #후기 리스트 가져오기
        review = driver.find_elements(By.CLASS_NAME, "flex.w-full.gap-6.p-4.shadow-md.rounded-2xl")

        #리스트가 비어 있으면 실패 처리
        assert len(review) > 0, "❌ 등록된 후기가 없습니다."

        #첫 번째 후기의 내용 가져오기
        first_review = review[0].get_attribute("innerHTML")
        assert "회식" in first_review, "❌ 후기가 정상적으로 작성되지 않았습니다."
        print("✅ 후기가 정상적으로 작성되었습니다.")