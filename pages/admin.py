import streamlit as st
import os
import json

UPLOAD_DIR = "upload"
META_FILE = os.path.join(UPLOAD_DIR, "meta.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 메타데이터(제목) 저장/불러오기 함수
def load_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_meta(meta):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def main():
    st.title("이미지 업로드")
    meta = load_meta()

    st.subheader("이미지 업로드 및 제목 입력")
        uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    title = st.text_input("이미지 제목을 입력하세요")
    if uploaded_file and title:
                save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
        meta[uploaded_file.name] = title
        save_meta(meta)
        st.success(f"'{uploaded_file.name}' 업로드 및 제목 저장 완료!")
                st.rerun()
    elif uploaded_file and not title:
        st.info("제목을 입력해야 업로드가 완료됩니다.")
        
        st.subheader("업로드된 이미지 목록")
        image_files = sorted([
            f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        if image_files:
            cols = st.columns(3)
            for idx, img_file in enumerate(image_files):
                with cols[idx % 3]:
                    img_path = os.path.join(UPLOAD_DIR, img_file)
                caption = meta.get(img_file, "(제목 없음)")
                # 제목 수정 입력창 (그림 위에)
                new_title = st.text_input(f"제목 수정: {img_file}", value=caption, key=f"title_{img_file}")
                if new_title != caption:
                    meta[img_file] = new_title
                    save_meta(meta)
                    st.success(f"'{img_file}' 제목이 수정되었습니다.")
                    st.rerun()
                st.image(img_path, caption=None, use_container_width=True)
                st.markdown(f"<div style='text-align:center; font-weight:bold; margin-bottom:8px;'>{new_title}</div>", unsafe_allow_html=True)
                    if st.button(f"삭제: {img_file}", key=f"del_{img_file}"):
                            os.remove(img_path)
                    meta.pop(img_file, None)
                    save_meta(meta)
                            st.success(f"'{img_file}' 삭제 완료!")
                            st.rerun()
    else:
        st.info("업로드된 이미지가 없습니다.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="이미지 업로드",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main() 