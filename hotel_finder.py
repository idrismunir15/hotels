#import selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options 
from dateutil import parser
import pandas as pd

options=Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

#get the names and address of all hotels in lagos.
def get_hotel_details(page_no):
    url=f"https://hotels.ng/hotels-in-lagos/{page_no}" 
    driver.get(url)
    hotels=driver.find_elements(By.CLASS_NAME, "col-xs-8")
    hotel_details=[]
    for hotel in hotels:
        name=hotel.find_element(By.TAG_NAME, "a").text
        address=hotel.find_element(By.CLASS_NAME, "listing-hotels-address").text
        link=hotel.find_element(By.TAG_NAME, "a").get_attribute('href')
        temp=hotel.find_elements(By.CLASS_NAME, "listing-hotels-facilities")
        facilities=[x.text for x in temp]
        hotel_details.append({"Name":name, "Address":address, "Link":link, "Facilities":facilities})
    #driver.quit()
    return hotel_details


w=[]
for i in range(0,361):
    print(f"page_no: {i}")
    w+=get_hotel_details(i)



#Convert to dataframe
hotel_info=pd.DataFrame(w)

hotel_info['city']=hotel_info['Address'].str.extract(r"([a-zA-Z ,]+) - ") 
hotel_info['location']=hotel_info['Address'].str.replace(r"([a-zA-Z ,]+) - ",'', regex=True)
hotel_info['Facilities']=hotel_info['Facilities'].apply(lambda x: x[0].replace('\n',',').split(','))
hotel_info.drop('Address',axis=1,inplace=True)

hotel_info.to_csv('lagos_hotels.csv')