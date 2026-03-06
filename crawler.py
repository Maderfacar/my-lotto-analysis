import requests
from bs4 import BeautifulSoup
import json
import os
import re

def get_lotto_data():
    url = "https://www.taiwanlottery.com.tw/index_info.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        db = {"649": [], "539": []}

        # --- 大樂透解析 ---
        box649 = soup.find("div", {"class": "contents_box02"})
        if box649:
            nums = [int(box649.find("span", {"id": re.compile(f".*No{i}_0")}).text) for i in range(1, 7)]
            sp = int(box649.find("span", {"id": re.compile(".*SNo_0")}).text)
            draw_id = box649.find("span", {"id": re.compile(".*No_0")}).text
            date = box649.find("span", {"id": re.compile(".*Date_0")}).text
            db["649"].append({"id": draw_id, "date": date.replace("/", "-"), "nums": nums, "sp": sp})

        # --- 539 解析 ---
        box539 = soup.find("div", {"class": "contents_box03"})
        if box539:
            nums = [int(box539.find("span", {"id": re.compile(f".*No{i}_0")}).text) for i in range(1, 6)]
            draw_id = box539.find("span", {"id": re.compile(".*No_0")}).text
            date = box539.find("span", {"id": re.compile(".*Date_0")}).text
            db["539"].append({"id": draw_id, "date": date.replace("/", "-"), "nums": nums, "sp": None})

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
        print("數據抓取成功！")

    except Exception as e:
        print(f"解析出錯: {e}")

if __name__ == "__main__":
    get_lotto_data()
