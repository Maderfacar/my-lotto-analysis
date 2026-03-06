import requests
from bs4 import BeautifulSoup
import json
import os
import re

# 定義抓取目標與解析邏輯
def get_lotto_data():
    url = "https://www.taiwanlottery.com.tw/index_info.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 讀取現有資料庫，若無則建立空的
        db_path = 'data.json'
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
        else:
            db = {"649": [], "539": []}

        # --- 解析大樂透 (649) ---
        # 尋找大樂透區塊內容
        lotto_649_box = soup.find("div", {"class": "contents_box02"})
        if lotto_649_box:
            res_id = lotto_649_box.find("span", {"id": "Lotto649Control_history_dl_Lotto649_No_0"}).text
            res_date = lotto_649_box.find("span", {"id": "Lotto649Control_history_dl_Lotto649_Date_0"}).text
            # 抓取 6 個一般號
            nums = []
            for i in range(1, 7):
                n = lotto_649_box.find("span", {"id": f"Lotto649Control_history_dl_Lotto649_No{i}_0"}).text
                nums.append(int(n))
            # 特別號
            sp = int(lotto_649_box.find("span", {"id": "Lotto649Control_history_dl_Lotto649_SNo_0"}).text)
            
            new_entry = {"id": res_id, "date": res_date.replace("/", "-"), "nums": sorted(nums), "sp": sp}
            if new_entry["id"] not in [x["id"] for x in db["649"]]:
                db["649"].insert(0, new_entry)
                print(f"大樂透更新成功: {res_id}")

        # --- 解析今彩 539 ---
        lotto_539_box = soup.find("div", {"class": "contents_box03"})
        if lotto_539_box:
            res_id = lotto_539_box.find("span", {"id": "DailyCashControl_history_dl_DailyCash_No_0"}).text
            res_date = lotto_539_box.find("span", {"id": "DailyCashControl_history_dl_DailyCash_Date_0"}).text
            nums = []
            for i in range(1, 6):
                n = lotto_539_box.find("span", {"id": f"DailyCashControl_history_dl_DailyCash_No{i}_0"}).text
                nums.append(int(n))
            
            new_entry = {"id": res_id, "date": res_date.replace("/", "-"), "nums": sorted(nums), "sp": None}
            if new_entry["id"] not in [x["id"] for x in db["539"]]:
                db["539"].insert(0, new_entry)
                print(f"今彩 539 更新成功: {res_id}")

        # 寫回檔案 (限制保存最近 500 期，避免檔案過大影響網頁速度)
        db["649"] = db["649"][:500]
        db["539"] = db["539"][:500]
        
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"爬取發生錯誤: {e}")

if __name__ == "__main__":
    get_lotto_data()
