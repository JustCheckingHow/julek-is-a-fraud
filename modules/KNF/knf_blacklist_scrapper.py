
# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

file_path = os.path.dirname(os.path.abspath('__file__'))
driver_path = os.path.join(
    os.path.dirname(file_path),
    'KNF\chromedriver.exe')

# %%
driver = webdriver.Chrome(driver_path)
driver.get('https://www.knf.gov.pl/dla_konsumenta/ostrzezenia_publiczne?warningName=&warningTypeId=all')

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'table-responsive')))

warnings = driver.find_elements_by_xpath('''//tr[@class='warning-row pure']''')
records = []
for warning in warnings:
    records += [warning.find_elements_by_tag_name('td')[1]
                       .text.lstrip('0123456789.- ')
                       .split(' z siedzibą')[0]
                       .split(' (')[0]]

# %%

fields = ['Names']

rows = []
for record in records:
    record = record.replace('\n', '')
    rows += [[record]]

with open('blacklist.csv', 'w', encoding='utf-8-sig') as f:
    write = csv.writer(f, lineterminator='\n') 
      
    write.writerow(fields)
    write.writerows(rows)
