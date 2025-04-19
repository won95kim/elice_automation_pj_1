import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    
    # 🌟 성능 최적화 옵션 추가
    chrome_options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
    chrome_options.add_argument("--disable-popup-blocking")  # 팝업 차단 해제
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화 (리소스 절약)
    chrome_options.add_argument("--headless")  # GUI 없이 실행 (젠킨스용)
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (속도 향상)
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 해제 (메모리 최적화)
    chrome_options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 설정
    chrome_options.add_argument("--log-level=3")  # 로그 레벨 낮춰 불필요한 출력 줄이기
    chrome_options.add_argument("--window-size=1920,1080")  # 창 사이즈 조절
    chrome_options.page_load_strategy = "eager"  # 빠른 페이지 로드

    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.delete_all_cookies() # 전체 쿠키 삭제
    driver.implicitly_wait(5)  # 암시적 대기 추가 (요소 로딩 기다리기)

    yield driver
    
    driver.quit()