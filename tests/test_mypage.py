import time
import pytest
import os
from src.utils.helpers import Utils
from src.pages.mypage import MyPage
from dotenv import load_dotenv

load_dotenv("src/config/.env")

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

@pytest.fixture
def setup(driver):
    mypage = MyPage(driver)
    helpers = Utils(driver)
    #로그인
    helpers.utils_login(EMAIL, PASSWORD)
    return mypage, helpers

class TestMyPage:
    
    #개인피드 프로필 수정 (슬라이더 랜덤 값) + 정상 프로필 수정
    #@pytest.mark.skip(reason="다른 테스트를 위해")
    def test_profile(self, setup):
        mypage, helpers = setup

        #네비게이션 바 이동
        helpers.utils_nevigationbar('개인 피드')
        time.sleep(1)

        #연필모양 아이콘 클릭
        mypage.pencil_icon()
        time.sleep(1)
        #프로필 이미지 삽입
        mypage.file_input()
        #슬라이더 랜덤 변수 이동
        mypage.slider_move()
        #텍스트 입력
        mypage.good_text_input("저는 매운 음식을 좋아합니다.")
        mypage.bad_text_input("저는 짠 음식을 싫어합니다.")
        #프로필 수정 완료 버튼 클릭
        mypage.submit_btn("프로필 수정 완료")

        #프로필 수정 확인
        time.sleep(2)
        mypage.profile_check("저는 매운 음식을")
    
    #2번째 프로필 수정 (슬라이더 값 정해주기) + 유효성 검사 추가(텍스트 공란으로 두기)
    #@pytest.mark.skip(reason="다른 테스트를 위해")
    def test_edit_profile(self, setup):
        mypage, helpers = setup

        #네비게이션 바 이동
        helpers.utils_nevigationbar('개인 피드')
        time.sleep(1)

        #연필모양 아이콘 클릭
        mypage.pencil_icon()
        time.sleep(1)
        #프로필 이미지 삽입
        mypage.file_input()
        #슬라이더 입력값 변수 이동
        mypage.input_slider_move(3.2,4.0,1.4)
        #텍스트 입력
        mypage.good_text_input("")
        mypage.bad_text_input("")
        #프로필 수정 완료 버튼 클릭
        mypage.submit_btn("프로필 수정 완료")

        #유효성 검사
        mypage.valid_text()
        
        time.sleep(2)
        #프로필 수정 확인
        mypage.profile_check("1.4")

    #개인피드 후기 작성 (정상적 후기) , 후기 작성 완료 확인
    #@pytest.mark.skip(reason="다른 테스트를 위해")        
    def test_review(self,setup):
        mypage, helpers = setup

        helpers.utils_nevigationbar('개인 피드')
        time.sleep(1)

        #스크롤 이동 함수
        mypage.scroll(300)

        # +아이콘 클릭 함수
        mypage.plus_icon()
        time.sleep(1)
        #라디오 업로드 함수
        mypage.radio_pick("혼밥")
        #파일 업로드 함수
        mypage.file_input()
        #메뉴 업로드 함수
        mypage.menu_input("거위")
        #카테고리 업로드 함수
        mypage.category_input()
        #후기 업로드 함수
        mypage.review_input("후기를 뭐라고 써야할지 모르겠어요")
        #별 1~5개 랜덤으로 업로드 함수
        mypage.star_input()
        #후기 작성 완료
        time.sleep(1)
        mypage.submit_btn("후기 작성 완료")

        #리뷰체크하기
        mypage.review_check("거위")

    #후기작성시 빠트린 문장 있는지 유효성 검사
    #@pytest.mark.skip(reason="다른 테스트를 위해") 
    def test_valid_review(self,setup):
            mypage, helpers = setup

            helpers.utils_nevigationbar('개인 피드')
            time.sleep(1)

            mypage.scroll(300)

            # +아이콘 클릭 함수
            mypage.plus_icon()
            time.sleep(1)
            #라디오 업로드 함수
            #mypage.radio_pick("혼밥")
            #파일 업로드 함수
            #mypage.file_input()
            #time.sleep(1)
            #메뉴 업로드 함수
            #mypage.menu_input("거위")
            #카테고리 업로드 함수
            #mypage.category_input()
            #후기 업로드 함수
            #mypage.review_input("후기를 뭐라고 써야할지 모르겠어요")
            #별 1~5개 랜덤으로 업로드 함수
            #mypage.star_input()
            #후기 작성 완료
            mypage.submit_btn("후기 작성 완료")
            time.sleep(1)

            #유효성 검사 함수
            mypage.valid_value()
            time.sleep(1)

            #리뷰체크하기
            mypage.review_check("오리")


    #팀 피드로 들어가 +아이콘 눌러서 정상 후기 작성 및 후기 작성 확인
    #@pytest.mark.skip
    def test_team(self,setup):
        mypage, helpers = setup

        time.sleep(2)
        helpers.utils_nevigationbar('팀 피드')
        time.sleep(1)

        # 스크롤 내리기
        mypage.scroll(600)
        time.sleep(2)

        # +아이콘 클릭
        mypage.plus_icon()
        time.sleep(1)
            
        #라디오 업로드 함수
        mypage.radio_pick("혼밥")
        #파일 업로드 함수
        mypage.file_input()
        #메뉴 업로드 함수
        mypage.menu_input("오리")
        #카테고리 업로드 함수 + 팀 카테고리는 요소가 두개라 두번째꺼 사용
        mypage.team_category_input()
        #후기 업로드 함수
        mypage.review_input("후기를 뭐라고 써야할지 모르겠어요")
        #별 1~5개 랜덤으로 업로드 함수
        mypage.star_input()
        #후기 작성 완료
        time.sleep(1)
        mypage.submit_btn("후기 작성 완료")

        #리뷰체크하기
        mypage.review_check("오리")

    #팀 피드로 들어가 +아이콘 눌러서 후기 작성 + 입력값 공란일 경우 유효성검사 및 후기작성 확인
    #@pytest.mark.skip
    def test_edit_team(self,setup):
        mypage, helpers = setup

        time.sleep(2)
        helpers.utils_nevigationbar('팀 피드')
        time.sleep(1)

        # 스크롤 내리기
        mypage.scroll(600)
        time.sleep(2)

        # +아이콘 클릭
        mypage.plus_icon()
        time.sleep(1)
            
        #라디오 업로드 함수
        #mypage.radio_pick("혼밥")
        #파일 업로드 함수
        #mypage.file_input()
        #메뉴 업로드 함수
        #mypage.menu_input("오리")
        #카테고리 업로드 함수 + 팀 카테고리는 요소가 두개라 두번째꺼 사용
        #mypage.team_category_input()
        #후기 업로드 함수
        #mypage.review_input("후기를 뭐라고 써야할지 모르겠어요")
        #별 1~5개 랜덤으로 업로드 함수
        #mypage.star_input()
        #후기 작성 완료
        #time.sleep(1)
        mypage.submit_btn("후기 작성 완료")

        time.sleep(2)
        mypage.team_valid_value()

        #리뷰체크하기
        mypage.review_check("오리")

    #개인 피드에서 리뷰 중 같은 메뉴 먹기 후기작성, 유효성 검사, 후기 작성 확인
    def test_same_review(self,setup):
            mypage, helpers = setup
            
            #네비게이션 바 개인피드
            helpers.utils_nevigationbar('개인 피드')
            time.sleep(1)

            #스크롤내리기
            mypage.scroll(600)
            
            #같은 메뉴 먹기 클릭
            mypage.same_review()
            time.sleep(1)

            #라디오 업로드 함수
            mypage.radio_pick("혼밥")
            #별 1~5개 랜덤으로 업로드 함수
            mypage.star_input()
            time.sleep(1)
            mypage.submit_btn("후기 작성 완료")

            #유효성 검사
            mypage.valid_value()

            #후기 작성 확인
            mypage.review_check("혼밥")