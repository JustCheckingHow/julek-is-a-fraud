
# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import json
import csv

CONFIG = json.load(open('config.json'))
file_path = os.path.dirname(os.path.abspath('__file__'))
driver_path = os.path.join(
    os.path.dirname(file_path),
    'KNF\chromedriver.exe')

# %%
driver = webdriver.Chrome(driver_path)
driver.get('https://app.neilpatel.com/en/seo_analyzer/backlinks')

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '''//*[text() = 'Sign in']''')))
driver.execute_script('''arguments[0].click();''', element)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'email')))
driver.find_element_by_name('email').send_keys(CONFIG['LOGIN'])
driver.find_element_by_name('password').send_keys(CONFIG['PASSWORD'])

driver.find_element_by_xpath('''//button[@type='submit']''').click()

# Complete the captcha before proceeding xd

# %%

driver.get('https://app.neilpatel.com/en/seo_analyzer/backlinks')

websites = ['http://yuandaqihuogongsi.b58b.com']

time_fmt = r'%m/%d/%Y'
records = []
for website in websites:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '''//input[@placeholder='Enter Domain or URL']'''))).clear()
    driver.find_element_by_xpath('''//input[@placeholder='Enter Domain or URL']''').send_keys(website)
    driver.find_element_by_xpath('''//button[text() ='Search']''').click()

    # element = driver.find_element_by_xpath('''//button[text() = 'EXPORT TO CSV']''')
    # driver.execute_script('''arguments[0].click();''', element)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'content')))
    backlinks = driver.find_element_by_id('content').find_elements_by_xpath('''./div''')

    for row in backlinks:
        columns = row.find_elements_by_xpath('''./div''')

        link = columns[0].find_element_by_tag_name('a').get_attribute('href')

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

print(records)
# %% 

fields = [
    'website',
    'link',
    'domain_score',
    'page_score',
    'link_type',
    'anchor_text',
    'first_seen',
    'last_seen'
]

with open('backlinks.csv', 'w', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
      
    for record in records:
        writer.writerow(record)
