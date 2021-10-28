##import Library
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import os
import pathlib
from datetime import date
from datetime import datetime
import time

# target url

df = pd.read_excel('target.xlsx', sheet_name='WAT url')
target_list = df['WAT url'].tolist()
# access url by using webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
targetProductdetail = []

# pop up message handler


def remove_popup():
    try:  # popup message handler
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "icon-close-button-1625037548411"))).click()
    except:
        print("no popup message!")


def get_product_data(target_url):
    product_offer_list = []
    r = driver.get(target_url)
    remove_popup()
    time.sleep(0.2)
    # web element locator
    productName = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/e2-product-summary/h1').text
    productBrand = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/e2-product-summary/h2/a').text
    productPrice = driver.find_element_by_class_name('displayPrice').text
    productOffer = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[6]/e2-product-promotions-details/div/div[2]/div').text
    productId = driver.find_element_by_xpath(
        '/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[10]/e2-product-code/p/span').text

    if any(str.format("第2件半價") in od for od in productOffer.splitlines()):
        promotionProductPrice = float(
            productPrice.replace('$', ''))*0.5
    else:
        promotionProductPrice = productPrice.replace('$', '')

    ItemDetails = {
        'product Name': productName,
        'Brand': productBrand,
        'Price': productPrice.replace('$', ''),
        'Promotion Price': promotionProductPrice,
        'WAT Product ID': productId,
        'Product Offer': productOffer,
        'Record Time': date.today()
    }
    targetProductdetail.append(ItemDetails)


for url in target_list:
    get_product_data(url)

print(targetProductdetail)

# use pandas to create dataframe and export to excel or csv
script_path = os.path.dirname(os.path.abspath(__file__))
pathlib.Path(script_path+'\\record').mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(targetProductdetail)
datestring = datetime.strftime(date.today(), ' %d%m%Y')
# df.to_csv('product_detail.csv')
df.to_excel(script_path+'\\record\\Watsons product_detail'+datestring+'.xlsx')
print('saved to file')

# close the webdriver after finish all
driver.quit()
