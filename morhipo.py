import time
import os
import validators
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.firefox.service import Service


def Morhipo(Link, folderName):
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

        # Extracting the product's brand
        try:
            Details = Driver.find_element(By.CLASS_NAME, "prod-detail-header")
            Brand = Details.find_element(By.ID, "ela-urun-detay-marka").text
            print("Brand : " + Brand)
        except:
            print("Brand Not found " + folderName)

        # Extracting the product's name
        try:
            Details = Driver.find_element(By.CLASS_NAME, "prod-detail-header")
            Name = Details.find_element(By.CSS_SELECTOR, ".text-muted").text
            print("Name : " + Name)
        except:
            print("Name Not found " + folderName)

        # Extracting the product's price
        try:
            PriceDetails = Driver.find_element(By.ID, "product-price")
            Price = PriceDetails.find_element(By.TAG_NAME, "strong").text
            print("Price : " + Price)
        except:
            print("Price not Found " + folderName)

        # Extracting the product's available sizes
        try:
            SizeDetails = Driver.find_element(By.ID, "sizeDiv")
            Sizes = SizeDetails.find_elements(By.TAG_NAME, 'label')
            print("Available Sizes :", end=" ")
            Sizesstr = ""
            flag = False
            for Size in Sizes:
                temp = Size.find_element(By.TAG_NAME, 'input')
                if temp.get_attribute('available') != "0":
                    Value = Size.get_attribute('title')
                    print(Value, end="  ")
                    Sizesstr = Sizesstr + " | " + Value
                    flag = True
            print("\n")
        except:
            if not flag:
                Sizesstr = "Not Available"
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
                PictureDetails = Driver.find_element(By.ID, "lookup-0")
                Picture = PictureDetails.find_element(By.TAG_NAME, 'img')
                Picture.click()
                for loop in range(4):
                    time.sleep(0.5)
                    Picture = Driver.find_element(By.CLASS_NAME, 'current')
                    url = Picture.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    Response = requests.get(url)
                    if Response.status_code == 200:
                        with open(f"{path}{loop + 1}.jpg", "wb") as file:
                            file.write(Response.content)
                    Next = Driver.find_element(By.CLASS_NAME, 'smartphoto-arrow-right')
                    NextButton = Next.find_element(By.TAG_NAME, "a")
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
