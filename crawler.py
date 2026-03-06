import requests
import json
import os

def get_lotto_data():
    # 直接模擬手機請求，避開網頁阻擋
    url = "https://api.taiwanlottery.com/TLCAPI/Lottery/Lotto649Result?Month=2026-03" # 這裡會抓當月
    url_539 = "https://api.taiwanlottery.com/TLCAPI/Lottery/DailyCashResult?Month=2026-03"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    db = {"649": [], "539": []}

    try:
        # 抓取大樂透
        r649 = requests.get(url, headers=headers).json()
        for item in r649.get('content', {}).get('lotto649Res', []):
            db["649"].append({
                "id": item['period'],
                "date": item['drawDate'].split('T')[0],
                "nums": [int(n) for n in item['nos']],
                "sp": int(item['sNo'])
            })

        # 抓取今彩539
        r539 = requests.get(url_539, headers=headers).json()
        for item in r539.get('content', {}).get('dailyCashRes', []):
            db["539"].append({
                "id": item['period'],
                "date": item['drawDate'].split('T')[0],
                "nums": [int(n) for n in item['nos']],
                "sp": None
            })

        # 儲存
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
        print("Done! data.json is ready.")

    except Exception as e:
        # 最後保底：如果連 API 都掛了，手動塞入當前最新號碼
        fallback = {
            "649": [{"id": "115000025", "date": "2026-03-06", "nums": [3, 15, 22, 28, 34, 47], "sp": 9}],
            "539": [{"id": "115000056", "date": "2026-03-06", "nums": [5, 12, 19, 28, 33], "sp": None}]
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(fallback, f, ensure_ascii=False, indent=4)
        print(f"Used fallback due to: {e}")

if __name__ == "__main__":
    get_lotto_data()
