import requests
from bs4 import BeautifulSoup

def get_module_description(module_code):
    url = f"https://www.ucl.ac.uk/module-catalogue/modules/{module_code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        description_div = soup.find("div", class_="module-description")
        if description_div:
            return description_div.get_text(strip=True)
        else:
            return "Module description not found"
    else:
        return f"Failed to fetch module page, status code: {response.status_code}"

if __name__ == "__main__":
    module_code = "COMP0015"  # 這裡可以改成你要查找的 module code
    description = get_module_description(module_code)
    print(f"Module {module_code} Description:\n{description}")
