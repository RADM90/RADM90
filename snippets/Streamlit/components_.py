import streamlit as st
import streamlit.components.v1 as components

st.title("보행 시 장애물 안내 서비스")

st.write("Session ID : {SESSION_ID}")

placeholder = st.empty()

upload_place = st.empty()
uploaded_file = upload_place.file_uploader("동영상을 선택하세요", type=["mp4"])
fn = uploaded_file.name.replace(" ", "_")
with open("{save_filepath}", 'wb') as f:
    f.write(uploaded_file.getbuffer())
    placeholder.success(f"파일이 서버에 저장되었습니다.")

col_slide, col_button = st.columns([2, 1])
slide_value = col_slide.slider("Confidence Lv Threshold", min_value=0.1, max_value=1.0, value=0.25, step=0.05)
button_value = col_button.button("Start Process")

with st.spinner("동영상 전처리 중..."):
    video_preprocessing(save_filepath, preprocessed_file, resize_h=640, tgt_framerate=TARGET_FPS)

components.html(f"""
                  <div class="container">
                    <video controls preload="auto" width="{container_w}" autoplay crossorigin="anonymous">
                      <source src="http://{EXTERNAL_IP}:30002/{user_session}/video" type="video/mp4"/>
                      <track src="http://{EXTERNAL_IP}:30002/{user_session}/subtitle" srclang="ko" type="text/{subtitle_ext}" default/>
                  </video>
                  </div>
                """, width=container_w, height=int(container_w / 16 * 9))