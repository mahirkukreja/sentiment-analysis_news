
# coding: utf-8

# In[ ]:

# Importing libraries
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import urllib2
from bs4 import BeautifulSoup
import pickle
import re
import time
import pandas as pd
import datetime
from os import listdir
from os.path import isfile, join
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium.webdriver.chrome.options import Options
# data cleaning
from data_cleaning import unicodetoascii
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
# code starts
start=time.time()
# setting up display
display = Display(visible=0, size=(800, 800))  
display.start()
# adding chrome options to avoid errors
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36")
driver = webdriver.Chrome(chrome_options=chrome_options)
# city list
city_list=['Delhi','Hyderabad','mumbai','bangalore']
for x in city_list:
    df=pd.DataFrame(columns=['desc'])
    df.to_csv(x+"data.csv",index=False)
# crawling above cities's news for the past five days
for x in city_list:
    for i in range(5):
        driver.get("http://www.thehindu.com/news/cities/"+x+"/?page="+str(i))
        time.sleep(3)
        s=driver.page_source
        s=s.encode('utf-8','ignore')
        article_urls=(re.findall('http://www.thehindu.com/news/cities/'+x+'(/.*?/article.*?.ece)" class="Other-StoryCard-heading" title="Updated: .*?;Published: .*? IST">\n',s))
        for i in article_urls:
            driver.get("http://www.thehindu.com/news/cities/"+x+i)
            time.sleep(2)
            code=driver.page_source
            code=code.encode('utf-8','ignore')
            posted_date=re.findall('span class="blue-color ksl-time-stamp">\n<none>\n(.*?)\n</none>\n</span>\n<div class="teaser-text update-time">\nUpdated:\n<span>\n<none>\n.*?\n</none>\n</span>\n</div>\n</div>\n</div>\n',code)[0]
            if ((datetime.datetime.today()-pd.to_datetime(posted_date)).days<=5):
                try:
                    txt=re.findall('<div id="content-body-.*?" class="_hoverrDone">\n<p>(.*?)</p>\n</div>',code)
                except:
                    continue
                if len(txt)>0: 
                    df['desc']=txt
                    df.to_csv(x+"data.csv",index=False,mode='a',header=False)
                else:
                    continue
            else:
                break  
# applying vader sentiment to calculate average sentiment per city
dir_cvs='/home/ubuntu/untrodden labs hiring/'
dircvs = [join(dir_cvs, f) for f in listdir(dir_cvs) if isfile(join(dir_cvs, f))]   
final_sentiments=[]
citylis=[]
for i in dircvs:
    if i.endswith('data.csv'):
        df=pd.read_csv(i)
        sentences=df['desc'].values
        analyzer = SentimentIntensityAnalyzer()
        neg=0
        pos=0
        for sentence in sentences:
            sentence=unicodetoascii(cleanhtml(sentence))
            vs = analyzer.polarity_scores(sentence)
            pos=pos+vs['pos']
            neg=neg+vs['neg']
        if pos>neg:
            final_sentiments.append('positive')
        else:
            final_sentiments.append('negative')
        citylis.append(re.findall('/untrodden labs hiring/(.*?)data.csv',i)[0])    
    else:
        continue
# final output stored in output dataframe     
output=pd.DataFrame()
output['city']=citylis  
output['sentiment']=final_sentiments
output.to_csv('output.csv',index=False)
end=time.time()
print(end-start)

