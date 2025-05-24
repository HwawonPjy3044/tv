import streamlit as st
import os
from PIL import Image
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
import datetime
import time
import json

# 설정
UPLOAD_DIR = "upload"
META_FILE = os.path.join(UPLOAD_DIR, "meta.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 페이지 설정
st.set_page_config(
    page_title="게시판",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 관리자 링크 추가
st.markdown("""
    <style>
        /* 기존 스타일 유지 */
        .admin-link {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 999;
        }
        .admin-link a {
            color: #666;
            text-decoration: none;
            font-size: 0.9rem;
        }
        .admin-link a:hover {
            color: #000;
        }
        .block-container {
            padding-top: 0rem !important;
        }
        
        /* 헤더 가운데 정렬 스타일 추가 */
        h1, h2, h3 {
            text-align: center !important;
            margin-bottom: 1rem !important;
        }
        /* Streamlit의 기본 헤더 스타일 오버라이드 */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            text-align: center !important;
        }
    </style>
    <div class="admin-link">
        <a href="/admin" target="_self">관리자</a>
    </div>
""", unsafe_allow_html=True)

# 자동 새로고침 설정 (10초마다)
refresh_count = st_autorefresh(interval=10000, key="main_refresh")
current_section = refresh_count % 4  # 5에서 4로 변경 (일정 섹션 제거)

def show_notice():
    st.header("공지사항")
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1iXSiQygopPUm0m9_B7-aX73uAjBy1cQuVhtKpNibgzQ/export?format=csv"
        df = pd.read_csv(sheet_url)
        df_checked = df[df[df.columns[2]] == True].head(5)  # 최대 5개 공지사항만 표시
        
        if len(df_checked) == 0:
            st.info("")
            return
            
        for idx, row in df_checked.iterrows():
            st.markdown(f"<div style='font-size:2rem; margin-bottom:1rem;'><b>{row[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;{row[1]}</div>", unsafe_allow_html=True)
            if idx < len(df_checked) - 1:  # 마지막 항목이 아닐 경우에만 구분선 표시
                st.divider()
    except Exception as e:
        st.error(f"공지사항을 불러올 수 없습니다: {e}")

def show_meal():
    # 오늘 날짜 + 점심
    today = datetime.datetime.today().strftime('%Y-%m-%d')  # 오늘 날짜 (YYYY-MM-DD)
    st.header(f"{today}일   점심 메뉴")
    try:
        API_KEY = "2a5d3d5355ce49dcb4e1a9273d04e629"
        ATPT_OFCDC_SC_CODE = "D10"
        SD_SCHUL_CODE = "7240209"
        today_api = datetime.datetime.today().strftime('%Y%m%d')  # 오늘 날짜 (YYYYMMDD)

        url = (
            f"https://open.neis.go.kr/hub/mealServiceDietInfo"
            f"?KEY={API_KEY}&Type=json&pIndex=1&pSize=1"
            f"&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}"
            f"&SD_SCHUL_CODE={SD_SCHUL_CODE}"
            f"&MLSV_YMD={today_api}"
        )

        response = requests.get(url)
        data = response.json()

        if (
            'mealServiceDietInfo' in data and
            len(data['mealServiceDietInfo']) > 1 and
            'row' in data['mealServiceDietInfo'][1] and
            len(data['mealServiceDietInfo'][1]['row']) > 0
        ):
            row = data['mealServiceDietInfo'][1]['row'][0]
            menu = row.get('DDISH_NM', '').replace('<br/>', '\n')
            calorie = row.get('CAL_INFO', '정보 없음')
            nutrition = row.get('NTR_INFO', '정보 없음')
            allergy = row.get('ALLERGY_INFO', '정보 없음')

            # 날짜 포맷 변경
            date_str = f"{today_api[:4]}-{today_api[4:6]}-{today_api[6:]}"
           # st.subheader(f"{date_str} 급식 메뉴")
            # 메뉴를 이미지 제목만큼 크게, 가운데 정렬
            st.markdown(f"<div style='text-align:center; font-weight:bold; font-size:2.2rem; margin-bottom:16px;'>{menu}</div>", unsafe_allow_html=True)
            st.write(f"**칼로리:** {calorie}")
            st.write(f"**영양성분:** {nutrition}")
            st.write(f"**알레르기 번호:** {allergy}")
            st.caption("※ 알레르기 번호는 식단 옆 괄호와 함께 표시됩니다. 번호별 상세는 NEIS 알레르기 표 참고.")
        else:
            st.info("오늘의 급식 정보가 없습니다.")
    except Exception as e:
        st.error(f"급식 정보를 불러올 수 없습니다: {e}")

def show_photos():
    st.markdown("""
        <style>
            .photo-container {
                margin-top: -12rem !important;  /* -6rem에서 -12rem으로 변경하여 더 위로 올림 */
            }
            .photo-title {
                margin-bottom: 0.5rem !important;
                text-align: center;
                font-weight: bold;
                font-size: 2.2rem;
            }
            .block-container {
                padding-top: 0 !important;
                margin-top: -4rem !important;  /* -2rem에서 -4rem으로 변경하여 전체 컨테이너를 더 위로 올림 */
            }
            /* Streamlit의 기본 여백 제거 */
            .main > div {
                padding-top: 0 !important;
            }
            /* 헤더 영역 여백 제거 */
            header {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    image_files = sorted([
        f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
    meta = load_meta()

    if image_files:
        photo_refresh = st_autorefresh(interval=3000, key="photo_refresh")
        index = photo_refresh % len(image_files)
        img_file = image_files[index]
        img_path = os.path.join(UPLOAD_DIR, img_file)
        title = meta.get(img_file, os.path.splitext(img_file)[0])
        
        st.markdown('<div class="photo-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'<div class="photo-title">{title}</div>', unsafe_allow_html=True)
            st.image(img_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("이미지를 업로드하면 슬라이드가 시작됩니다.")

def show_video():
    #st.header("영상")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# 현재 섹션에 따라 해당 내용 표시
if current_section == 0:
    show_notice()
elif current_section == 1:
    show_meal()
elif current_section == 2:
    show_photos()
else:
    show_video()


