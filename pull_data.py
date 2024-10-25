# /// script
# dependencies = [
#   "rich",
#   "requests",
#   "beautifulsoup4"
# ]
# ///
import json
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def change_names(name: str):
    team_mapping = {
        "D Zagreb": "Dinamo Zagreb",
        "PSV": "PSV Eindhoven",
        "Man City": "Manchester City",
        "Stuttgart": "VfB Stuttgart",
        "Shakhtar": "Shakhtar Donetsk",
        "Sporting": "Sporting CP",
        "Atlético": "Atlético Madrid",
        "Leverkusen": "Bayer Leverkusen",
        "PSG": "Paris Saint-Germain",
        "Bayern": "Bayern Munich",
        "Dortmund": "Borussia Dortmund",
        "AC Milan": "Milan",
    }
    if name in team_mapping:
        return team_mapping[name]
    return name


def download_html(url: str, file_name: str):
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f"{file_name}", "w") as f:
            f.write(resp.text)

    return None


def read_data_local(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()

    return content


def extract_data(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    results = soup.find_all("td", class_="football-match__teams")
    matches = {}
    for result in results:
        team1 = result.find_all("span", class_="team-name__long")[0].text
        team1 = change_names(team1)
        team2 = result.find_all("span", class_="team-name__long")[1].text
        team2 = change_names(team2)
        score1 = result.find_all("div", class_="football-team__score")[0].text
        score2 = result.find_all("div", class_="football-team__score")[1].text
        
        matches[f"{team1} vs {team2}"] = f"{score1}-{score2}"
      
    return matches



def save_json(data, file_path: str):
    with open(file_path, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":

    data_path = "workdir"

    base_url = "https://www.theguardian.com/football/championsleague/results"
    today = datetime.today().strftime("%Y-%m-%d")

    html_file = f"{data_path}/cl_results_{today}.html"
    download_html(f"{base_url}", html_file)

    matches_results = extract_data(html_content=read_data_local(html_file))
    # print(matches_results)
    with open(f"{data_path}/matches.json", "r") as f:
        matches_template = json.load(f)

    for i, match in enumerate(matches_template):
        w, t1, t2, result = match
        
        if f"{t1} vs {t2}" in matches_results:
            # print(matches_results[f"{t1} vs {t2}"], " - ", result)
            matches_template[i][3] = matches_results[f"{t1} vs {t2}"]
    with open(f"{data_path}/matches.json", "w") as f:
        json.dump(matches_template, f)