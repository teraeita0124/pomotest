import time
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="ポモドーロタイマー", page_icon="🍅")

# -------------------------
# 初回だけ状態を作る
# -------------------------
if "focus_minutes" not in st.session_state:
    st.session_state.focus_minutes = 25

if "break_minutes" not in st.session_state:
    st.session_state.break_minutes = 5

if "mode" not in st.session_state:
    st.session_state.mode = "集中"

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 25 * 60

if "running" not in st.session_state:
    st.session_state.running = False

if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0

# -------------------------
# サイドバー
# -------------------------
st.sidebar.title("時間設定")

focus_time = st.sidebar.slider(
    "集中時間（分）",
    1,
    60,
    st.session_state.focus_minutes,
)

break_time = st.sidebar.slider(
    "休憩時間（分）",
    1,
    30,
    st.session_state.break_minutes,
)

# タイマー停止中だけ設定を変更する
if not st.session_state.running:
    if (
        focus_time != st.session_state.focus_minutes
        or break_time != st.session_state.break_minutes
    ):
        st.session_state.focus_minutes = focus_time
        st.session_state.break_minutes = break_time

        if st.session_state.mode == "集中":
            st.session_state.remaining_seconds = focus_time * 60
        else:
            st.session_state.remaining_seconds = break_time * 60

# -------------------------
# タイトル
# -------------------------
st.title("🍅 ポモドーロタイマー")

# 現在時刻
now = datetime.now().strftime("%H:%M:%S")
st.write(f"🕒 現在時刻：**{now}**")

st.subheader(f"現在のモード：{st.session_state.mode}")

# -------------------------
# 残り時間表示
# -------------------------
minutes = st.session_state.remaining_seconds // 60
seconds = st.session_state.remaining_seconds % 60

st.markdown(
    f"""
    <h1 style="text-align:center;font-size:70px;">
    {minutes:02}:{seconds:02}
    </h1>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# ボタン
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("開始"):
        st.session_state.running = True

with col2:
    if st.button("一時停止"):
        st.session_state.running = False

with col3:
    if st.button("リセット"):
        st.session_state.running = False

        if st.session_state.mode == "集中":
            st.session_state.remaining_seconds = (
                st.session_state.focus_minutes * 60
            )
        else:
            st.session_state.remaining_seconds = (
                st.session_state.break_minutes * 60
            )

# -------------------------
# 集中回数
# -------------------------
st.write(f"✅ 完了した集中回数：{st.session_state.completed_count}")

# -------------------------
# タイマー処理
# -------------------------
if st.session_state.running:

    # 1秒待つ
    time.sleep(1)

    # 残り時間を1秒減らす
    st.session_state.remaining_seconds -= 1

    # タイマー終了
    if st.session_state.remaining_seconds <= 0:

        if st.session_state.mode == "集中":

            st.session_state.completed_count += 1
            st.session_state.mode = "休憩"
            st.session_state.remaining_seconds = (
                st.session_state.break_minutes * 60
            )

            st.success("🎉 集中時間が終了しました。休憩しましょう！")

        else:

            st.session_state.mode = "集中"
            st.session_state.remaining_seconds = (
                st.session_state.focus_minutes * 60
            )

            st.success("💪 休憩が終わりました。集中を始めましょう！")

    # 画面を更新
    st.rerun()