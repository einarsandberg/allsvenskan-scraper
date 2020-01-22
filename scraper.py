from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json
import csv
import os
def scrape():
    # Url fetched by https://www.svenskfotboll.se/serier-cuper/spelprogram/allsvenskan-herrar/77486/ when clicking "Omgång"
    # Contains json of format {data: html_content}
    rounds_url = 'https://www.svenskfotboll.se/api/sort-games/?contentID=5701&ftid=77486&sortBy=round'
    req = Request(rounds_url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req).read()

    doc = resp.decode("utf8")
    json_data = json.loads(doc)
    html_doc = json_data['data']
    
    # Get 2019 data
    soup = BeautifulSoup(html_doc, 'html.parser')
    teams_el_list = soup.find_all(class_='match-list__team-name')
    goals_el_list = soup.find_all(class_='match-list__score')

    matches = create_matches(teams_el_list, goals_el_list)
    write_json(matches)

def create_matches(teams_el_list: list, goals_el_list: list):
    matches = []
    for i in range(1, len(teams_el_list), 2):
        matches.append(
            create_match(
                home_team=teams_el_list[i-1].getText(), 
                away_team=teams_el_list[i].getText(),
                home_goals=goals_el_list[i-1].getText(),
                away_goals=goals_el_list[i].getText(),
            )
        )
    
    return matches

def create_match(home_team: str, away_team: str, home_goals: str, away_goals: str):
    return {
        'home_team': home_team,
        'away_team': away_team,
        'home_goals': home_goals,
        'away_goals': away_goals,
    }

def write_json(matches: list):
    path = '{}/res/matches.json'.format(os.path.dirname(os.path.realpath(__file__)))
    with open(path, 'w') as file:
        json.dump(matches, file, ensure_ascii=False, indent=4)

scrape()
