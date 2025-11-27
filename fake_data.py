import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random
import zipfile
import os

# ============================
# 設定
# ============================
N_PARTICIPANTS = 24

COLUMNS = [
    "rt", "stimulus", "response", "trial_type", "trial_index", "plugin_version",
    "time_elapsed", "run_id", "condition", "recorded_at", "id", "ip", "browser",
    "browser_version", "platform", "platform_version", "user_agent", "referer",
    "language", "accept_language", "success", "question_number", "block",
    "question_text", "valence", "slider_start", "question_order"
]

positive_items = [
    "寛大","親切","視野が広い","知的","社交的","果敢","勤勉","正直","人に好かれる","従順",
    "大胆","頼りになる","実務家","誠実","想像力に富む","慎重","控え目","器用","陽気","冷静",
    "ユーモアがある","謙虚","思いやりがある","真面目","粘り強い","厳格"
]

negative_items = [
    "人望がない","無責任","単純","陰気","衝動的","知性がない","不器用","不正直","浅薄","頼りない",
    "うぬぼれ屋","間抜け","悲観的","感傷的","内気","支配的","短気","気難しい","存在感が薄い",
    "優柔不断","冴えない","浪費家","想像力に欠ける","気まぐれ","ユーモアがない","軽薄"
]

loneliness_items = [
    "自分には人との付き合いがないと感じることがありますか？",
    "自分は取り残されていると感じることがありますか？",
    "自分は他の人たちから孤立していると感じることはありますか？"
]

rows = []

for _ in range(N_PARTICIPANTS):
    pid = uuid.uuid4().hex[:16]
    base_time = datetime.now() - timedelta(minutes=random.randint(20, 600))
    trial_index = 0

    order = random.choice(["loneliness_first", "superiority_first"])
    block_order = ["loneliness", "superiority"] if order == "loneliness_first" else ["superiority", "loneliness"]

    for block in block_order:

        # --------------------
        # Loneliness block
        # --------------------
        if block == "loneliness":
            items = random.sample(loneliness_items, len(loneliness_items))
            for i, q in enumerate(items):
                rows.append({
                    "rt": random.randint(500, 4000),
                    "stimulus": f"<p style='font-size:22px;'>{q}</p>",
                    "response": str(random.randint(0, 3)),
                    "trial_type": "survey-likert",
                    "trial_index": trial_index,
                    "plugin_version": "2.1.0",
                    "time_elapsed": random.randint(1000, 50000),
                    "run_id": 1,
                    "condition": 1,
                    "recorded_at": (base_time + timedelta(seconds=trial_index*4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "id": pid, "ip": f"158.217.104.{random.randint(1,254)}",
                    "browser": "Chrome", "browser_version": "143.0.0.0",
                    "platform": "Windows", "platform_version": "10",
                    "user_agent": "Mozilla/5.0",
                    "referer": "https://ckfu3zufqx.cognition.run/",
                    "language": "ja-JP", "accept_language": "ja-JP,ja;q=0.9,en-US;q=0.6",
                    "success": np.nan,
                    "question_number": i+1,
                    "block": "loneliness",
                    "question_text": q,
                    "valence": np.nan,
                    "slider_start": np.nan,
                    "question_order": np.nan,
                })
                trial_index += 1

        # --------------------
        # Superiority block
        # --------------------
        if block == "superiority":
            items = (
                [{"text": x, "valence": "positive"} for x in positive_items] +
                [{"text": x, "valence": "negative"} for x in negative_items]
            )
            random.shuffle(items)

            for i, item in enumerate(items):

                if item["valence"] == "positive":
                    response = int(np.random.normal(70, 15))
                else:
                    response = int(np.random.normal(30, 15))
                response = max(0, min(100, response))

                rows.append({
                    "rt": random.randint(500, 4000),
                    "stimulus": f"<p style='font-size:22px;'>{item['text']}</p>",
                    "response": str(response),
                    "trial_type": "html-slider-response",
                    "trial_index": trial_index,
                    "plugin_version": "2.1.0",
                    "time_elapsed": random.randint(1000, 50000),
                    "run_id": 1,
                    "condition": 1,
                    "recorded_at": (base_time + timedelta(seconds=trial_index*4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "id": pid, "ip": f"158.217.104.{random.randint(1,254)}",
                    "browser": "Chrome", "browser_version": "143.0.0.0",
                    "platform": "Windows", "platform_version": "10",
                    "user_agent": "Mozilla/5.0",
                    "referer": "https://ckfu3zufqx.cognition.run/",
                    "language": "ja-JP", "accept_language": "ja-JP,ja;q=0.9,en-US;q=0.6",
                    "success": np.nan,
                    "question_number": i+1,
                    "block": "superiority",
                    "question_text": item["text"],
                    "valence": item["valence"],
                    "slider_start": 50,
                    "question_order": np.nan,
                })
                trial_index += 1

# ------------------------
# DataFrame & 保存
# ------------------------
df = pd.DataFrame(rows, columns=COLUMNS)

# 個別保存フォルダ
out_dir = "fake_EX_Aoki_individual/"
os.makedirs(out_dir, exist_ok=True)

paths = []
for pid in df["id"].unique():
    part = df[df["id"] == pid]
    path = f"{out_dir}{pid}.csv"
    part.to_csv(path, index=False)
    paths.append(path)

# ------------------------
# ZIP化
# ------------------------
zip_path = "fake_EX_Aoki_24p_individual.zip"
with zipfile.ZipFile(zip_path, "w") as z:
    for p in paths:
        z.write(p, os.path.basename(p))

print("ZIP 作成完了 →", zip_path)
