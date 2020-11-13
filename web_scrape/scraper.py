import pandas as pd
import sqlalchemy as db
import configparser

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from  import cr

def draftkings_parse(input_dict, driver, key):
    """HTML parser for draftkings odds

    Args:
        input_dict (dict): stores appropriate mappings to odds and outcomes
        driver (chromedriver): selenium Chromedriver that will go and grab our data
        key (string): source name, used as key in dict

    Returns:
        list: list of outcomes zipped, ready to be concatenated into a dataframe
    """
    outcomes = [x.text for x in driver.find_elements_by_class_name(input_dict['outcomes_class'])]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    odds = [x.text for x in soup.findAll('span',{'class', input_dict['odds_class']})]
    # odds = [x.text for x in driver.find_elements_by_class_name(input_dict['odds_class'])]
    return list(zip(outcomes[::3], outcomes[2::3], odds[::3], odds[1::3], odds[2::3], [key] * len(outcomes[::3]), [datetime.now()] * len(outcomes[::3])))

def fanduel_parse(input_dict, driver, key):
    """HTML parser for fanduel odds

    Args:
        input_dict (dict): stores appropriate mappings to odds and outcomes
        driver (chromedriver): selenium Chromedriver that will go and grab our data
        key (string): source name, used as key in dict

    Returns:
        list: list of outcomes zipped, ready to be concatenated into a dataframe
    """
    outcomes = [x.text for x in driver.find_elements_by_class_name(input_dict['outcomes_class'])]
    odds = [x.text for x in driver.find_elements_by_class_name(input_dict['odds_class'])]
    return list(zip(outcomes[::2], outcomes[1::2], odds[::3], odds[1::3], odds[2::3], [key] * len(outcomes[::3]), [datetime.now()] * len(outcomes[::3])))

def bovada_parse(input_dict, driver, key):
    """HTML parser for bovada odds

    Args:
        input_dict (dict): stores appropriate mappings to odds and outcomes
        driver (chromedriver): selenium Chromedriver that will go and grab our data
        key (string): source name, used as key in dict

    Returns:
        list: list of outcomes zipped, ready to be concatenated into a dataframe
    """
    outcomes = [x.text for x in driver.find_elements_by_class_name(input_dict['outcomes_class'])]
    odds = [x.text for x in driver.find_elements_by_class_name(input_dict['odds_class'])]
    return list(zip(outcomes[::2], outcomes[1::2], odds[2::7], odds[4::7], odds[3::7], [key] * len(outcomes[::3]), [datetime.now()] * len(outcomes[::3])))

class Web_Scraper:
    def __init__(self, map_dir, output_cols, scr_options=None):
        self.map_dir = map_dir
        self.output_cols = output_cols
        self.scr_options = scr_options
        self.scr_data = None
        if self.scr_options is None:
            options = Options()
            options.headless = self.scr_options['headless']
            options.add_argument(''.join('--window-size=',self.scr_options['width'],',',self.scr_options['height']))    
    
    def go(self):
        dn = []
        for key in self.map_dir:
            driver = webdriver.Chrome(options=self.scr_options)
            driver.get(self.map_dir[key]['url'])
            driver.implicitly_wait(3)
            
            data = pd.DataFrame(prem_dir[key]['parser'](prem_dir[key]['args'],driver, key),columns=self.output_cols)
            dn.append(data)
            driver.quit()
        return pd.concat(dn, axis=0)

    def update_db(self, conn):
        df = self.go()
        ## need to 
