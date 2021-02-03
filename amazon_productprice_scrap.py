# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 00:02:49 2020

@author: winwo
"""

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

""" changing web browser driver can be done by changing the webdriver_manager above and code in line 65
     for example  for chrome, import change to -> from webdriver_manager.chrome import ChromeDriverManager
     and for line 65 change to -> driver = webdriver.Chrome(ChromeDriverManager().install())"""



'''scraping function'''

def extract_record(item):
    
  
     #'''Product name and hyperlink'''
    
    atag=item.h2.a
    desc=atag.text.strip()
   
    
    atag.get('href')
    product_url= 'https://www.amazon.com' + atag.get('href')
   
      
        #price
    try:    
        price=item.find('span',{'class','a-offscreen'})
        price=price.text.strip()
    except AttributeError:
        price=''
      
        #rating
    try:
        rating=item.find('span',{'class':'a-icon-alt'})
        rating=rating.text.strip()
    except AttributeError:
         rating=''
   
    
        #rating count
    try:
        rating_c=item.find('span',{'class','a-size-base'})
        rating_c=rating_c.text.strip()
    except AttributeError:
        rating_c=''
    
    
    result=(desc,price,product_url,rating,rating_c)
    return result

    

'''main function'''

record_list=[]

def main(search_term,langua='zh_TW'):
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    
    #variables
    page=1
   
    
    for i in range(1,21): 
        def get_url(search_term,langua='zh_TW'):
            """"generate url from search term and product ID, where search term is product's url"""
            searchterm=search_term.replace(' ','+')
            language=langua
            template=f"https://www.amazon.com/s?k={searchterm}&page={page}&language={language}&ref=sr_pg_{page}"
            return template
        
        
        #open and soup html
        url=get_url(search_term,langua='zh_TW')
        driver.get(url)
        soup=BeautifulSoup(driver.page_source, 'html.parser')
        results=soup.find_all('div',{"data-component-type":'s-search-result'})
        try:
            item = results[0]
        except IndexError:
            break
        #scraping function and using break if there is no result
        print(len(record_list))
       
        
        for item in results:
            record=extract_record(item)
            if record:
                record_list.append(record)
            
        page=page+1
   
    driver.close()
    with open('Screwdriver.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['description','price','product url','rating','number of customer rated'])
        writer.writerows(record_list)

if __name__ == '__main__':
    main('screwdriver')