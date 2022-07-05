# selenium packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

# time releated packages
import time
from time import sleep
from datetime import datetime, date

# making folder for screenshot
from pathlib import Path

# login credentials
import credentials

from selenium.webdriver.firefox.options import Options

options = Options()
# setup "True" for headless, "False" for normal mode
options.headless = True

PATH = "c:/Program Files (x86)/geckodriver.exe"
driver = webdriver.Firefox(options=options, executable_path=PATH)


def set_window_size():
    # get window size
    size = driver.get_window_size()
    width1 = size.get("width")
    height1 = driver.execute_script("return document.documentElement.scrollHeight")

    driver.set_window_size(width1, height1)


def login_field():
    username = driver.find_element(By.ID, "sellerUserId")
    password = driver.find_element(By.ID, "sellerEmailPassword")

    username.send_keys(credentials.username)
    password.send_keys(credentials.password + Keys.ENTER)


# logging time starts here
start = time.time()

print("Script started...")
driver.get("https://www2.avon.hu/hu-home/product-catalog.html")  # opens MAB

# ---------------- MUST HAVE PART ----------------
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sellerEmailPassword"))
    )
    login_field()
    print("login page OK")
except:
    print("login page NOT OK")
    driver.quit()

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sub-div"))
    )
    print("product-catalog OK")
except:
    print("product-catalog NOT OK")
    driver.quit()

# creates new folder for the upcoming printscreens with today's date
today_date = date.today()
scrnshot_img_path = f"c:/Users/ujvaris/OneDrive - Avon/Desktop/MAB/MAB sprint screenshots/{today_date}/"  # img will be saved here

Path(scrnshot_img_path).mkdir(parents=True, exist_ok=True)


def create_printscreen(css_selector):
    ele = driver.find_element(By.CSS_SELECTOR, css_selector)
    if css_selector == ".plpPage-c":
        ele.screenshot(f"{scrnshot_img_path}TANÁCSADÓKNAK - {driver.title}.png")
    if css_selector == ".pao-salestool":
        ele.screenshot(f"{scrnshot_img_path}SALES TOOLS - {driver.title}.png")

    print(f"PRINTSCREEN created from: {driver.title}")


# ---------------- LOCAL CATEGORIES PART ----------------
try:
    elements = driver.find_elements(
        By.CSS_SELECTOR, "div.nav-itm:nth-child(2) masonry-brick div"
    )  # get URLs from 'Tanácsadóknak' menu
    url_list = []
    for e in elements:
        mab_url = e.get_attribute("url")
        url_list.append(mab_url)
    print("URLs loaded to array OK")
except:
    print("URLs loaded to array NOT OK")
    driver.quit()

try:
    # Loops through the 'Tanácsadóknak' menu URLs
    for i in url_list:
        driver.get(f"https://www2.avon.hu{i}")
        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            create_printscreen(".plpPage-c")
        except:
            print(f"error when loading URL: https://www2.avon.hu{i}")
    print("local category printscreens OK")
except:
    print("local category printscreens NOT OK")
    driver.quit()


# ---------------- SALES TOOLS PART ----------------
driver.get("https://www2.avon.hu/hu-home/orders/sales-tools")

try:
    sleep_time = 3
    print(f"WAITING for popup for {sleep_time} seconds")
    popup_button = "#sim button"
    WebDriverWait(driver, sleep_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, popup_button))
    )
    popup_window_close_button = driver.find_element_by_css_selector(popup_button)
    popup_window_close_button.click()
except:
    print("no popup")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".st-itm-prc"))
    )
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    create_printscreen(".pao-salestool")
    print("sales tools page success OK")
except Exception as e:
    print(e)


def next_step_click(selector):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        driver.find_element(By.CSS_SELECTOR, selector).click()
    except Exception as e:
        print(e)


next_step_click(".nxt-stp")

create_printscreen(".pao-salestool")

now = datetime.now()
end = time.time()

current_time = now.strftime("%H:%M:%S")
print(f"Script ended at {current_time} and ran {end - start} seconds")

driver.quit()
