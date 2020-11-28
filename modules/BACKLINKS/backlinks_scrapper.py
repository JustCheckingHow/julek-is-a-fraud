from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from modules import WebpageResolver
from datetime import datetime
import os
import json
import time
import csv
import pandas as pd


class BacklinksScrapper():
    def __init__(self, config, driver_path) -> None:
        self.config = config
        self.driver = webdriver.Chrome(driver_path)
        self.driver.get('https://app.neilpatel.com/en/seo_analyzer/backlinks')

    def login(self):
        '''
        A hacky way to split main logic from logging in, due to the
        CAPTCHA problem. User needs to complete the captcha at the
        end of this function.
        '''        
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '''//*[text() = 'Sign in']''')))
        self.driver.execute_script('''arguments[0].click();''', element)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email')))
        self.driver.find_element_by_name('email') \
                   .send_keys(self.config['LOGIN'])
        self.driver.find_element_by_name('password') \
                   .send_keys(self.config['PASSWORD'])

        element = self.driver.find_element_by_xpath(
            '''//button[@type='submit']''').click()

    def scrape(self, websites) -> list:   
        '''
        Scrapes the neilpatel website for backlinks and some additional info,
        returns dict of data.

        :param websites: websites to check
        :type websites: list of strings

        :return: list of dicts containing backlink data
        :rtype: list of dict
        '''

        self.driver.get('https://app.neilpatel.com/en/seo_analyzer/backlinks')

        time_fmt = r'%m/%d/%Y'
        records = []
        for website in websites:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '''//input[@placeholder='Enter Domain or URL']'''))) \
                  .clear()
            self.driver.find_element_by_xpath(
                '''//input[@placeholder='Enter Domain or URL']''') \
                  .send_keys(website)

            element = self.driver.find_element_by_xpath(
                '''//button[text() = 'Search']''')
            self.driver.execute_script('''arguments[0].click();''', element)

            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '''//b[text() = 'Ouch!']''')))
                continue
            except Exception:
                pass
                
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'content')))
            except Exception:
                continue

            backlinks = self.driver.find_element_by_id('content') \
                              .find_elements_by_xpath('''./div''')

            for row in backlinks:
                columns = row.find_elements_by_xpath('''./div''')

                link = columns[0].find_element_by_tag_name('a') \
                                 .get_attribute('href')

                records += [{
                    'website': website,
                    'link': link,
                    'domain_score': columns[1].text,
                    'page_score': columns[2].text,
                    'link_type': columns[3].text,
                    'anchor_text': columns[4].text,
                    'first_seen': datetime.strptime(columns[5].text, time_fmt),
                    'last_seen': datetime.strptime(columns[6].text, time_fmt),
                }]

        return records

    @staticmethod
    def to_pandas(results) -> pd.DataFrame:
        return pd.DataFrame(results)


if __name__ == '__main__':
    CONFIG = json.load(open('config.json', 'r'))
    file_path = os.path.dirname(os.path.abspath('__file__'))
    driver_path = os.path.join(
        os.path.dirname(file_path),
        'BACKLINKS\chromedriver.exe')

    scraper = BacklinksScrapper(CONFIG, driver_path)

    scraper.login()
    input('')
    websites = ['http://yuandaqihuogongsi.b58b.com',
                'http://hrgj168.com',
                'http://pecuniaco.com',
                'https://24primeoption.com',
                'https://alpinumcg.com',
                'https://atlasfx.co',
                'https://binarytrades24.com',
                'https://caelusasset.com',
                'https://cescaptial.com',
                'https://cryptocashfx.com',
                'https://edit.fca.org.uk',
                'https://es.eurswiss.com',
                'https://fxg.mark',
                'https://globalfxs.org',
                'https://haitongcaifu1.com',
                'https://haitongcaifu8.com',
                'https://intrgroups.com',
                'https://lautorite.qc.ca',
                'https://leveltrades.com',
                'https://market.wikifx.hk',
                'https://mastertradingfx.com',
                'https://moontradefx.com',
                'https://nimbusplatform.io',
                'https://ns0t2sr3a.zy',
                'https://platinumproinvestment.com',
                'https://quantfury.com',
                'https://royaltyfinance.io',
                'https://stocklux.co',
                'https://swiftcryptofx.com',
                'https://web.coopermarkets.com',
                'https://worldmarkets.com',
                'https://www.afm.nl',
                'https://www.amf',
                'https://www.bcsc.bc.ca',
                'https://www.centralbank.ie',
                'https://www.cmvm.pt',
                'https://www.cnb.cz',
                'https://www.cnmv.es',
                'https://www.cssf.lu',
                'https://www.fca.org.uk',
                'https://www.finma.ch',
                'https://www.fi.se',
                'https://www.fma.govt.nz',
                'https://www.fma.gv.at',
                'https://www.fsc.bg',
                'https://www.fsma.be',
                'https://www.knf.gov.pl',
                'https://www.osc.gov.on.ca',
                'https://www.sfc.hk',
                'https://www.sfx247.com',
                'https://www.vuel',
                'http://www.consob.it',
                'http://yuandaqihuogongsi.b58b.com']

    records = scraper.scrape(websites)
    df = BacklinksScrapper.to_pandas(records).to_csv(
        'backlinks.tsv',
        sep='\t',
        quotechar='\'',
        quoting=csv.QUOTE_NONE)
