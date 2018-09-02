import scrapy
from walmart.items import WalmartItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from scrapy.http import TextResponse
from lxml import html
from lxml import etree
import csv
import unicodedata
from selenium.webdriver.common.by import By
import time
import datetime
from dateutil.tz import tzlocal
import pytz
class DictUnicodeProxy(object):
    def __init__(self, d):
        self.d = d
    def __iter__(self):
        return self.d.__iter__()
    def get(self, item, default=None):
        i = self.d.get(item, default)
        if isinstance(i, unicode):
            return i.encode('utf-8')
        return i
class WalmartSpider(scrapy.Spider):
    name = "walmart"

    def __init__(self):
        chrome_driver = "walmart/chromedriver/chromedriver.exe"
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary
        self.driver = webdriver.Chrome(chrome_driver, chrome_options = options)
        
    def start_requests(self):
        self.start_urls = ['https://exchangemarketplace.com/categories/established-stores-for-sale']
          
        response =  HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        self.parse(response)
    
    def parse(self, response):
      
        timezone = pytz.timezone("America/Los_Angeles")
        now = datetime.datetime.now(timezone)
        fmt1 = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        fmt=str(fmt1).encode('utf-8').replace("\n",'').replace("\\n",'').replace("'",'').replace(",",'').replace('<','').replace(':','-').replace("200",'').replace(" ",'-').strip()
        with open('result/'+str(fmt)+'.csv', 'wb') as csvfile:
            sIndex=0
            sPage=0
            
            fieldnames = ["Marketplace", "ListingTitle", "BusinessName", "AskingPrice", "NetProfit", "GrossRevenue", "Inventory", "averagesales", "sessions","lastxmonth", "Description", "BusinessWebsite","ListingLink","updatetime"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            csvfile.close() 
            # self.driver.get("https://exchangemarketplace.com/categories/fashion-and-apparel-businesses-for-sale?&page=1")   
            print("==========================================Scraping Start==========================================") 
            # last_height = self.driver.execute_script("return document.body.scrollHeight")
            while(1):
                item = WalmartItem()
                Marketplace="Shopify Exchange"
                item['Marketplace']=Marketplace.encode('utf-8')
                try:
                    (self.driver.find_elements_by_xpath("//div[@class='shop-tile__content shop-tile__content--border-bottom shop-tile__header']/a/p[@class='shop-tile__url heading--truncated']"))[sIndex%24].click()
                    pass
                except Exception as e:
                    pass
                    
                try:
                    ListingTitle = self.driver.find_elements_by_xpath("//div[@class='grid']/div[@class='grid__item grid__item--desktop-up-two-thirds']/section[@class='section section--tight']/h1[@class='heading--2 shop-title']")[0].text
                    item['ListingTitle'] =ListingTitle.encode('utf-8')
                    pass
                except Exception as e:
                    item['ListingTitle'] = ""
                    pass
                try:
                    BusinessName = self.driver.find_elements_by_xpath("//div[@class='grid']/div[@class='grid__item grid__item--desktop-up-two-thirds']/section[@class='section section--tight']/h1[@class='heading--2 shop-title']")[0].text
                    item['BusinessName'] = BusinessName.encode('utf-8')
                    pass
                except Exception as e:
                    item['BusinessName'] = ""
                    pass
                try:
                    item['AskingPrice'] = self.driver.find_elements_by_xpath('.//*[@id="Main"]/div[2]/div/div/p/span[1]')[0].text
                    #//*[@id="Main"]/div[2]/div/div/p/span[1]  //*[@id="Main"]/div[3]/div[2]/section/div/div/p/span[1]
                    # print("================================================asking price==========================="+str(AskingPrice))
                    # item['AskingPrice']=AskingPrice.encode('utf-8')
                    pass
                except Exception as e:
                    item['AskingPrice'] = ""
                    pass
                try:
                    item['NetProfit'] = self.driver.find_elements_by_xpath("//div[@class='grid__item grid__item--tablet-up-half'][1]/div[@class='block gutter-bottom']/div[@class='block__content gutter-bottom--reset']/p[@class='heading--3 font-regular']/span[@class='text-standout']")[0].text
                    pass
                except Exception as e:
                    item['NetProfit'] = ""
                    pass
                try:
                    item['GrossRevenue'] = self.driver.find_elements_by_xpath("//div[@class='grid__item gutter-bottom']/div[@class='block gutter-bottom']/div[@class='block__content gutter-bottom--reset']/p[@class='heading--3 font-regular']/span[@class='text-standout']")[0].text
                    pass
                except Exception as e:
                    item['GrossRevenue'] = ""
                    pass
                try:
                    item['Inventory'] = self.driver.find_elements_by_xpath("//div[@class='grid__item grid__item--tablet-up-half gutter-bottom'][2]/div[@class='block gutter-bottom']/div[@class='block__content gutter-bottom--reset']/p[@class='heading--3 font-regular']/span[@class='text-standout']")[0].text
                    pass
                except Exception as e:
                    item['Inventory'] = ""
                    pass
                try:
                    item['averagesales'] = self.driver.find_elements_by_xpath("//div[@class='grid__item grid__item--tablet-up-half gutter-bottom']/div[@class='block gutter-bottom']/div[@class='block__content gutter-bottom--reset']/p[@class='heading--3 font-regular']/span[@class='text-standout']")[0].text
                    pass
                except Exception as e:
                    item['averagesales'] = ""
                    pass
                try:
                    item['sessions'] = self.driver.find_elements_by_xpath("//div[@class='grid__item']/div[@class='block gutter-bottom']/div[@class='block__content gutter-bottom--reset']/p[@class='heading--3 font-regular']/span[@class='text-standout']")[0].text
                    pass
                except Exception as e:
                    item['sessions'] = ""
                    pass
                try:
                    item['lastxmonth'] = self.driver.find_elements_by_xpath("//section[@class='section section--tight']/section[@class='section section--tight section--padding-bottom-only']/div[@class='sidebar-box seller background-off-white']/div[@class='seller__content'][1]/p[@class='gutter-bottom--reset']")[0].text
                    pass
                except Exception as e:
                    item['lastxmonth'] = ""
                    pass
                try:
                    Description = self.driver.find_elements_by_xpath("//section[@class='section section--tight']/section[@class='section section--tight'][1]/div[@class='long-form-content']/p")[0].text
                    item['Description'] =Description.encode('utf-8')
                    pass
                except Exception as e:
                    item['Description'] = ""
                    pass
                try:
                    BusinessWebsite = self.driver.find_elements_by_xpath("//div[@class='grid__item grid__item--desktop-up-two-thirds']/section[@class='section section--tight']/p[@class='gutter-bottom--quarter']")[0].text
                    item['BusinessWebsite'] =BusinessWebsite.encode('utf-8')
                    pass
                except Exception as e:
                    item['BusinessWebsite'] = ""
                    pass
                try:
                    ListingLink = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                    item['ListingLink']=str(ListingLink).encode('utf-8').replace("\n",'').replace("\\n",'').replace("'",'').replace(",",'').replace('<','').replace('>','').replace("200",'').strip()
                    pass
                except Exception as e:
                    item['ListingLink'] = ""
                    pass 
                try:
                    timezone = pytz.timezone("America/Los_Angeles")
                    now = datetime.datetime.now(timezone)
                    fmt1 = now.strftime('%Y-%m-%d %H:%M:%S %Z')
                    item['updatetime']=str(fmt1).encode('utf-8').replace("\n",'').replace("\\n",'').replace("'",'').replace(",",'').replace('<','').replace('>','').replace("200",'').strip()
                    pass
                except Exception as e:
                    item['updatetime'] = ""
                    pass 
                self.driver.back()
                
                sIndex+=1
                
                if sIndex%24==0:
                    sPage = sIndex/24
                    self.driver.get("https://exchangemarketplace.com/categories/fashion-and-apparel-businesses-for-sale?&page="+str(sPage))
               
                with open('result/'+str(fmt)+'.csv', 'a') as csvfile:
                 
                    fieldnames = ["Marketplace", "ListingTitle", "BusinessName", "AskingPrice", "NetProfit", "GrossRevenue", "Inventory", "averagesales", "sessions","lastxmonth", "Description", "BusinessWebsite", "ListingLink","updatetime"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
                    writer.writerow(item)
                    csvfile.close() 
                if sIndex%6==0: 

                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")   
                    
                    
                   
                if sIndex == 817:
                    break
        with open('result/'+str(fmt)+'.csv', 'rb') as inp, open('result/'+str(fmt)+'-Result.csv', 'wb') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if row[11]=="data:":
                    pass
                else:
                    writer.writerow(row)            
    pass
