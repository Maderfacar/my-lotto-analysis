import requests
from bs4 import BeautifulSoup
import json
import os
import re

def get_lotto_data():
    url = "https://www.taiwanlottery.com.tw/index_info.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # 1. 讀取現有數據 (如果檔案存在)
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            try:
                db = json.load(f)
            except:
                db = {"649": [], "539": []}
    else:
        db = {"649": [], "539": []}

    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # --- 處理大樂透 ---
        box649 = soup.find("div", class_="contents_box02")
        if box649:
            l_id = box649.find("span", class_="td_w font_black14b").text.strip()
            # 檢查是否已存在該期號，避免重複累加
            if not any(item['id'] == l_id for item in db["649"]):
                l_date = box649.find("span", class_="font_black14b").find_next("span", class_="font_black14b").text.strip()
                balls = box649.find_all("div", class_="ball_tx")
                nums = sorted([int(balls[i].text) for i in range(6, 12)])
                sp = int(balls[12].text)
                # 插入到列表最前面 (最新的在上面)
                db["649"].insert(0, {"id": l_id, "date": l_date, "nums": nums, "sp": sp})

        # --- 處理今彩539 ---
        box539 = soup.find("div", class_="contents_box03")
        if box539:
            s_id = box539.find("span", class_="td_w font_black14b").text.strip()
            if not any(item['id'] == s_id for item in db["539"]):
                s_date = box539.find("span", class_="font_black14b").find_next("span", class_="font_black14b").text.strip()
                balls_539 = box539.find_all("div", class_="ball_tx")
                nums539 = sorted([int(balls_539[i].text) for i in range(5, 10)])
                db["539"].insert(0, {"id": s_id, "date": s_date, "nums": nums539, "sp": None})

        # 2. 儲存完整歷史數據
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
        print(f"數據累加成功！目前大樂透共有 {len(db['649'])} 期紀錄。")

    except Exception as e:
        print(f"執行出錯: {e}")

if __name__ == "__main__":
    get_lotto_data()
