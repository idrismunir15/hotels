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

"""_summary_

comment_extractor
------------
This function extracts comments from a hotel's page on hotels.ng

Parameters
----------
hotel_link : str
    The link to the hotel's page on hotels.ng
    
Returns
-------
None

Example
-------
comment_extractor('https://hotels.ng/hotel/1063667-royal-orchid-hotels-limited-lagos')
"""

def comment_extractor(hotel_link):
    url=f"{hotel_link}/reviews"
    driver.get(url)

    try:
        hotel_name=driver.find_element(By.CLASS_NAME, "sph-header-name").text
        hotel_name=hotel_name.replace('Reviews of ','').replace(" ","_")
        articles= driver.find_elements(By.CLASS_NAME, "sph-reviews-individual")

        comments=[]
        for article in articles:
            a={'rating': article.find_element(By.CLASS_NAME, "sph-reviews-individual-rating").text
            ,'title': article.find_element(By.CLASS_NAME, "sph-reviews-title").text
            ,'person': article.find_element(By.CLASS_NAME, "sph-reviews-person").text
            ,'comment': article.find_elements(By.TAG_NAME, 'p')[-1].text
            } 
            
            comments.append(a)


        #convert to dataframe
        comments=pd.DataFrame(comments)
        comments['Date']=comments['person'].str.extract(r"(on \w+ \d{1,2},[ ]\d{4})").replace('on ','',regex=True)
        comments['Date']=comments['Date'].apply(lambda x: parser.parse(x))
        comments.drop('person',axis=1,inplace=True)

        #save to csv
        comments.to_csv(f'comments\{hotel_name}.csv',index=False)
        print(f'{hotel_name} processed')
    except:
        pass
    return None

df=pd.read_csv('lagos_hotels.csv', usecols=['Name','Link','Facilities','city','location'])
df['Link'].apply(lambda x: comment_extractor(x))