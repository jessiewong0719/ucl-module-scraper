import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 讀取 CSV 文件
file_path = "UCL EAST MODULES ENG(Sheet1).csv"  # 這是 GitHub 上的文件名稱
df = pd.read_csv(file_path)

# 設置 UCL Module Catalogue 的基本 URL
base_url = "https://www.ucl.ac.uk/module-catalogue/modules/"
module_codes = df["Module Code"].dropna().unique()

# 儲存爬取的結果
module_descriptions = []

# 設置 headers（模擬瀏覽器）
headers = {"User-Agent": "Mozilla/5.0"}

# 爬取每個 Module Code 的描述
for module_code in module_codes:
    url = f"{base_url}{module_code}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            description_div = soup.find("div", class_="field--name-field-module-description")
            description = description_div.get_text(strip=True) if description_div else "Description not found"
        else:
            description = f"Error {response.status_code}"
    except Exception as e:
        description = f"Request failed: {str(e)}"

    # 存入列表
    module_descriptions.append({"Module Code": module_code, "Description": description})

    # 避免請求過快
    time.sleep(2)

# 轉換為 DataFrame 並保存
desc_df = pd.DataFrame(module_descriptions)
desc_df.to_csv("ucl_module_descriptions.csv", index=False)

print("爬取完成，結果已保存為 ucl_module_descriptions.csv")
