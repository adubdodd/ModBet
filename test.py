import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def draftkings_parse(input_dict, driver, key):
    outcomes = [x.text for x in driver.find_elements_by_class_name(input_dict['outcomes_class'])]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    odds = [x.text for x in soup.findAll('span',{'class', input_dict['odds_class']})]
    # odds = [x.text for x in driver.find_elements_by_class_name(input_dict['odds_class'])]
    return list(zip(outcomes[::3], outcomes[2::3], odds[::3], odds[1::3], odds[2::3], [key] * len(outcomes[::3]), [datetime.now()] * len(outcomes[::3])))

prem_dir = {'draftkings':{'url':'https://sportsbook.draftkings.com/leagues/soccer/53591936',
                          'parser': draftkings_parse,
                          'args':{'outcomes_class':'sportsbook-outcome-cell__label',
                                  'odds_class':'sportsbook-odds american default-color'}}
           }
           
output_cols = ['home_team','away_team', 'home_odds','tie_odds', 'away_odds', 'source', 'datetime']

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs
chrome_prefs['profile.default_content_settings'] = {"images":2}

def get_odd_json():
    dn = []
    for key in prem_dir:
        driver = webdriver.Chrome(options=options)
        driver.get(prem_dir[key]['url'])
        driver.implicitly_wait(3)

        data = pd.DataFrame(prem_dir[key]['parser'](prem_dir[key]['args'],driver, key),columns=output_cols)
        dn.append(data)
        driver.quit()
    return pd.concat(dn, axis=0)[['home_team']].head().to_dict(orient='records')

