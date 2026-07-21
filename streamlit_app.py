# ============================
# 学習履歴
# ============================
import pandas as pd
from datetime import datetime

# 初回のみ履歴を作成
if "history" not in st.session_state:
    st.session_state.history = []

st.divider()
st.header("📚 学習履歴")

# 学習時間を入力
study_minutes = st.number_input(
    "学習時間（分）",
    min_value=1,
    max_value=600,
    value=30,
)

# 保存ボタン
if st.button("学習時間を保存"):

    st.session_state.history.append(
        {
            "日時": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "学習時間": study_minutes,
        }
    )

    st.success("学習履歴を保存しました。")

# 履歴を表示
if st.session_state.history:

    df = pd.DataFrame(st.session_state.history)

    st.subheader("履歴一覧")
    st.dataframe(df, use_container_width=True)

    st.subheader("学習時間の推移")
    st.line_chart(
        df.set_index("日時")["学習時間"]
    )

    total = df["学習時間"].sum()

    st.metric(
        "合計学習時間",
        f"{total} 分"
    )

else:
    st.info("まだ学習履歴はありません。")