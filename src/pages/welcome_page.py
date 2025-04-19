import random
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

''' 인적사항 작성 페이지는 회원가입 후 혹은 처음 접속한 계정만 접근할 수 있습니다. '''

class WelcomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)  # 최대 10초 대기 설정

    ''' 사용자 이름 입력 '''
    def welcome_input_name(self, name):
        # 이름 입력
        input_name_element = self.wait.until(EC.presence_of_element_located((By.NAME, "name")))
        input_name_element.send_keys(name)
        return input_name_element


    ''' 팀 선택을 위한 드롭다운 클릭 '''
    def click_team_dropdown(self):
        # 드롭다운 클릭
        team_dropdown_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox']")))
        team_dropdown_button.click()


    ''' 드롭다운에서 팀 옵션 선택 (index를 사용하여 선택) '''
    def select_team(self, team_index):
        # 팀 옵션 선택
        team_option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[@role='option'])[{team_index}]")))
        team_option_element.click()


    ''' 음식 성향 슬라이더를 지정된 위치로 이동 '''
    def move_taste_slider(self, taste):
        slider_element = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//span[.='{taste}']/following-sibling::div//span[@role='slider']")))

        min_value = 0   # 슬라이더의 최소값 정의
        max_value = 5   # 슬라이더의 최대값 정의
        slider_width = 407  # 슬라이더의 전체 길이 설정

        random_move = round(random.uniform(1.0, 5.0), 1)    # 슬라이더 이동 거리 랜덤 값 생성

        move_percentage = slider_width / (max_value - min_value)    # 슬라이더 이동 비율 계산
        move_distance = random_move * move_percentage   # 이동 거리 계산
        
        # 슬라이더 이동 실행
        actions = ActionChains(self.driver)
        actions.click_and_hold(slider_element).move_by_offset(move_distance, 0).release().perform()
        return random_move


    ''' 추가적인 음식 성향(좋아요/싫어요) 입력 처리 '''
    def input_taste_preference(self, like_unlike, text):
        # 추가 음식 성향 입력
        input_taste_text_element = self.wait.until(EC.presence_of_element_located((By.NAME, f"{like_unlike}")))
        input_taste_text_element.send_keys(text)
        return input_taste_text_element


    ''' 랜덤으로 음식 성향을 생성하여 반환 '''
    def generate_random_food_preferences(self):
        # 음식 종류별 리스트 정의
        korean_food = ["김치찌개", "비빔밥", "떡볶이", "불고기", "된장찌개", "갈비", "김밥", "불닭", "수제비", "찜닭"]
        western_food = ["파스타", "피자", "스테이크", "햄버거", "리조또", "프라이드 치킨", "샐러드", "스프", "크로아상", "오믈렛"]
        chinese_food = ["짜장면", "짬뽕", "탕수육", "마파두부", "깐풍기", "유산슬", "팔보채", "양장피", "볶음밥", "춘권"]
        japanese_food = ["초밥", "라멘", "덮밥", "우동", "가츠동", "타코야끼", "오니기리", "쇼유라멘", "규동", "모찌"]
        indian_food = ["카레", "난", "비리야니", "탄두리 치킨", "사모사", "라시", "푸리", "팔락 파니르", "알루 고비", "차이"]

        # 음식 종류 딕셔너리 생성
        food_type_dict = {
            "한식": korean_food,
            "양식": western_food,
            "중식": chinese_food,
            "일식": japanese_food,
            "인도식": indian_food
        }
        food_type = random.choice(list(food_type_dict.keys()))  # 음식 종류 무작위 선택
        food_list = random.sample(food_type_dict[food_type], k=3)   # 3가지 음식 랜덤 샘플링
        return f"{food_type}: {food_list}"


    ''' 제출하기 버튼 클릭 '''
    def click_submit(self):
        # 제출 버튼 클릭
        submit_button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='제출하기']")))
        submit_button_element.click()


    ''' 입력이 부족할 경우 나오는 오류 메시지 리스트 반환 '''
    def get_all_error_messages(self):
        # 각 오류 메시지 요소 찾기
        input_name_error_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '이름을 입력')]"))).text
        selected_team_error_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), '팀을 선택')]"))).text
        taste_slider_error_message_1 = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(), '맛에 대한 성향')])[1]"))).text
        taste_slider_error_message_2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(), '맛에 대한 성향')])[2]"))).text
        taste_slider_error_message_3 = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(), '맛에 대한 성향')])[3]"))).text
        like_unlike_taste_text_error_message_1 = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(), '10자 이상')])[1]"))).text
        like_unlike_taste_text_error_message_2 = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(), '10자 이상')])[2]"))).text
            
        # 오류 메시지 리스트 정의
        error_type = ["이름 미입력", "팀 미선택", "단 맛 미선택", "짠 맛 미선택", "매운 맛 미선택", "좋아요 성향 미입력", "싫어요 성향 미입력"]
        error_messages = [input_name_error_message, selected_team_error_message, taste_slider_error_message_1, taste_slider_error_message_2,
                          taste_slider_error_message_3, like_unlike_taste_text_error_message_1, like_unlike_taste_text_error_message_2]
        check_error_messages = ["이름을 입력해주세요", "팀을 선택해주세요", "맛에 대한 성향은 최소 1 이상 설정해주세요", "맛에 대한 성향은 최소 1 이상 설정해주세요", 
                                "맛에 대한 성향은 최소 1 이상 설정해주세요", "10자 이상 입력해주세요", "10자 이상 입력해주세요"]
        
        return error_type, error_messages, check_error_messages