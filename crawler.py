import requests
from bs4 import BeautifulSoup
import json
import os
import re

def get_lotto_data():
    url = "https://www.taiwanlottery.com.tw/index_info.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # 讀取現有的數據 (確保在 GitHub Action 環境路徑正確)
    db = {"649": [], "539": []}
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                db = json.load(f)
        except: pass

    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # 大樂透邏輯
        box649 = soup.find("div", class_="contents_box02")
        if box649:
            l_id = box649.find("span", class_="td_w font_black14b").text.strip()
            # 只有當期號不在資料庫時才加入
            if not any(d['id'] == l_id for d in db["649"]):
                balls = box649.find_all("div", class_="ball_tx")
                item = {
                    "id": l_id,
                    "date": box649.find("span", class_="font_black14b").find_next("span").text.strip(),
                    "nums": sorted([int(balls[i].text) for i in range(6, 12)]),
                    "sp": int(balls[12].text)
                }
                db["649"].insert(0, item) # 新的排前面

        # 539 邏輯
        box539 = soup.find("div", class_="contents_box03")
        if box539:
            s_id = box539.find("span", class_="td_w font_black14b").text.strip()
            if not any(d['id'] == s_id for d in db["539"]):
                balls = box539.find_all("div", class_="ball_tx")
                item = {
                    "id": s_id,
                    "date": box539.find("span", class_="font_black14b").find_next("span").text.strip(),
                    "nums": sorted([int(balls[i].text) for i in range(5, 10)])
                }
                db["539"].insert(0, item)

        # 限制資料庫大小，只存最近 50 期，避免檔案過大
        db["649"] = db["649"][:50]
        db["539"] = db["539"][:50]

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_lotto_data()
