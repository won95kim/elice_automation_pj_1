import time
import random
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from src.utils.helpers import Utils

load_dotenv("src/config/.env")
FILE = os.path.abspath("src/config/sky.jpg")

class MyPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)
        self.helpers = Utils(driver)
        self.action = ActionChains(driver)
    #개인피드 연필모양 요소 찾기 (부모클래스를 찾아서 자식클래스로 받아들인다은 배열 써서 클릭)
    def pencil_icon(self):
        parent_div = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.items-center.justify-between.text-subbody")))
        child_elements = parent_div.find_elements(By.XPATH, "./*") # 부모 기준 모든 직계 자식
        child_svg = child_elements[1]
        child_svg.click()

    def scroll(self,num):
        self.driver.execute_script(f"window.scrollTo(0, {num});")

    def slider_move(self):
        #슬라이더 요소 찾기
            sliders = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'block h-5 w-5 rounded-full')]")))

            # 단맛, 짠맛, 매운맛 슬라이더 랜덤값 설정
            target_sliders = sliders[3:6]
            slider_names = ["단맛", "짠맛", "매운맛"]
            for idx, slider in enumerate(target_sliders):
                    current_value = float(slider.get_attribute("aria-valuenow"))  # 현재 aria-valuenow 값
                    random_value = round(random.uniform(1.1, 5), 2)  # 랜덤 목표 값
                    print(f"{slider_names[idx]} 슬라이더 - 현재 값: {current_value}, 목표 값: {random_value}")
                    # 슬라이더 전체 길이 (447px로 고정)
                    slider_width = 447  # 슬라이더 픽셀 길이 (전체 기준)
                    # 픽셀당 값 비율 계산
                    min_value = 0  # 슬라이더 최소값
                    max_value = 5  # 슬라이더 최대값
                    pixels_per_value = slider_width / (max_value - min_value)  # 픽셀당 값 비율
                    # 목표 값으로 이동할 거리 계산
                    move_distance = round((random_value - current_value) * pixels_per_value, 2)
                    # 마우스 드래그 동작
                    self.action.click_and_hold(slider).move_by_offset(move_distance, 0).release().perform()
                    # 값이 변경되도록 잠시 대기
                    time.sleep(1)
                    # 이동 후 aria-valuenow 확인
                    new_value = float(slider.get_attribute("aria-valuenow"))
                    print(f"{slider_names[idx]} 슬라이더 - 최종 값: {new_value}")

    def input_slider_move(self,sweet_value,salt_value,spciy_value):
        #슬라이더 요소 찾기
            sliders = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'block h-5 w-5 rounded-full')]")))

            # 단맛, 짠맛, 매운맛 슬라이더 랜덤값 설정
            target_sliders = sliders[3:6]
            slider_names = ["단맛", "짠맛", "매운맛"]
            target_values = [sweet_value, salt_value, spciy_value]

            for idx, slider in enumerate(target_sliders):
                current_value = float(slider.get_attribute("aria-valuenow"))  # 현재 aria-valuenow 값
                target_value = target_values[idx]  # 목표 값
                print(f"{slider_names[idx]} 슬라이더 - 현재 값: {current_value}, 목표 값: {target_value}")

                # 슬라이더 전체 길이 (447px로 고정)
                slider_width = 447  # 슬라이더 픽셀 길이 (전체 기준)
                # 픽셀당 값 비율 계산
                min_value = 0  # 슬라이더 최소값
                max_value = 5  # 슬라이더 최대값
                pixels_per_value = slider_width / (max_value - min_value)  # 픽셀당 값 비율
                # 목표 값으로 이동할 거리 계산
                move_distance = round((target_value - current_value) * pixels_per_value, 2)

                # 마우스 드래그 동작
                self.action.click_and_hold(slider).move_by_offset(move_distance, 0).release().perform()
                # 값이 변경되도록 잠시 대기
                time.sleep(1)

                # 이동 후 aria-valuenow 확인
                new_value = float(slider.get_attribute("aria-valuenow"))
                print(f"{slider_names[idx]} 슬라이더 - 최종 값: {new_value}")

    def good_text_input(self,text):
        good_text = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='좋아하는 음식 성향을 이야기해주세요!']")))
        good_text.clear()
        good_text.send_keys(text)
    
    def bad_text_input(self,text):
        bad_text = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@placeholder='싫어하는 음식 성향을 이야기해주세요!']")))
        bad_text.clear()
        bad_text.send_keys(text)

    #유효성 검사 함수
    def valid_text(self):
        has_required_values = False
        
        if  self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-root"]/div/div[2]/section/form/div[3]/p'))):
            self.good_text_input('10글자 이상 넣어야 된다니까요 좋은음식')
            has_required_values = True  # 플래그 업데이트
        
        if  self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-root"]/div/div[2]/section/form/div[4]/p'))):
            self.bad_text_input('10글자 이상 넣어야 된다니까요 싫은음식')
            has_required_values = True  # 플래그 업데이트
        
        if has_required_values:
            time.sleep(1)
            self.submit_btn("프로필 수정 완료")

    def profile_check(self,text):
        profile = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='flex flex-col w-full gap-3']")))
        first_review = profile[0].get_attribute("innerHTML")  # innerHTML로 요소 내부 구조 가져오기
        assert text in first_review, "프로필 수정이 정상적으로 작성되지 않았다."
        print("프로필 수정이 정상적으로 작성되었다.")

    #+아이콘 찾기 함수
    def plus_icon(self):
        plus = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'cursor-pointer') and contains(@class, 'inline-flex') and contains(@class, 'items-center') and contains(@class, 'gap-2')]")))
        plus.click()

    # 작성 완료 버튼 함수
    def submit_btn(self,text):
        submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@type='submit' and text()='{text}']")))
        submit_btn.click()
    
    def radio_pick(self,text):
        radio_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"button[value='{text}']")))
        radio_button.click()

        if text == "그룹":
        # "같이 먹은 사람 등록" 요소 찾기
            group_input = self.driver.find_element(By.XPATH, "//input[@placeholder='이름을 검색해주세요']")
            group_input.clear()  # 기존 텍스트 비우기
            group_input.send_keys("홍길동, 김철수")

    def category_option(self,text):
        category_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{text}']")))
        category_option.click()

    def review_check(self,text):
        self.helpers.utils_nevigationbar('개인 피드')
        time.sleep(2)
        review = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flex.w-full.gap-6.p-4.shadow-md.rounded-2xl")))
        first_review = review[0].get_attribute("innerHTML")  # innerHTML로 요소 내부 구조 가져오기
        assert text in first_review, "후기가 정상적으로 작성되지 않았다."
        print("후기가 정상적으로 작성되었다.")

    def file_input(self):
        # 파일 업로드 요소 찾기 (일반적으로 input type="file")
        file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        # 파일 경로 입력 (예: zzz.jpg)
        file_input.send_keys(FILE)  # zzz.jpg 파일의 절대 경로

    def menu_input(self,text):
        menu_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='메뉴 명을 입력해주세요.']")))
        menu_input.send_keys(text)

    def category_random(self):
        random_category = random.choice(["중식", "일식", "한식","양식","아시안","기타", "분식", "패스트푸드"])
        self.category_option(random_category)

    def category_input(self):
        category_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.flex.h-10.items-center.justify-between.rounded-md")))
        category_input.click()
        self.category_random()
    
    def team_category_input(self):
        category_input = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.flex.h-10.items-center.justify-between.rounded-md")))
        second_category = category_input[1]
        second_category.click()
        self.category_random()

    def review_input(self,text):
        review_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='후기를 등록 입력해주세요.']")))
        review_input.send_keys(text)

    def star_input(self):
        random_num = random.randint(0, 4)
        star_input = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='w-10 h-10 cursor-pointer text-gray-300']")))
        star_input[random_num].click()

    def same_review(self):
        review = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'cursor-pointer') and contains(text(), '같은 메뉴 먹기')]")))
        review.click()

    def is_text_present(self, text):
        xpath = f"//p[contains(text(), '{text}')]"
        try:
        # 텍스트가 보이는지 확인
            short_wait = ws(self.driver, 5)  # 5초로 대기 시간 설정
            short_wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False
        
    def valid_value(self):
        # 요소가 발견되었는지 추적하는 플래그 변수
        has_required_values = False

        # "리뷰 이미지는 필수입니다" 텍스트 확인
        if self.is_text_present("리뷰 이미지는 필수입니다"):
            self.file_input()
            has_required_values = True  # 플래그 업데이트

        # "메뉴명은 필수입니다" 텍스트 확인
        if self.is_text_present("메뉴명은 필수입니다"):
            self.menu_input("오리")
            has_required_values = True  # 플래그 업데이트

        # "카테고리는 필수입니다" 텍스트 확인
        if self.is_text_present("카테고리는 필수입니다"):
            self.category_input()
            has_required_values = True  # 플래그 업데이트

        # "후기는 필수입니다" 텍스트 확인
        if self.is_text_present("후기는 필수입니다"):
            self.review_input("후기를 뭐라고 써야할지 모르겠어요")
            has_required_values = True  # 플래그 업데이트

        # "별점은 최소 1점 이상이어야 합니다" 텍스트 확인
        if self.is_text_present("별점은 최소 1점 이상이어야 합니다"):
            self.star_input()
            has_required_values = True  # 플래그 업데이트

        # 요소가 하나라도 발견된 경우에만 "후기 작성 완료" 버튼 클릭
        if has_required_values:
            time.sleep(1)
            self.submit_btn("후기 작성 완료")

    def team_valid_value(self):
        # 요소가 발견되었는지 추적하는 플래그 변수
        has_required_values = False

        # "리뷰 이미지는 필수입니다" 텍스트 확인
        if self.is_text_present("리뷰 이미지는 필수입니다"):
            self.file_input()
            has_required_values = True  # 플래그 업데이트

        # "메뉴명은 필수입니다" 텍스트 확인
        if self.is_text_present("메뉴명은 필수입니다"):
            self.menu_input("오리")
            has_required_values = True  # 플래그 업데이트

        # "카테고리는 필수입니다" 텍스트 확인
        if self.is_text_present("카테고리는 필수입니다"):
            self.team_category_input()
            has_required_values = True  # 플래그 업데이트

        # "후기는 필수입니다" 텍스트 확인
        if self.is_text_present("후기는 필수입니다"):
            self.review_input("후기를 뭐라고 써야할지 모르겠어요")
            has_required_values = True  # 플래그 업데이트

        # "별점은 최소 1점 이상이어야 합니다" 텍스트 확인
        if self.is_text_present("별점은 최소 1점 이상이어야 합니다"):
            self.star_input()
            has_required_values = True  # 플래그 업데이트

        # 요소가 하나라도 발견된 경우에만 "후기 작성 완료" 버튼 클릭
        if has_required_values:
            time.sleep(1)
            self.submit_btn("후기 작성 완료")
