import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def highlight_position(row):
    if row["ポジション"] == "GK":
        return ["background-color: #E3F2FD"] * len(row)  # 青
    elif row["ポジション"] == "DF":
        return ["background-color: #E8F5E9"] * len(row)  # 緑
    elif row["ポジション"] == "MF":
        return ["background-color: #FFFDE7"] * len(row)  # 黄
    elif row["ポジション"] == "FW":
        return ["background-color: #FCE4EC"] * len(row)  # 赤
    return [""] * len(row)

st.set_page_config(page_title="Jリーグ選手一覧", layout="wide")

st.title("⚽ Jリーグ選手一覧")
st.caption("スプレッドシート連携｜チーム別選手データを一覧表示")

st.divider()
st.subheader("チームを選択すると選手一覧が表示されます")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    team_name = st.text_input("チーム名（例：京都サンガ）")

# ===== Googleスプレッドシート設定（★ここは1回書くだけ）=====
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "soccer-app-481912-b7f66352b50e.json",  # ← JSONファイル名
    scopes=SCOPES
)
client = gspread.authorize(creds)
spreadsheet = client.open("選手表もと")  # ← あなたのシート名
worksheet = spreadsheet.sheet1
# =============================================================

if team_name:
    st.success(f"「{team_name}」の選手データを表示します")

    # スプレッドシートから全データ取得
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # チーム名で絞り込み
    team_df = df[df["チーム名"] == team_name]

    st.subheader("選手一覧")

    if team_df.empty:
        st.warning("該当するチームのデータがありません")
    else:
        st.dataframe(
            df.style.apply(highlight_position, axis=1),
            use_container_width=True,
        )
