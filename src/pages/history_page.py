from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import random
import time

#메뉴 추천받기
class MenuRecommendation:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click_button(self, xpath: str):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()

    #홈에서 메뉴 추천
    def click_eating(self, option: str):
        xpath = f"//button[div/p[text()='{option}']]"
        self.click_button(xpath)

# 음식 카테고리 랜덤 선택
    def select_food(self):
        food_choices = random.choice(["한식", "중식", "양식", "일식", "분식", "아시안", "패스트푸드", "기타"])
    
    # 드롭다운 버튼 클릭
        self.click_button("//button[@role='combobox']")
    
    # 옵션들 가져오기
        options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']")))
    
    # 옵션 중 랜덤으로 하나의 옵션 선택
        random_food_choice = random.choice(food_choices)
    
        # 리스트에서 랜덤으로 선택된 값과 일치하는 옵션 찾기
        for option in options:
            if random_food_choice in option.text:
                option.click()
                break
    
        # 랜덤으로 선택된 음식을 반환
        return random_food_choice


    #첫 번째 체크박스 클릭
    def click_group_checkbox(self):
        checkbox_xpath = "//input[@type='checkbox' and contains(@class, 'cursor-pointer') and contains(@class, 'accent-main-black')]"
        checkbox = self.driver.find_element(By.XPATH, checkbox_xpath)
        if not checkbox.is_selected():
            self.click_button(checkbox_xpath)

    #선택 완료 버튼 클릭
    def click_select_complete(self):
        self.click_button("//button[text()='선택 완료']")

    #추천 수락하기 버튼 클릭
    def click_accept_recommendation(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.click_button("//button[text()='추천 수락하기']")

    #다시 추천 받기 버튼 클릭
    def click_reset_recommendation(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.click_button("//button[text()='다시 추천 받기']")

    #ai가 분석한 취향 적합률 가져오기 
    def get_suitability_score(self):
        print("[DEBUG] 적합률 요소 찾기 시작...")

        try:
        # 1️⃣ 해당 class를 가진 요소를 먼저 대기
            suitability_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'bg-sub') and contains(@class, 'text-white')]")
                )
            )
            print("[DEBUG] 요소 찾음. 값 로딩 확인 중...")

            max_wait_time = 15  # 최대 대기 시간 (초)
            start_time = time.time()

            while True:
                try:
                    suitability_text = suitability_element.text.strip()
                    print(f"[DEBUG] 현재 적합률 값: '{suitability_text}'")

                    if suitability_text and "%" in suitability_text:
                        suitability_score = float(suitability_text.replace("%", "").strip())
                        print(f"[DEBUG] 최종 적합률: {suitability_score}%")
                        return suitability_score

                except StaleElementReferenceException:
                    print("[WARNING] 요소가 변경됨. 다시 찾는 중...")
                    suitability_element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'bg-sub') and contains(@class, 'text-white')]")
                        )
                    )

                if time.time() - start_time > max_wait_time:
                    raise TimeoutException("[ERROR] 적합률 값이 15초 내에 로딩되지 않음!")

                time.sleep(0.5)

        except (TimeoutException, NoSuchElementException) as e:
            print(f"[ERROR] 요소를 찾을 수 없음: {str(e)}")
            return None
    
    
    #취향 적합률이 50% 미만이면 다시 추천받기
    def accept_recommendation(self):
        suitability_score = self.get_suitability_score()
        retry_count = 0  #반복 횟수 제한

        while suitability_score <= 50.0:
            if retry_count > 3:  #최대 3번 반복 후 종료
                print("[ERROR] 추천을 너무 많이 요청했어요! 종료합니다.")
                break
        
            print(f"[INFO] 취향 적합률 {suitability_score}% → 다시 추천 받기 클릭!")
            self.click_reset_recommendation()
            time.sleep(2)
            suitability_score = self.get_suitability_score() #새 적합률 확인
            retry_count += 1

        print(f"[INFO] 최종 취향 적합률 {suitability_score}% → 추천 수락하기 클릭!")
        self.click_accept_recommendation() #추천 수락하기
        print("[DEBUG] 추천 수락하기 클릭 완료 (함수 끝)")

class HistoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_button(self, xpath: str):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()

    #홈 버튼 클릭
    def click_home(self):
        self.click_button("//a[span[text()='홈']]")

    #히스토리 클릭
    def click_history(self):
        self.click_button("//a[span[text()='히스토리']]")

     #홈에서 개인 피드 버튼 클릭
    def click_my_feed(self):
        self.click_button("//a[span[text()='개인 피드']]")

    #추천 후기 등록 버튼 클릭 (첫 번째)
    def click_recommendation_review(self):
        self.click_button("(//button[text()='추천 후기 등록하기'])[1]")

    #히스토리 페이지 메뉴 이미지와 이름 정상 표시
    def check_menu_images(self):
        errors = []
        images = self.driver.find_elements(By.CLASS_NAME, "object-cover")
        for index, img in enumerate(images):
            try:
                menu_name = img.get_attribute("alt")
                img_src = img.get_attribute("src")

                if not menu_name or menu_name.strip() == "":
                    errors.append(f"❌ 이미지 {index+1}: 메뉴 이름(alt) 없음")
                if not img_src or "http" not in img_src:
                    errors.append(f"❌ 이미지 {index+1}: 이미지 src 없음")     

            except Exception as e:
                errors.append(f"❌ 이미지 {index+1}: 오류 발생 - {str(e)}")
            return errors
        
    #히스토리 페이지에서 혼밥, 한식 정상 표시
    def check_food_category(self, category):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(@class, 'bg-main') and text()='{category}']"))
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'bg-sub') and text()='한식']"))
            )
            return True
        except:
            return False
        
    #히스토리에서 가장 최근 메뉴명 가져오기 
    def get_latest_menu_name(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            latest_menu = self.driver.find_element(By.XPATH, "//div[contains(@class, 'font-bold')]").text
            print(f"[INFO] 최근 추천받은 메뉴: {latest_menu}")
            return latest_menu
        except Exception as e:
            print(f"[ERROR] 최근 메뉴명 가져오기 실패: {e}")
            return None

class ReviewPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_button(self, xpath: str):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()
    
    #혼밥/그룹/회식 선택 고정
    def is_eating_fixed(self, category):
        try:
            solo_label = self.driver.find_element(By.XPATH, f"//div[contains(@class, 'bg-main') and text()='{category}']")
            if solo_label:
                print("[PASS] 식사유형이 고정되어 있습니다.")
                return True
            else:
                print(f"[FAIL] 식사유형이 고정되어 있지 않습니다.")
                return False
        except Exception as e:
            print(f"[ERROR] '{category}' 고정 확인 중 오류: {e}")
            return False
        
    #메뉴 이름 고정
    def is_menu_name_fixed(self, expected_name):
        try:
            input_field = self.driver.find_element(By.NAME, "menu")
            actual_value = input_field.get_attribute("value")
            if actual_value == expected_name and input_field.get_attribute("disabled") is not None:
                print(f"[PASS] 메뉴 이름이 '{expected_name}'으로 고정되어 있습니다.")
                return True
            else:
                print(f"[FAIL] 메뉴 이름이 '{expected_name}'으로 고정되지 않았습니다. 현재 값: '{actual_value}'")
                return False
        except Exception as e:
            print(f"[ERROR] 메뉴 이름 고정 확인 중 오류: {e}")
            return False
        
    #카테고리 선택 고정
    def is_food_fixed(self, expected_food):
        try:
            xpath = f"//div[contains(@class, 'bg-sub') and text()='{expected_food}']"
            fixed_label = self.driver.find_element(By.XPATH, xpath)
            if fixed_label:
                print(f"[PASS] '{expected_food}'이(가) 고정되어 있습니다.")
                return True
            else:
                print(f"[FAIL] '{expected_food}'이(가) 고정되어 있지 않습니다.")
                return False
        except Exception as e:
            print(f"[ERROR] '{expected_food}' 고정 확인 중 오류: {e}")
            return False

    #후기 작성 완료 버튼 클릭
    def click_submit_review(self):
        self.click_button("//button[text()='후기 작성 완료']")

    #메시지 출력 확인
    def message_displayed(self, message):
        return bool(self.driver.find_elements(By.XPATH, f"//p[contains(text(), '{message}')]"))
    
    #이미지 업로드
    def upload_image(self, image_path):
        file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(image_path)

    #후기 내용 입력
    def enter_review_text(self, text):
        review_textarea = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='후기를 등록 입력해주세요.']")))
        review_textarea.send_keys(text)

    #별점
    def select_random_star_rating(self):
        star_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='w-10 h-10 cursor-pointer text-gray-300']"))
        )
        random_num = random.randint(0, 4)  # 0~4 중 랜덤 선택
        star_elements[random_num].click()