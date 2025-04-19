# 🍱 직장인의 점심 고민을 해결하는 AI 메뉴 추천 서비스 테스트

## 🧑‍🤝‍🧑 팀 정보
- 팀명: **일단박아보자!!!**  
- 좌우명: _Python과 GPT만 있다면 어디든 갈 수 있어_  
- 팀원: 조선동(팀장), 이수빈, 김수진, 황인철, 김혜원  
  

## 🎯 프로젝트 개요
**‘오늘 뭐 먹지?’**는 직장인을 위한 AI 기반의 점심/회식 메뉴 추천 서비스입니다.  
본 프로젝트는 해당 서비스의 주요 기능에 대해 테스트를 설계하고,  
**Selenium, Pytest, Jenkins**를 활용해 자동화 테스트 및 CI 환경을 구축한 협업 프로젝트입니다.

- **진행 기간:** 2025.03.21 ~ 2025.04.03  
- **목표:** 주요 기능의 테스트 자동화 및 반복 테스트 효율화  
- **기여:** 테스트 케이스 설계, 자동화 스크립트 구현, Jenkins 연동 등 협업 기반 QA 업무 수행  
  

## 💡 팀별 역할
- **회원가입 / 로그인 / 인적사항 작성 기능:** 김혜원  
- **홈 기능:** 황인철  
- **팀 피드 기능:** 이수빈  
- **히스토리 기능:** 김수진  
- **개인 피드 기능:** 조선동  
  

## ✅ 테스트 목표
- 주요 기능(UI/기능)에 대한 테스트 케이스 작성  
- Selenium과 Pytest를 활용한 테스트 자동화  
- Jenkins를 활용한 CI 환경 구축 및 테스트 리포트 자동화  
  

## 🔧 기술 스택
- **언어:** Python  
- **테스트 프레임워크:** Pytest  
- **웹 자동화:** Selenium  
- **CI 도구:** Jenkins (pytest-html 리포트 출력)  
- **협업:** Git / Notion / Google Spreadsheet 
  

## 🗂️ 파일 구조
.gitignore              # Git에 포함되지 않을 파일/폴더 목록  
pytest.ini              # Pytest 설정 파일  
README.md               # 프로젝트 설명 문서  
requirements.txt        # 필요한 라이브러리 목록  

reports/                # 테스트 보고서 및 로그 (Git 무시 대상)  
├── logs/               # 테스트 실행 시 생성된 로그  
└── screenshots/        # 실패 테스트 시 캡처된 스크린샷  

src/                    # 테스트 관련 소스 코드  
├── resources/          # 리소스 파일들  
│   └── testdata/       
│       └── account.json # 테스트용 계정 정보 (Git 무시 대상)  
├── config/             # 설정 및 환경 파일 (Git 무시 대상)  
│   ├── .env  
│   ├── config.py  
│   └── sky.jpg         # 테스트용 이미지  
├── pages/              # 페이지 단위 모듈  
│   ├── history_page.py  
│   ├── login_pagy.py  
│   ├── mainpage.py  
│   ├── mypage.py  
│   ├── signup_page.py  
│   ├── team_page.py  
│   └── welcome_page.py  
└── utils/              # 공통 유틸리티 함수  
    └── helpers.py  

tests/                  # 테스트 코드  
├── __init__.py  
├── conftest.py  
├── test_history_page.py  
├── test_login_pagy.py  
├── test_mainpage.py  
├── test_mypage.py  
├── test_signup_page.py  
├── test_team_page.py  
└── test_welcome_page.py  
  

## 📊 테스트 케이스 요약
| Page Name     | Total TCs | Executed TCs | Execution Rate | PASS | FAIL | N/A |  
|---------------|-----------|---------------|----------------|------|------|-----|  
| Signup Page   | 11        | 11            | 100%           | 10   | 1    | 0   |  
| Welcome Page  | 26        | 26            | 100%           | 23   | 3    | 0   |  
| Login Page    | 19        | 19            | 100%           | 18   | 1    | 0   |  
| Home Page     | 13        | 13            | 100%           | 13   | 0    | 0   |  
| Team Page     | 16        | 16            | 100%           | 15   | 1    | 0   |  
| History Page  | 16        | 16            | 100%           | 16   | 0    | 0   |  
| My Page       | 11        | 11            | 100%           | 11   | 0    | 0   |  
| **Total**     | **112**   | **112**       | **100%**       | **106** | **6** | **0** |  
  

## 🧪 자동화 테스트 방식
- Pytest 기반 테스트 코드로 시나리오 구현  
- Selenium으로 UI 자동화  
- Jenkins에 연동하여 Pull 시 테스트 자동 수행 및 리포트 출력  
  

## 📝 프로젝트 산출물
| 항목 | 내용 |  
|------|------|  
| ✅ 테스트 케이스 | [스프레드시트 바로가기](https://docs.google.com/spreadsheets/d/147I40EIpwn0MUDYqUeM1B9GABHnUmOLrPAJ-vThpZIo/edit?usp=sharing) |  
| 🧪 자동화 코드 | [GitHub Repository](https://github.com/won95kim/elice_automation_pj_1) |  
| 📊 테스트 리포트 | Jenkins에서 Pytest 실행 후 자동 생성된 `pytest-html` 기반 리포트 확인 가능 |
  
  
## ✨ 프로젝트 회고
- 테스트 자동화 경험을 통해 실무 QA 환경을 체험  
- 테스트 시나리오 도출, 오류 탐지 및 리포트 작성 역량 향상  
- Git을 활용한 브랜치 전략 및 협업 방식에 대한 이해 증진
