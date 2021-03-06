##import Library
from re import I
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import pathlib
from datetime import date
from datetime import datetime
import time


# chrome_options = Options()
# chrome_options.add_argument('headless')
# target url
df = pd.read_excel(r'<Target file path>', sheet_name='PNS url')
target_list = df['PNS url'].tolist()
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

def bonus_buy(productOffer,productPrice):
    for i in range(len(productOffer)):
        if "慳$" in productOffer[i]:
            deducted_price=(productOffer[i].split("慳$",1)[1])
            bonus_buy=(productOffer[i].split("慳$",1)[0][1])
            promotionProductPrice=(float(productPrice.replace('HK$', ''))-float(deducted_price)/float(bonus_buy))
            return promotionProductPrice   
    return productPrice

def get_product_data(target_url):
    product_offer_list = []
    time.sleep(1)
    r = driver.get(target_url)
    time.sleep(1)
 
    # web element locator 
    productName = driver.find_element_by_xpath(
        '/html/body/div[5]/main/div[1]/div[2]/div[1]/div[1]/h1').text
    productBrand = driver.find_element_by_xpath(
        '/html/body/div[5]/main/div[1]/div[2]/div[1]/div[1]/a/span').text
    productPrice = driver.find_element_by_xpath('/html/body/div[5]/main/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/div/span[1]').text.replace('HK$', '')
    driver.save_screenshot(r'<Target file path>'+'PNS '+productName+datetime.strftime(date.today(), ' %d%m%Y')+".png")
    try: 
        driver.find_element_by_xpath('/html/body/div[5]/main/div[1]/div[2]/div[2]/div[6]/div[3]/div[1]/span').click()
        productOfferGrid = driver.find_elements_by_class_name("info")
        for offer in productOfferGrid:
            product_offer_list.append(offer.text)
            productOffer=product_offer_list
        promotionProductPrice=bonus_buy(productOffer,productPrice)
    except:
        productOffer = ''
        promotionProductPrice=productPrice

    # try:
    #     for i in range(len(productOffer)):
    #         if "慳$" in productOffer[i]:
    #             deducted_price=(productOffer[i].split("慳$",1)[1])
    #             bonus_buy=(productOffer[i].split("慳$",1)[0][1])
    #             promotionProductPrice=(float(productPrice.replace('HK$', ''))-float(deducted_price)/float(bonus_buy))
    # except:
    #     promotionProductPrice=productPrice
    
    productId = driver.find_element_by_xpath(
        '/html/body/div[5]/main/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/span').text

    ItemDetails = {
        'product Name': productBrand+productName,
        'Brand': productBrand,
        'Price': productPrice,
        'Promotion Price': promotionProductPrice,
        'PNS Product ID': productId,
        'Product Offer': str(productOffer).replace("', '", ',\n'),
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
df.to_excel(script_path+'\\record\\PNS product_detail'+datestring+'.xlsx')
print('saved to file')

# close the webdriver after finish all
driver.quit()
