import pandas as pd
import configparser
import sqlalchemy as db
import requests
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
        df = pd.concat(dn, axis=0)
        df['datetime'] = df['datetime'].astype('str')
    return df.head().to_dict(orient='records')

config = configparser.ConfigParser()
config.read('credentials.txt')
remote = config['remote']
DB_URI = ''.join(['postgres+psycopg2://',remote['user'],':',remote['password'],'@',remote['server'],'/',remote['database']])

conn = db.create_engine(DB_URI).connect()
teams_data = requests.get('https://raw.githubusercontent.com/openfootball/football.json/master/2020-21/en.1.clubs.json')
teams_json = teams_data.json()

teams = pd.DataFrame(teams_json['clubs'])

teams.loc[teams['code'].isna(),'code'] = 'LEE'
teams = teams.drop('country', axis=1)
teams.columns = ['team_name', 'abbreviation']
teams.loc[:,'league_id'] = 1

## print(teams.head())

# cols = ",".join([str(i) for i in teams.columns.tolist()])
# for i,row in teams.iterrows():
#     sql = "INSERT INTO Teams(" +cols + ") VALUES(" + "%s,"*(len(row)-1) + "%s)"
#     conn.execute(sql, tuple(row))

## teams.to_sql('Teams', conn, if_exists='append', index=False)
results = pd.read_sql('SELECT * FROM Teams;', conn)
print(results)

conn.close()