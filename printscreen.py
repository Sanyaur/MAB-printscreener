# nyissa meg a mabot
# login fieldbe írja be a tszámot + jelszót
# navigáljon el a https://www2.avon.hu/hu-home/product-catalog/ URLre (és annak aloldalaira)
    # gyűjtse ki a rep-support category URL-jeit
    # loopoljon át az összes oldalon
    # csináljon printscreent mindegyik oldalról (ha már betöltött az oldal)
    # mentse el a megadott helyre megadott néven a printscreeneket
# lépjen ki a böngészőből

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

from time import sleep
from datetime import datetime

PATH = 'c:/Program Files (x86)/geckodriver.exe'
driver = webdriver.Firefox(executable_path=PATH)

scrnshot_img_path = 'c:/Users/ujvaris/OneDrive - Avon/Desktop/_to_be_deleted/MAB sprint screenshots/' #img will be saved here

def set_window_size():
    # get window size
    size = driver.get_window_size()
    width1 = size.get('width')
    height1 = driver.execute_script('return document.documentElement.scrollHeight')

    print("scrollheight is", height1)

    driver.set_window_size(width1, height1)

def login_field():
    # wait for elements to load
    username = driver.find_element_by_id('sellerUserId')
    password = driver.find_element_by_id('sellerEmailPassword')

    username.send_keys('6290011')
    password.send_keys('ezEgyJelszó!01' + Keys.ENTER)

driver.get('https://www2.avon.hu/hu-home/product-catalog.html') # opens MAB

try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sellerEmailPassword")))
    print('login page ✅')
    login_field()
except:
    print('login page ❌')

# WAIT TILL X ELEMENT LOADS
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "sub-div")))
    print('product-catalog ✅')
except:
    print('product-catalog ❌')

def create_printscreen(css_selector):
    ele = driver.find_element(By.CSS_SELECTOR, css_selector)
    if css_selector == '.plpPage-c':
        ele.screenshot(f'{scrnshot_img_path}TANÁCSADÓKNAK - {driver.title}.png')
    if css_selector == '.pao-salestool':
        ele.screenshot(f'{scrnshot_img_path}SALES TOOLS - {driver.title}.png')

    # driver.save_screenshot(scrnshot_img_path + driver.title + ' .png') # takes screenshot
    print(f'Printscreen created from: {driver.title}')

elements = driver.find_elements(By.CSS_SELECTOR, 'div.nav-itm:nth-child(2) masonry-brick div') # get URLs from 'Tanácsadóknak' menu
url_list = []
for e in elements:
    mab_url = e.get_attribute("url")
    url_list.append(mab_url)

# Loops through the 'Tanácsadóknak' menu URLs
for i in url_list:
    driver.get(f'https://www2.avon.hu{i}')
    try:
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        create_printscreen('.plpPage-c')
    except:
        print(f'error when loading URL: https://www2.avon.hu{i}')

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print(f'Script ended at{current_time}')

quit()

def order_process():
    try:
        # sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.get('https://www2.avon.hu/hu-home/orders/product-entry')
    except:
        print('LN input page load failed')
        exit()
        
    ln_input_field = driver.find_element_by_css_selector('.shpByProdNum > tab-entry-core:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
    termek_mentese_button = driver.find_element_by_css_selector('.shpByProdNum > tab-entry-core:nth-child(2) > div:nth-child(1) > div:nth-child(3) > button:nth-child(2)')
    tovabb_button = driver.find_element_by_id('btnCont')

    sleep(3)
    ln_input_field.send_keys('00018')
    sleep(2)
    termek_mentese_button.click()
    sleep(4)
    product_popup_X = driver.find_element_by_css_selector('.nav_wrap > span:nth-child(1)')
    product_popup_X.click()
    sleep(4)
    tovabb_button.click()
    print('ennyike')
order_process()

# printscreen from sales tools
# next page
# printscreen from next page
