import requests
from bs4 import BeautifulSoup
import json
import re

def get_lotto_data():
    url = "https://www.taiwanlottery.com.tw/index_info.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        db = {"649": [], "539": []}

        # --- 精確定位大樂透區塊 ---
        # 尋找標題為 "大樂透" 的 div，並往上找到它的容器
        title_649 = soup.find("div", string=re.compile("大樂透"))
        if title_649:
            box = title_649.find_parent("div", class_="contents_box02")
            lotto_id = box.find("span", class_="td_w font_black14b").text.strip()
            lotto_date = box.find("span", class_="font_black14b").find_next("span", class_="font_black14b").text.strip()
            
            # 抓取開出順序 (球號通常在球的容器裡)
            balls = box.find_all("div", class_="ball_tx")
            # 台彩結構：1~6是開出順序，7~12是大小順序，13是特別號
            # 我們抓「大小順序」 7~12 (index 6 to 11)
            nums = [int(balls[i].text) for i in range(6, 12)]
            sp = int(balls[12].text)
            
            db["649"].append({"id": lotto_id, "date": lotto_date, "nums": sorted(nums), "sp": sp})

        # --- 精確定位今彩539區塊 ---
        title_539 = soup.find("div", string=re.compile("今彩539"))
        if title_539:
            box = title_539.find_parent("div", class_="contents_box03")
            id539 = box.find("span", class_="td_w font_black14b").text.strip()
            date539 = box.find("span", class_="font_black14b").find_next("span", class_="font_black14b").text.strip()
            
            balls = box.find_all("div", class_="ball_tx")
            # 539 結構：1~5是開出順序，6~10是大小順序
            nums539 = [int(balls[i].text) for i in range(5, 10)]
            
            db["539"].append({"id": id539, "date": date539, "nums": sorted(nums539), "sp": None})

        # 輸出結果至 data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
        print("數據抓取完成！")

    except Exception as e:
        print(f"抓取失敗: {e}")

if __name__ == "__main__":
    get_lotto_data()
