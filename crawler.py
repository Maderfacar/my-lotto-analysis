import requests
from bs4 import BeautifulSoup
import json
import re

def get_lotto_data():
    # 這裡使用固定的來源網址
    url = "https://www.taiwanlottery.com.tw/index_info.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        db = {"649": [], "539": []}

        # 1. 大樂透精確抓取 (鎖定 Lotto649Control)
        # 我們抓取包含 'Lotto649Control_history_No1_0' 這種 ID 的 span
        lotto_id = soup.select_one('span[id*="Lotto649Control_history_res_no"]').text.strip()
        lotto_date = soup.select_one('span[id*="Lotto649Control_history_res_date"]').text.strip()
        
        # 抓取 1~6 號 (台彩現在的 ID 命名規則)
        lotto_nums = []
        for i in range(1, 7):
            num = soup.select_one(f'span[id*="Lotto649Control_history_No{i}_0"]').text.strip()
            lotto_nums.append(int(num))
        
        lotto_sp = int(soup.select_one('span[id*="Lotto649Control_history_SNo_0"]').text.strip())
        
        db["649"].append({
            "id": lotto_id,
            "date": lotto_date.replace('/', '-'),
            "nums": sorted(lotto_nums),
            "sp": lotto_sp
        })

        # 2. 今彩539精確抓取 (鎖定 DailyCashControl)
        cash_id = soup.select_one('span[id*="DailyCashControl_history_res_no"]').text.strip()
        cash_date = soup.select_one('span[id*="DailyCashControl_history_res_date"]').text.strip()
        
        cash_nums = []
        for i in range(1, 6):
            num = soup.select_one(f'span[id*="DailyCashControl_history_No{i}_0"]').text.strip()
            cash_nums.append(int(num))
            
        db["539"].append({
            "id": cash_id,
            "date": cash_date.replace('/', '-'),
            "nums": sorted(cash_nums),
            "sp": None
        })

        # 驗證輸出 (您可以在 Actions Log 看到這個)
        print(f"確認抓取 - 大樂透 {lotto_id}: {lotto_nums}, SP: {lotto_sp}")
        print(f"確認抓取 - 539 {cash_id}: {cash_nums}")

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"抓取失敗，錯誤訊息: {e}")

if __name__ == "__main__":
    get_lotto_data()
