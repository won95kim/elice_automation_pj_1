from time import sleep
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

class TeamPage:
    URL = "https://kdt-pt-1-pj-2-team03.elicecoding.com/"

    def __init__(self,driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
    # 팀 피드 탭 클릭
    def click_team_feed_tab(self):
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/ul/li[2]/a').click()
    # 1. 팀 메뉴 제목 + 드롭다운 요소
    def is_team_menu_and_category_visible(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/ul/li[2]/a')
            return True
        except NoSuchElementException:
            return False

    # 2. 음식 성향 요소
    def is_food_preference_section_visible(self):
        try: 
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/main/section/section/section')
            return True
        except NoSuchElementException:
            return False

    # 3. 팀 통계 원형 그래프
    def is_pie_chart_visible(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/main/section/section/div[2]/div/div/canvas')
            return True
        except NoSuchElementException:
            return False

    # 4. 팀 통계 바형 그래프
    def is_bar_chart_visible(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/main/section/section/div[2]/canvas')
            return True
        except NoSuchElementException:
            return False
        
    # 5. 카테고리 드롭다운 버튼   
    def open_category_dropdown(self):
        try:
             dropdown = ws(self.driver, 10).until(
                 EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/main/section/section/div[1]/button/svg'))  # 예시 클래스명
            )
             dropdown.click()
            
        except Exception as e:
            return False
        
    # 6. 인덱스로 개발2팀,디자인1팀,디자인2팀 클릭   
    def select_teams_by_index(self):
        team_indexes = [1, 3, 4, 2]
        team_names = {
        2: "개발2팀",
        3: "디자인1팀",
        4: "디자인2팀",
        1: "개발1팀"
        }
        for index in team_indexes:
            try:
                # 현재 인덱스에 해당하는 팀 이름 가져오기
                team_name = team_names.get(index, "알 수 없는 팀")
                print(f"\n▶ {team_name} 클릭 시도 중...")

                # 드롭다운 열기
                dropdown = ws(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@role="combobox"]'))
                )
                dropdown.click()
                sleep(0.5)

                # 드롭다운 옵션 클릭
                option = ws(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'(//div[@role="option"])[{index}]'))
                )
                option.click()

                print(f"✅ {team_name} 선택 완료")
                sleep(1.5)

            except Exception as e:
                print(f"❌ {team_name} 선택 실패 - 에러: {e}")
                sleep(2)

    # 7. 단맛,짠맛,매운맛 슬라이더 기능
    def move_flavor_sliders(self, direction="right", distance=10):

            slider_xpaths = [
            '//*[@id="modal-root"]/div/div[2]/section/form/div[1]/div/section[1]/div/span[1]/span[2]/span',  # 단맛
            '//*[@id="modal-root"]/div/div[2]/section/form/div[1]/div/section[2]/div/span[1]/span[2]/span',  # 짠맛
            '//*[@id="modal-root"]/div/div[2]/section/form/div[1]/div/section[3]/div/span[1]/span[2]/span',  # 매운맛
            ]

            offset = distance if direction == "right" else -distance

            for idx, xpath in enumerate(slider_xpaths):
                slider = self.driver.find_element(By.XPATH, xpath)
                actions = ActionChains(self.driver)
                actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()
                sleep(0.5)
                print(f"✅ 슬라이더 {idx+1}번 ({'단맛' if idx==0 else '짠맛' if idx==1 else '매운맛'}) → {direction}로 이동 완료")
            
    # 좋아하는 음식에 랜덤 텍스트 입력
    def input_random_favorite_food(self):
        texts = [
            "한식과 양식 좋아합니다",
            "매운 음식에 진심입니다",
            "디저트는 무조건 필수",
            "초밥과 라멘 최고에요",
            "간단한 분식류 좋아요",
            "저는 국밥도 최고에요"
        ]

        try:
            textarea = ws(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "pros"))
            )
            random_text = random.choice(texts)
            textarea.clear()
            textarea.send_keys(random_text)
            print(f"✅ 텍스트 입력 성공: {random_text}")
        except Exception as e:
            print(f"❌ 텍스트 입력 실패: {e}")

    # 싫어하는 음식에 랜덤 텍스트 입력
    def input_random_hated_food(self):
        texts = [
            "중식은 기름져서 별로에요",
            "향신료 강한 음식은 어려워요",
            "단 음식은 잘 안 먹어요",
            "짜고 매운 건 부담돼요",
            "해산물은 안 맞아요",
            "느끼한 음식은 싫어요"
        ]

        try:
            textarea = ws(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "cons"))
            )
            random_text = random.choice(texts)
            textarea.clear()
            textarea.send_keys(random_text)
            print(f"✅ 싫어하는 음식 텍스트 입력 성공: {random_text}")
        except Exception as e:
            print(f"❌ 싫어하는 음식 텍스트 입력 실패: {e}")

    def pencil_icon(self):
        parent_div = ws(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.items-center.justify-between.text-subbody")))
        child_elements = parent_div.find_elements(By.XPATH, "./*") # 부모 기준 모든 직계 자식
        child_svg = child_elements[1]
        child_svg.click()

    # 작성 완료 버튼 함수
    def submit_btn(self,text):
        submit_btn = ws(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@type='submit' and text()='{text}']")))
        submit_btn.click()