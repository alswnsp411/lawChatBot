import streamlit as st
import base64
import os
import team_intro 
import service_intro
from src.components.main_css_loader import load_main_css
from src.components.main_html_loader import render_html, render_horizontal_line

# 페이지 설정
st.set_page_config(
    page_title="AI 법률 서비스 사고닷",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 로드 
base_dir = os.path.dirname(os.path.abspath(__file__))
load_main_css(base_dir)

# DB 구성
from databases import baseSource
conn = baseSource.init()
conn = baseSource.connect()
cursor = conn.cursor()

# 리디렉션 처리 (최상단에 배치)
if 'redirect_page' in st.session_state:
    redirect_page = st.session_state.redirect_page
    
    # 먼저 조회수 업데이트
    if redirect_page == "ai_consultation":
        baseSource.updateView("user_view")
    elif redirect_page == "law_report":
        baseSource.updateView("report_view")
    
    # 세션에서 제거
    del st.session_state.redirect_page
    
    # 페이지 이동 (마지막에 실행)
    if redirect_page == "ai_consultation":
        st.switch_page("pages/ai_chatbot.py")
    elif redirect_page == "law_report":
        st.switch_page("pages/ai_report.py")
    elif redirect_page == "guestbook":
        st.switch_page("pages/guestbook.py")

# 이미지를 base64로 인코딩하는 함수
def get_image_as_base64(file_path):
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# 사이드바
with st.sidebar:
    st.image("images/저울.webp", width=100)
    st.title("AI 법률 서비스 사고닷")
    st.markdown('<p>AI와 법률 전문가가 함께하는 스마트 법률 서비스.<br>승리를 만드는 길, 사고닷과 함께 준비하세요.</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # 메뉴란 대신 버튼으로 대체
    st.subheader("소개합니다")
    show_services = st.button("👩🏻‍⚖️ 우리 서비스 소개")
    show_team = st.button("☀️ 우리 팀 소개")
    show_home = st.button("🏠 홈 돌아가기")
    
    st.divider()
    
    # 연락처 정보
    st.caption("고객센터: 02-1004-1004")
    st.caption("이메일: happy6team@skala.com")
    st.caption("운영시간: 연중무휴 24시간!")

# 세션 상태로 현재 페이지 관리
if 'current_page' not in st.session_state:
    st.session_state.current_page = "홈"

# 버튼 클릭에 따라 페이지 상태 변경
if show_home:
    st.session_state.current_page = "홈"
if show_team:
    st.session_state.current_page = "우리 팀 소개"
if show_services:
    st.session_state.current_page = "우리 서비스 소개"

# 홈 화면
if st.session_state.current_page == "홈":
    # 헤더 표시
    render_html(base_dir, "main_header.html")
    
    # 서비스 소개 제목
    render_html(base_dir, "main_services_title.html")
    
    # 카드 스타일을 폼으로 대체
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # AI 법률 상담 폼
        with st.form(key="ai_consultation_form"):
            service_values = {
                "icon": "💬",
                "title": "실시간 AI 법률 상담",
                "description": "AI 법률 비서가 실시간으로 법률 상담을 제공합니다.<br>간단한 법률 질문부터 검색까지 신속하게 답변해 드립니다."
            }
            render_html(base_dir, "main_service_card.html", service_values)
            submit_button = st.form_submit_button("바로가기", use_container_width=True)
            
            if submit_button:
                st.session_state.redirect_page = "ai_consultation"
                st.rerun()
    
    with col2:
        # 법률 자문 보고서 폼
        with st.form(key="law_report_form"):
            service_values = {
                "icon": "📝",
                "title": "AI 법률 보고서 + 변호사 매칭",
                "description": "케이스에 맞는 맞춤형 법률 자문 보고서를 생성합니다.<br>이를 바탕으로 국내 최고의 변호사들과 바로 연결됩니다."
            }
            render_html(base_dir, "main_service_card.html", service_values)
            submit_button = st.form_submit_button("바로가기", use_container_width=True)
            
            if submit_button:
                st.session_state.redirect_page = "law_report"
                st.rerun()

    with col3:
        # 방명록 폼
        with st.form(key="guestbook_form"):
            service_values = {
                "icon": "📋",
                "title": "방명록",
                "description": "서비스에 대해 자유롭게 의견을 남길 수 있는 공간입니다.<br>방명록을 작성하거나 '좋아요'를 눌러보세요!"
            }
            render_html(base_dir, "main_service_card.html", service_values)
            submit_button = st.form_submit_button("바로가기", use_container_width=True)
            
            if submit_button:
                st.session_state.redirect_page = "guestbook"
                st.rerun()
    
    # 구분선
    render_horizontal_line()
    
    # 변호사 소개 제목
    render_html(base_dir, "main_lawyers_title.html")
    
    # 변호사 정보와 이미지 정의
    lawyers = [
        {"name": "손지영", "specialty": '"백전 백승, 무패의 전설<br>상대가 누구든 다 뿌셔드립니다."<br><br>• 성격: ENTJ (의뢰인에게도 화낼 수 있음 주의)<br><br>• 대원한국어고등학교 졸업 (2005)<br>• 한국대학교 물리학과 학사 (2010)<br>• 한국대학교 법학전문대학교 법학전문 석사 (2013)<br>• 김앤손 법률 사무소 (2008 ~ 2015)<br>• 사고닷 법률 사무소 (2015 ~ 현재)<br>', "image": "images/손지영.png"},
        {"name": "이재웅", "specialty": '"자신이 없습니다. 질 자신이.<br>가장 확실한 해결책, 포기 없는 변호."<br><br>• 성격 : INFJ (근데 사실 T임)<br><br>• 한국대학교 법학전문대학학원<br>(법학스칼라전문박사, 박사 졸업, 2018)<br>• 너뭐대학교<br>(한국사, 문학과, 수석 졸업, 2015)<br>• 사고닷 법률 사무소 (2016 - 현재)', "image": "images/이재웅.png"},
        {"name": "김다은", "specialty": '"시켜줘 그럼, SKALA 명예 변호사"<br><br>• 성격: ESTJ (인성은 글쎄? 근데 이기면 되잖아)<br><br>• 내 머리는 너무나 나빠서 너 하나밖에 난 모른대학교<br>(법학스칼라전문박사, 박사 졸업, 2016)<br>• 하버드 법학대학원 (법학 박사, 2005)<br>• 국제 법률 자문관 (2015 - 2025)<br>• 사고닷 법률 사무소 변호사 (2016 - 현재)<br>• SKALA 명예 변호사로 활동 (2018 - 현재)<br>', "image": "images/김다은.png"},
        {"name": "진실", "specialty": '"믿음, 소망, 사랑, 그중에 제일은 사랑이라.<br>이혼 전문 맡겨만 주세요."<br><br>• 성격: ISFP (공감 잘함. 의뢰인과 울음 대결 가능)<br><br>• 제9회 변호사시험 합격 (2020)<br>• 한국대학교 법학전문대학원<br>(법학스칼라전문석사, 수석졸업, 2020)<br>• 두번 다시 사랑모대학교<br>(문학사, 서양사학, 수석졸업, 2017)<br>• 사고닷 법률사무소 (2020-현재)', "image": "images/진실.png"},
        {"name": "김민주", "specialty": '"법과 정의, 그리고 사람. <br>혼자가 아닌 서비스를 제공하기 위해 최선을 다하겠습니다."<br><br>• 성격: ENFP (긍정적 사고 전문)<br><br>• 제 7회 변호사시험 합격 (2007)<br>• 비빔대학교 법학전문대학원 (법학전문석사, 수석 졸업, 2007)<br>• 비빔대학교 (법학/문학, 수석 졸업, 2005)<br>• 사고닷 법률사무소 (2020 - 현재)<br>', "image": "images/김민주.png"},
        {"name": "이효정", "specialty": '"오직 노동자만을 위한<br>노동자의, 노동자에 의한, 노동자를 위한 법률 서비스"<br><br>• 성격: INTJ (노동자에게만 F)<br><br>• 한국대학교(법학, 2020)<br>• 한국대학교 법학전문대학원(법학전문석사, 2023)<br>• 한국노동교육원 법률 자문(2023 - 현재)<br>• 사고닷 법률 사무소(2024 - 현재)', "image": "images/이효정.png"}
    ]
    
    # 2행 3열로 변경
    # 첫 번째 행 (변호사 0, 1, 2)
    row1_cols = st.columns(3)
    
    for i in range(3):
        lawyer = lawyers[i]
        img_path = lawyer["image"]
        img_base64 = get_image_as_base64(img_path)
        
        if img_base64:
            img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width:100%; height:100%; object-fit:cover;">'
        else:
            # 이미지가 없을 경우 기본 아이콘 사용
            gender_icon = "👩‍⚖️" if lawyer["name"] not in ["이재웅"] else "👨‍⚖️"
            img_html = f'<span style="font-size: 30px;">{gender_icon}</span>'
        
        profile_values = {
            "image": img_html,
            "name": lawyer["name"],
            "specialty": lawyer["specialty"]
        }
        
        with row1_cols[i]:
            render_html(base_dir, "main_profile_card.html", profile_values)
    
    # 첫 번째 행과 두 번째 행 사이의 간격 추가
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # 두 번째 행 (변호사 3, 4, 5)
    row2_cols = st.columns(3)
    
    for i in range(3, 6):
        lawyer = lawyers[i]
        img_path = lawyer["image"]
        img_base64 = get_image_as_base64(img_path)
        
        if img_base64:
            img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width:100%; height:100%; object-fit:cover;">'
        else:
            # 이미지가 없을 경우 기본 아이콘 사용
            gender_icon = "👩‍⚖️" if lawyer["name"] not in ["이재웅"] else "👨‍⚖️"
            img_html = f'<span style="font-size: 30px;">{gender_icon}</span>'
        
        profile_values = {
            "image": img_html,
            "name": lawyer["name"],
            "specialty": lawyer["specialty"]
        }
        
        with row2_cols[i-3]:
            render_html(base_dir, "main_profile_card.html", profile_values)
    
    # 구분선
    render_horizontal_line()
    
    # 통계 섹션
    render_html(base_dir, "main_statistics_title.html")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'user_view'")
        user_view = cursor.fetchall()[0][0]
        st.metric(label="누적 상담 건수", value=user_view)
        conn.commit()
        
    with col2:
        cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'report_view'")
        report_view = cursor.fetchall()[0][0]
        st.metric(label="누적 보고서 생성 수", value=report_view)
        conn.commit()
    
    with col3:
        cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'total_view'")
        total_view = cursor.fetchall()[0][0]
        st.metric(label="총 누적 사용 수", value=total_view)
        conn.commit()

# 우리 팀 소개 페이지
elif st.session_state.current_page == "우리 팀 소개":
    # ✅ `team_intro.py`의 내용을 실행하여 현재 페이지를 "우리 팀 소개"로 변경
    team_intro.show_team_page()
    
# 우리 서비스 소개 페이지
elif st.session_state.current_page == "우리 서비스 소개":
    service_intro.show_service_page()

# 모든 페이지에 공통으로 표시되는 푸터
render_html(base_dir, "main_footer.html")