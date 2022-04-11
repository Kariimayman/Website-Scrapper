import time
import os
import validators
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def Trendyol(Link, folderName):
    # initializing
    s = Service("geckodriver.exe")
    Sizesstr = "Not Available"
    Price_value = "Not Available"
    link = Link
    validation = validators.url(link)

    # Validating the website
    if validation:
        options = Options()
        options.headless = True
        Driver = webdriver.Firefox(service=s, options=options, )
        Driver.get(link)
    else:
        print(link + " is not a valid URL")
        return Price_value, Sizesstr
    try:

        # Extracting the product's name
        try:
            Name = Driver.find_element(By.CLASS_NAME, "pr-new-br").text
            print("Product Name : " + Name)
        except:
            print("Name not found " + folderName)

        # Extracting the product's price
        try:
            Price = Driver.find_element(By.CLASS_NAME, 'pr-bx-w')
            try:
                Price_value = Price.find_element(By.CLASS_NAME, "prc-dsc").text
            except:
                Price_value = Driver.find_element(By.CLASS_NAME, "prc-slg").text
            print("Price : " + Price_value)
        except:
            print("Price not found " + folderName)

        # Extracting the product's Available sizes
        Driver.refresh()
        time.sleep(3)
        counter = 1
        try:
            Sizes = Driver.find_element(By.CLASS_NAME, "variants")
            Sizesstr = ""
            while True:
                size = Sizes.find_element(By.XPATH, f"//*[@class = 'sp-itm' or @class = 'selected sp-itm'][{counter}]")
                Sizesstr = Sizesstr + " | " + size.text
                counter = counter + 1
        except:
            if counter == 1:
                Sizesstr = "Not Available"
                print("Sizes not found " + folderName)
            else:
                print(Sizesstr[2:])

        # Extracting the product's pictures
        try:
            FolderFlag = False
            path = "Pictures\\" + folderName + "\\"
            try:
                os.mkdir(path)
            except:
                FolderFlag = True
            if not FolderFlag:
                Picture = Driver.find_element(By.CLASS_NAME, "base-product-image")
                Picture.click()
                for loop in range(4):
                    time.sleep(0.5)
                    Picture = Driver.find_element(By.CLASS_NAME, "gallery-modal-content")
                    url = Picture.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    response = requests.get(url)
                    if response.status_code == 200:
                        with open(f"{path}{loop + 1}.jpg", "wb") as file:
                            file.write(response.content)
                    nextB = Picture.find_element(By.CSS_SELECTOR, ".i-arrow-right.right")
                    nextB.click()
        except:
            pass
    except:
        pass
    Driver.quit()
    Sizesstr = Sizesstr.replace("| ", "", 1)

    # Copying data to .txt File
    try:
        with open(path + "Details.txt", "w+", encoding="utf-8") as f:
            f.write(("Name : %s\n" % Name))
            f.write(("Price : %s\n" % Price_value))
            f.write(("Available Sizes : %s\n" % Sizesstr))
    except:
        pass

    return Price_value, Sizesstr
