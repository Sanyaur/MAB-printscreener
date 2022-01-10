from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

from time import sleep
from datetime import datetime

# -----HEADLESS SCRIPT-----
# from selenium.webdriver.firefox.options import Options

# options = Options()
# options.headless = True

# PATH = "c:/Program Files (x86)/geckodriver.exe"
# driver = webdriver.Firefox(options=options, executable_path=PATH)
# -----HEADLESS SCRIPT-----

PATH = "c:/Program Files (x86)/geckodriver.exe"
driver = webdriver.Firefox(executable_path=PATH)

scrnshot_img_path = "c:/Users/ujvaris/OneDrive - Avon/Desktop/_to_be_deleted/MAB sprint screenshots/"  # img will be saved here


def set_window_size():
    # get window size
    size = driver.get_window_size()
    width1 = size.get("width")
    height1 = driver.execute_script("return document.documentElement.scrollHeight")

    driver.set_window_size(width1, height1)


def login_field():
    username = driver.find_element_by_id("sellerUserId")
    password = driver.find_element_by_id("sellerEmailPassword")

    username.send_keys("6290011")
    password.send_keys("ezEgyJelszó!01" + Keys.ENTER)


driver.get("https://www2.avon.hu/hu-home/product-catalog.html")  # opens MAB

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sellerEmailPassword"))
    )
    print("login page ✅")
    login_field()
except:
    print("login page ❌")

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sub-div"))
    )
    print("product-catalog ✅")
except:
    print("product-catalog ❌")


def create_printscreen(css_selector):
    ele = driver.find_element(By.CSS_SELECTOR, css_selector)
    if css_selector == ".plpPage-c":
        ele.screenshot(f"{scrnshot_img_path}TANÁCSADÓKNAK - {driver.title}.png")
    if css_selector == ".pao-salestool":
        ele.screenshot(f"{scrnshot_img_path}SALES TOOLS - {driver.title}.png")

    # driver.save_screenshot(scrnshot_img_path + driver.title + ' .png') # takes screenshot
    print(f"Printscreen created from: {driver.title}")


elements = driver.find_elements(
    By.CSS_SELECTOR, "div.nav-itm:nth-child(2) masonry-brick div"
)  # get URLs from 'Tanácsadóknak' menu
url_list = []
for e in elements:
    mab_url = e.get_attribute("url")
    url_list.append(mab_url)

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


# ---------------- SALES TOOLS PART ----------------
driver.get("https://www2.avon.hu/hu-home/orders/product-entry")


try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".dnt-btn > button:nth-child(1)")
        )
    )
    driver.find_element_by_css_selector(".dnt-btn > button:nth-child(1)").click()
    print("product entry page loaded")
except:
    print("product entry page failed")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".shpByProdNum > tab-entry-core:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > input:nth-child(2)",
            )
        )
    )
    driver.find_element_by_css_selector(".dnt-btn > button:nth-child(1)").click()
    print("input fields loaded")
except:
    print("input fields failed")


def ln_input_field(num):
    ln_input_field = driver.find_element_by_css_selector(
        f".shpByProdNum > tab-entry-core:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child({num}) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"
    )
    return ln_input_field


def county_box(num):
    ln_input_field = driver.find_element_by_css_selector(
        f".shpByProdNum > tab-entry-core:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child({num}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"
    )
    return ln_input_field


def LN_input_page():
    try:
        popup_button = ".nav_wrap > span:nth-child(1)"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, popup_button))
        )
        product_popup_X = driver.find_element_by_css_selector(popup_button)
        product_popup_X.click()
    except:
        print("nincs popup")

    order_list = ["00018", 1]
    termeklista = order_list[::2]
    product_count = order_list[1::2]

    ln_input_field_child = 1
    for line_number in range(len(termeklista)):
        ln_input_field(ln_input_field_child).send_keys(str(termeklista[line_number]))
        county_box(ln_input_field_child).send_keys(str(product_count[line_number]))
        ln_input_field_child += 1
        sleep(0.7)

    tovabb_button = driver.find_element_by_id("btnCont")

    termek_mentese_button = driver.find_element_by_css_selector(
        ".shpByProdNum > tab-entry-core:nth-child(2) > div:nth-child(1) > div:nth-child(3) > button:nth-child(2)"
    )
    termek_mentese_button.click()

    tovabb_button.click()


LN_input_page()


def next_step_click(selector):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    driver.find_element_by_css_selector(selector).click()


create_printscreen(".pao-salestool")
next_step_click(".nxt-stp")
create_printscreen(".pao-salestool")

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print(f"Script ended at {current_time}")

driver.quit()
