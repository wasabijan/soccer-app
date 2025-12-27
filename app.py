import gspread
from google.oauth2.service_account import Credentials

# ==============================
# 認証設定
# ==============================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "soccer-app-481912-b7f66352b50e.json"

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(creds)

# ==============================
# スプレッドシートを開く
# ==============================
spreadsheet = client.open("選手表もと")  # スプレッドシート名に置き換える
sheet = spreadsheet.sheet1  # 1つ目のシートを使用

# ==============================
# データを取得
# ==============================
data = sheet.get_all_values()  # 2次元リスト
header = data[0]  # ヘッダー行
rows = data[1:]   # データ部分

# ==============================
# チーム名で選手を表示
# ==============================
team_input = input("チーム名を入力してください（例：ガンバ大阪）: ")

found = False
print(f"\n{team_input} 選手一覧")
print("-" * 70)
print("No. | 名前 | ポジション | 生年月日 | 身長・体重 | 出場試合数 | 得点")
print("-" * 70)

for row in rows:
    team_name, number, name, position, birth, height_weight, appearances, goals = row
    if team_name == team_input:
        found = True
        print(f"{number} | {name} | {position} | {birth} | {height_weight} | {appearances} | {goals}")

if not found:
    print("該当するチームが見つかりませんでした。")
