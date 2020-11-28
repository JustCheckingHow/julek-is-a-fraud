
# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
import os

file_path = os.path.dirname(os.path.abspath('__file__'))
driver_path = os.path.join(
    os.path.dirname(file_path),
    'julek-is-a-fraud\chromedriver.exe')

# %%
driver = webdriver.Chrome(driver_path)
driver.get('https://www.knf.gov.pl/podmioty/wyszukiwarka_podmiotow#')

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'searchButton'))).click()

# %%
records = []
while True:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ddButton')))

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '''//*[@class='knf-icon knf-arrowDown small']''')))

    records += [rec.text for rec in driver.find_elements_by_class_name('singleEntity')]
    # results = driver.find_elements_by_xpath('''//*[@class='searchresult-entity-item panel panel-default']''')
    # for result in results:
        # list_elements = result.find_element_by_class_name('tableize')
        # dt = list_elements.find_elements_by_tag_name('dt')
        # dd = list_elements.find_elements_by_tag_name('dd')
        
        # records += [{
        #     name.text: value.text
        #     for name, value in zip(dt, dd)
        # }]

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'nextPage')))
        driver.execute_script('''arguments[0].click();''', element)
    except Exception as e:
        print('breaking...')
        break

# %%

# for record in records[:10]:
#     print(record)
import csv
fields = ['Names']

rows = []
for record in records:
    record = record.replace('\n', '')
    rows += [[record]]

with open('whitelist.csv', 'w', encoding='utf-8-sig') as f:
    write = csv.writer(f, lineterminator='\n') 
      
    write.writerow(fields)
    write.writerows(rows)
