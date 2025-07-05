import requests
from bs4 import BeautifulSoup
import json

url = "https://voxiitk.com/our-team/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

all_tenures = []

for tab_title_div in soup.find_all("div", id=lambda x: x and x.startswith("elementor-tab-title-")): #  Find all tab titles by ID pattern
    tab_id = tab_title_div["id"]
    tab_number = tab_id.split("-")[-1]
    tenure_label = tab_title_div.get_text(strip=True)
    content_id = f"elementor-tab-content-{tab_number}"# Corresponding content panel has id elementor-tab-content-<number>
    tab_content_div = soup.find("div", id=content_id)
    if not tab_content_div:
        continue

    team = {}
    role = None
    for el in tab_content_div.find_all(["strong", "b", "p", "span"], recursive=True):
        text = el.get_text(strip=True)
        # Detect role headings
        if "chief editor" in text.lower():
            role = "Chief Editors"
            team[role] = []
        elif "editor" in text.lower() and "chief" not in text.lower():
            role = "Editors"
            team[role] = []
        elif "web executive" in text.lower():
            role = "Web Executives"
            team[role] = []
        elif "designer" in text.lower():
            role = "Designers"
            team[role] = []
        elif role and text:
            names = [n.strip() for n in text.split(",") if n.strip()]
            team[role].extend(names)
    for role in team: # Convert lists to newline-separated strings
        team[role] = "\n".join(team[role])

    all_tenures.append({
        "tenure": tenure_label,
        "team": team
    })

with open("voxiitk_team_by_id.json", "w", encoding="utf-8") as f:
    json.dump(all_tenures, f, indent=2, ensure_ascii=False)

print("Scraping complete. Data saved to voxiitk_team_by_id.json")