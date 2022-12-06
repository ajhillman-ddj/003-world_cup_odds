from bs4 import BeautifulSoup
import numpy
import pandas
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
chrome_options.add_argument('user-agent={0}'.format(user_agent))
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver.exe'),options=chrome_options)

wait = WebDriverWait(driver, 20)
action = ActionChains(driver)

driver.get('https://www.oddschecker.com/football/world-cup/winner')
soup = BeautifulSoup(driver.page_source)

listOfCountries = ['Brazil', 'Argentina', 'France', 'Spain', 'England', 'Germany', 'Netherlands', 'Portugal', 'Belgium', 'Denmark', 'Uruguay', 'Croatia', 'Serbia', 'Switzerland', 'Senegal', 'Mexico', 'USA', 'Poland', 'Ecuador', 'Wales', 'Morocco', 'Japan', 'Ghana', 'Canada', 'Cameroon', 'Iran', 'South Korea', 'Australia', 'Qatar', 'Tunisia', 'Saudi Arabia', 'Costa Rica']

oddsData = []
totalProb = 0

for country in listOfCountries:
    
    countryData = soup.find( class_ = "diff-row evTabRow bc", attrs={"data-bname" : country} )

    if countryData is None:
        
        oddsArray = [0]
        
    else:
    
        oddsArray = countryData.findChildren("td", class_ = "bc", recursive=False)

        for i in range(len(oddsArray)):
            oddsArray[i] = 1/(float(oddsArray[i]["data-odig"]))

    oddsMean = numpy.mean(oddsArray)
    totalProb += oddsMean
    
    oddsData.append({"country": country, "prob": oddsMean, "currDateTime": datetime.now()})
    
for obj in oddsData:
    
    obj["prob"] = obj["prob"]/totalProb
    
pandas.DataFrame(oddsData).to_csv("outputsAdditional.csv", sep=',', encoding='utf-8', index=False, mode='a', header=False)
