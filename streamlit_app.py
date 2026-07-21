import time
import streamlit as st

st.set_page_config(page_title="pomo Timer", page_icon="🖊")

# ----------------------------
# 初回だけ状態を作るll
# ----------------------------
if "focus_minutes" not in st.session_state:
    st.session_state.focus_minutes = 25

if "break_minutes" not in st.session_state:
    st.session_state.break_minutes = 5

if "mode" not in st.session_state:
    st.session_state.mode = "Focus"

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = (
        st.session_state.focus_minutes * 60
    )

if "running" not in st.session_state:
    st.session_state.running = False

if "completed_focus" not in st.session_state:
    st.session_state.completed_focus = 0

if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

# ----------------------------
# サイドバー
# ----------------------------
st.sidebar.title("時間設定")

new_focus = st.sidebar.slider(
    "集中時間（分）",
    1,
    60,
    st.session_state.focus_minutes,
)

new_break = st.sidebar.slider(
    "休憩時間（分）",
    1,
    30,
    st.session_state.break_minutes,
)

# タイマー停止中だけ時間設定を反映
if not st.session_state.running:
    if new_focus != st.session_state.focus_minutes:
        st.session_state.focus_minutes = new_focus
        if st.session_state.mode == "Focus":
            st.session_state.remaining_seconds = new_focus * 60

    if new_break != st.session_state.break_minutes:
        st.session_state.break_minutes = new_break
        if st.session_state.mode == "Break":
            st.session_state.remaining_seconds = new_break * 60

# ----------------------------
# タイマー更新
# ----------------------------
now = time.time()

if st.session_state.running:
    elapsed = int(now - st.session_state.last_time)

    if elapsed > 0:
        st.session_state.remaining_seconds -= elapsed
        st.session_state.last_time = now

    if st.session_state.remaining_seconds <= 0:

        # 集中終了
        if st.session_state.mode == "Focus":
            st.session_state.completed_focus += 1
            st.success("🎉 集中時間が終了しました。休憩しましょう！")

            st.session_state.mode = "Break"
            st.session_state.remaining_seconds = (
                st.session_state.break_minutes * 60
            )

        # 休憩終了
        else:
            st.success("✨ 休憩終了です。集中を始めましょう！")

            st.session_state.mode = "Focus"
            st.session_state.remaining_seconds = (
                st.session_state.focus_minutes * 60
            )

# ----------------------------
# 表示
# ----------------------------
st.title("🖊 pomo Timer")

st.subheader(f"現在：{st.session_state.mode}")

minutes = st.session_state.remaining_seconds // 60
seconds = st.session_state.remaining_seconds % 60

st.markdown(
    f"<h1 style='text-align:center;font-size:70px;'>{minutes:02}:{seconds:02}</h1>",
    unsafe_allow_html=True,
)

st.write(f"✅ 完了した集中回数：{st.session_state.completed_focus}")

# ----------------------------
# ボタン
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("開始"):
        st.session_state.running = True
        st.session_state.last_time = time.time()

with col2:
    if st.button("一時停止"):
        st.session_state.running = False

with col3:
    if st.button("リセット"):
        st.session_state.running = False
        st.session_state.mode = "Focus"
        st.session_state.remaining_seconds = (
            st.session_state.focus_minutes * 60
        )

# ----------------------------
# 動作中は約0.2秒ごとに画面更新
# ----------------------------
if st.session_state.running:
    time.sleep(0.2)
    st.rerun()