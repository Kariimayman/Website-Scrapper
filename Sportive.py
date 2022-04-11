import time
import os
import validators
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.firefox.service import Service


def Sportive(Link, folderName):
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

        # Extracting the product's name
        try:
            Details = Driver.find_element(By.CLASS_NAME, "product-content")
            Name = Details.find_element(By.CLASS_NAME, "product-detail__name").text
            print("Name : " + Name)
        except:
            print("Name not Found " + folderName)

        # Extracting the product's price
        try:
            PriceDetails = Details.find_element(By.XPATH, "//div[@class='product-detail__price hidden-xs']")
            Price = PriceDetails.find_element(By.CLASS_NAME, "product-detail__sale-price").text
            print("Price : " + Price)

        except:
            print("Price not Found " + folderName)

        # Extracting the product's available sizes
        try:
            SizeDetails = Details.find_element(By.XPATH, "//div[@class='product-variant__item-options variant-sizes "
                                                         "js-product-sizes cf hidden-xs']")
            Sizes = SizeDetails.find_elements(By.TAG_NAME, "a")
            Sizesstr = ""
            print("Available Sizes :", end=" ")
            for Size in Sizes:
                if Size.text != "":
                    print(Size.text, end="  ")
                    Sizesstr = Sizesstr + " | " + Size.text
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
                PictureDetails = Driver.find_element(By.CLASS_NAME, "product-slider-inner")
                Picture = PictureDetails.find_element(By.TAG_NAME, 'img')
                Picture.click()
                for loop in range(4):
                    time.sleep(0.5)
                    Picture = Driver.find_element(By.CLASS_NAME, 'fancybox-content')
                    url = Picture.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    Response = requests.get(url)
                    if Response.status_code == 200:
                        with open(f"{path}{loop + 1}.jpg", "wb") as file:
                            file.write(Response.content)
                    Next = Driver.find_element(By.CLASS_NAME, 'fancybox-navigation')
                    NextButton = Next.find_element(By.XPATH, "//*[@title='Next']")
                    NextButton.click()
        except:
            pass
    except:
        pass
    Driver.quit()
    Sizesstr = Sizesstr.replace("| " , "" , 1)

    # Copying data to .txt File
    try:
        with open(path + "Details.txt", "w+", encoding="utf-8") as f:
            f.write(("Name : %s\n" % Name))
            f.write(("Price : %s\n" % Price))
            f.write(("Available Sizes : %s\n" % Sizesstr))
    except:
        pass

    return Price, Sizesstr
