import time
import os
import validators
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def Decathlon(Link, folderName):

    # initializing
    s = Service("geckodriver.exe")
    Price = "Not Available"
    Sizesstr = "Not Available"

    # Validating the website
    link = Link
    validation = validators.url(link)
    if validation:
        options = Options()
        options.headless = True
        Driver = webdriver.Firefox(service=s, options=options, )
        Driver.get(link)
    else:
        print(link + " is not a valid URL")
        return Price, Sizesstr
    try:
        time.sleep(1.5)
        Buttons = Driver.find_element(By.ID, "buttons")
        AcceptButton = Buttons.find_element(By.XPATH, "//button[@id = 'didomi-notice-agree-button']")
        AcceptButton.click()

        # Extracting the product's price
        try:
            PriceDetails = Driver.find_element(By.CLASS_NAME, "prc__cartridge")
            Price = PriceDetails.find_element(By.XPATH, "//div[contains(@class,'prc__active-price')]").text
            print("Price : " + Price)
        except:
            print("Price not Found " + folderName)

        # Extracting the product's available sizes
        try:
            SizeDetails = Driver.find_element(By.CLASS_NAME, "svelte-1cr01ag")
            SizeDetails.click()
            Sizes = SizeDetails.find_elements(By.TAG_NAME, "li")
            Sizesstr = ""
            print("Available Sizes :", end=" ")
            for Size in Sizes:
                try:
                    Size.find_element(By.CSS_SELECTOR,
                                                ".sku-selector.svelte-1dkais7 li:not(.selected) .stock.no")
                except:
                    AvailableSize = Size.find_element(By.TAG_NAME, "span").text
                    print(AvailableSize, end=" ")
                    Sizesstr = Sizesstr + " | " + AvailableSize
            if Sizesstr == "":
                Sizesstr = "Not Available"
            print("\n")
        except:
            print("Size not Found " + folderName)

        # Extracting the product's pictures
        try:
            FolderFlag = False
            path = "Pictures\\" + folderName + "\\"
            try:
                os.mkdir(path)
            except:
                FolderFlag = True
            if not FolderFlag:
                Slider = Driver.find_element(By.ID, "thumbnails-slider")
                Pictures = Slider.find_element(By.XPATH, "//button[@class = 'thumbnail svelte-kkzyj5']")
                for loop in range(2):
                    Selector = Driver.find_element(By.XPATH, "//button[@class = 'thumbnail svelte-kkzyj5 selected']")
                    Picture = Selector.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    Response = requests.get(Picture)
                    if Response.status_code == 200:
                        with open(f"{path}{loop + 1}.jpg", "wb") as file:
                            file.write(Response.content)
                    Pictures.click()
                    time.sleep(1)
        except:
            pass
    except:
        pass
    Driver.quit()
    Sizesstr = Sizesstr.replace("| " , "" , 1)

    # Copying data to .txt File
    try:
        with open(path + "Details.txt", "w+", encoding="utf-8") as f:
            f.write(("Price : %s\n" % Price))
            f.write(("Available Sizes : %s\n" % Sizesstr))
    except:
        pass

    return Price, Sizesstr
