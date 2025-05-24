import streamlit as st
import os
from PIL import Image
import shutil

# 설정
UPLOAD_DIR = "upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 페이지 설정
st.set_page_config(
    page_title="이미지 업로드",
    layout="wide"
)

st.title("이미지 업로드")

# 이미지 업로드
uploaded_files = st.file_uploader(
    "이미지 파일을 선택하세요 (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # 파일 저장
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 이미지 최적화
        try:
            img = Image.open(file_path)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            img.save(file_path, "JPEG", quality=85, optimize=True)
            st.success(f"{uploaded_file.name} 업로드 완료")
        except Exception as e:
            st.error(f"{uploaded_file.name} 처리 중 오류 발생: {e}")

# 현재 업로드된 이미지 목록
st.subheader("현재 업로드된 이미지")
image_files = sorted([
    f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

if image_files:
    cols = st.columns(4)
    for idx, image_file in enumerate(image_files):
        with cols[idx % 4]:
            st.image(os.path.join(UPLOAD_DIR, image_file), caption=image_file)
            if st.button(f"삭제: {image_file}", key=f"del_{image_file}"):
                try:
                    os.remove(os.path.join(UPLOAD_DIR, image_file))
                    st.success(f"{image_file} 삭제 완료")
                    st.rerun()
                except Exception as e:
                    st.error(f"삭제 중 오류 발생: {e}")
else:
    st.info("업로드된 이미지가 없습니다.")

# 전체 삭제 버튼
if st.button("모든 이미지 삭제"):
    if st.checkbox("정말로 모든 이미지를 삭제하시겠습니까?"):
        try:
            shutil.rmtree(UPLOAD_DIR)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            st.success("모든 이미지가 삭제되었습니다.")
            st.rerun()
        except Exception as e:
            st.error(f"삭제 중 오류 발생: {e}") 