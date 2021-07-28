import json
import time
import csv
from glob import glob

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import ElementClickInterceptedException



from tqdm import tqdm


def create_driver():
    driver = webdriver.Chrome('./chromedriver')
    return driver


def get_tickers():
    glob_path = './stock-tickers/*.txt'
    tickers = []
    ticker_paths = glob(glob_path)
    for path in ticker_paths:
        with open(path) as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                # check if it is an ETF
                if row['ETF'] != 'Y':
                    tickers.append(row)
    final_tickers = []
    for ticker in tickers:
        try:
            ticker_symbol = ticker['NASDAQ Symbol']
        except Exception:
            ticker_symbol = ticker['Symbol']
        final_tickers.append(ticker_symbol)
    return final_tickers


def main():
    driver = create_driver()
    tickers = get_tickers()
    for ticker in tickers[:1]:
        driver.get('https://zacks.com/stock/chart/{}/price-eps-surprise'.format(ticker.lower()))

        time.sleep(3)

        eps_surprise_table_link = driver.find_element_by_link_text('EPS Surprise')
        actions = ActionChains(driver)
        actions.move_to_element(eps_surprise_table_link).perform()

        try:
            eps_surprise_table_link.click()
        except ElementClickInterceptedException:
            time.sleep(2)

            eps_surprise_table_link.click()
        
        time.sleep(5)
        pagination = driver.find_element_by_css_selector('#DataTables_Table_3_paginate')
        buttons = pagination.find_elements_by_css_selector('a.paginate_button')[:5]
        
        
        final_surprises = []

        for button in buttons:
            button.click()
            eps_surprise_container = driver.find_element_by_id('chart_wrapper_datatable_eps_surprise')
            table = eps_surprise_container.find_elements_by_css_selector('table')
            surprises = table.find_elements_by_css_selector('tr')
            for surprise in surprises:
                surprise = {}
                surprise['date'] = surprise.find_elemensurpri_by_css_selector('td.sorting_1').text
                surprise['surprise'] = surprise.find_elements_by_css_selector('td')[1].text
            
                final_surprises.append(surprise)
        print(final_surprises)

   

if __name__ == "__main__":
    main()