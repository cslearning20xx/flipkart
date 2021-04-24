# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 12:09:20 2021

@author: 91998
"""


from selenium import webdriver        
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time
import random
import os.path

driver = webdriver.Chrome(executable_path=r"C:\Users\91998\chromedriver") 
driver = webdriver.Chrome(executable_path=r"C:\Users\91998\chromedriver")
baseurl = "https://www.flipkart.com/search?q=carpet&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.fulfilled_by%255B%255D%3DFlipkart%2BAssured&p%5B%5D=facets.shape%255B%255D%3DRectangle"

Csizes = ['Regular', 'Small', 'Large', 'Extra Large', 'Runner']
Ctypes = ['Runner', 'Dhurrie', 'Carpet', 'Area Rug']
Ccolors = [ 'Beige', 'Black', 'Blue', 'Brown', 'Dark Blue', 'Gold', 'Green', 'Dark Green', 'Grey', 
          'Lavendar', 'Light Blue', 'Light Green', 'Maroon',
          'Multicolor', 'Orange', 'Pink', 'Purple', 'Peach',
              'Red', 'White', 'Yellow', 'Silver' ]

AdditionalUrls = []
for CsizeOrig in Csizes:    
    for CtypeOrig in Ctypes:
        for CcolorOrig in Ccolors:
            Ctype = CtypeOrig.replace(" ", "%2B")
            Csize = CsizeOrig.replace(" ", "%2B")
            Ccolor = CcolorOrig.replace(" ", "%2B")
            x = "&p%5B%5D=facets.type%255B%255D%3D" + Ctype + "&p%5B%5D=facets.size%255B%255D%3D" + Csize + "&p%5B%5D=facets.color%255B%255D%3D" + Ccolor
            AdditionalUrls.append({'URL': x, 'CType': CtypeOrig, 'CSize': CsizeOrig, 'Ccolor': CcolorOrig })

numpages = 25

def getlinks(url, driver):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content)

    links = []
    for a in soup.findAll('div', attrs={'class':'_4ddWXP'}):   
        templink = a.find('a').get('href')                 
        links.append("https://flipkart.com" + templink)    
    return links
        
LinksAll = []
for item in AdditionalUrls:
    for i in range(numpages):
        time.sleep(max(random.gauss(2,1),1))    
        
        try:
            url = baseurl + item["URL"] + "&page=" + str(i + 1)
            links = getlinks(url, driver)
            if len(links) == 0:
                break
            else:
                for link in links:
                    LinksAll.append({"Link": link.strip(), "CType": item["CType"], "CSize": item["CSize"], "Ccolor": item["Ccolor"]})
            print("Success for CType:", item["CType"], "CSize:", item["CSize"], "Ccolor:", item["Ccolor"], "#Links", len(links))
        
        except:
            print("\t Failed! for CType:", item["CType"], "CSize:", item["CSize"], "Ccolor:", item["Ccolor"])       
            
df = pd.DataFrame(LinksAll)
df['Id'] = pd.Series(range(df.shape[0]))
df.head()
df.to_csv("C:/Users/91998/href_list.csv")

def getdata(Ctype, Csize, Ccolor, url, id, driver):
       
    tempinfo = { "CType": Ctype, "CSize": Csize, "Ccolor": Ccolor, "URL": url, "Id": id }
    driver.get(url)   
    time.sleep(max(random.gauss(3,1),2))        
   
    content = driver.page_source        
    soup = BeautifulSoup(content)    
    
    try:
        price = soup.find('div', attrs = {'class': '_30jeq3 _16Jk6d'})
        price = re.sub("[^0-9]", "", price.text)      
        tempinfo.update({"Price": int(price.strip())})  
    except:
        price = np.nan
    
    try:
        rating = soup.find('div', attrs = {'class': '_3LWZlK'}).text
        rating = float(rating.strip())
    
        ratinginfo = soup.find('span', attrs = {'class':'_2_R_DZ'}).text
        CountRating = ratinginfo.split("\xa0")[0].split(" ")[0]
        CountRating = re.sub('[^0-9]','', CountRating)
        CountRating = int(CountRating.strip())
    
        CountReview = ratinginfo.split("\xa0")[2].split(" ")[0]        
        CountReview = re.sub('[^0-9]','', CountReview)
        CountReview = int(CountReview.strip())
    except:
        rating = np.nan
        CountRating = np.nan
        CountReview = np.nan
       
   
    tempinfo.update({ "Rating": rating })   
    tempinfo.update({ "CountRating" : CountRating } )  
    tempinfo.update({ "CountReview": CountReview })  
    
    
    s = soup.find_all('li', attrs = {'class':'_21Ahn-'})
    for x in s:         
        if ":" in x.text:
            tempinfo.update({x.text.split(":")[0]: x.text.split(":")[1]})        
            
    try:
        name = soup.find('span', attrs = {'class':'B_NuCI'})
        tempinfo.update({ "Name": name.text.split("\xa0")[0]})
    except:
        name = "NA"
    
    tags = []
    vals = []
    for tag in soup.find_all('td', attrs = {'class':'_1hKmbr col col-3-12'}):
        tags.append(tag.text)
        
    for val in soup.find_all('li', attrs = {'class':'_21lJbe'}):
        vals.append(val.text)
                            
    for i in range(len(tags)):
        tempinfo.update({tags[i] : vals[i]})
    
    df = pd.DataFrame([tempinfo])
    filename = "C:/Users/91998/Flipkartnew/flipkart_data_" + str(id) + ".csv"
    df.to_csv(filename)    

href_df = pd.read_csv("C:/Users/91998/href_list.csv")

def chkfile(x):
    filename = "C:/Users/91998/Flipkartnew/flipkart_data_" + str(x) + ".csv"
    return os.path.isfile(filename)

href_df['Check'] = href_df['Id'].apply(chkfile)

index_names = href_df[ href_df['Check'] == True ].index 
href_df.drop(index_names, inplace = True)  
numurl = href_df.shape[0]
print("Count URL:",numurl)

for index, row in href_df.iterrows():        
    try:         
        getdata( row["CType"], row["CSize"], row["Ccolor"], row["Link"], row["Id"], driver)        
        print("Success URL:", index + 1 , "/", numurl )        
    except:
        print("\t Failure URL:", index + 1 , "/", numurl )  
    