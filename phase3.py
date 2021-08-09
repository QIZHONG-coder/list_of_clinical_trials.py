#!/usr/bin/python
# find the sponsors of phase3 clinical trials in the recruiting stage
# from https://clinicaltrials.gov/ct2/results?
# search terms:cond=Infectious+Disease&term=&cntry=&state=&city=&dist=&recrs=a&phase=2

import sys
import time
import requests
import csv
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def replacecom(alist):
    blist=[]
    for itm in alist:
        blist.append(itm.replace('"','').replace(',',';'))       
    return blist

def source(ds):
    ur = "https://clinicaltrials.gov/ct2/results?cond="+ds+"&term=&cntry=&state=&city=&dist=&recrs=a&phase=2"
    driver = webdriver.Firefox(executable_path=r'C:\Program Files (x86)\geckodriver.exe')
    driver.implicitly_wait(30)
    driver.get(ur)
    ddelement= Select(driver.find_element_by_name('theDataTable_length')) #set number of entries on the page
    ddelement.select_by_visible_text('100')
    time.sleep(10)
    sumDv=BeautifulSoup(driver.page_source, 'lxml')
    rows=sumDv.find('table', {'id':'theDataTable'}).tbody.find_all('a', href=True)
    return rows, driver, sumDv

def scraper(row): 
        uur="https://clinicaltrials.gov"+row['href']
        page=requests.get(uur)
        pro=BeautifulSoup(page.text, 'lxml')
        sponsor=pro.find("div",{"id":"sponsor"}).text.replace(",", "")
        parties=pro.find("div", {"id":"responsibleparty"}).text.replace(",", "")
        summ=pro.find("table", {"class":"ct-layout_table"}).find_all("td",{"headers":"studyInfoColData"})
        ttl=summ[len(summ)-4].text.replace(",", "").replace(";", "")
        strt=summ[len(summ)-3].text.replace(",", "")
        primary=summ[len(summ)-2].text.replace(",", "")
        complete=summ[len(summ)-1].text.replace(",", "")         
        return(replacecom([ttl, sponsor, parties, strt, primary, complete]))       

def turnPage(driver, rows):
    driver.find_element_by_xpath('//*[@id="theDataTable_next"]').click() #click next page
    time.sleep(10)
    sumDv=BeautifulSoup(driver.page_source, 'lxml')                         #load next page
    rows=sumDv.find('table', {'id':'theDataTable'}).tbody.find_all('a', href=True) #find a with link
    return rows, sumDv

def printStar(j, star):
    if j in range(0, 100, 20):
        print(star)

def main():
    if len(sys.argv)>1:
        ds=sys.argv[1]
    else:
        ds="infectious+Disease"
    with open(ds+date.today().strftime('%b%d%y')+'.csv', 'w', encoding="utf-8", newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['TITLES', 'SPONSORS', 'RESPONSIBLE PARTIES', 'START DATES', 'PRIMARY DATES', 'COMPLETION DATES'])        
        rows, driver, sumDv=source(ds)
        j=1
        for row in rows:
            csvWriter.writerow(scraper(row))#the first pages
            printStar(j, "*")
            j=j+1  

        while ('disabled' not in sumDv.find('a', {'id':'theDataTable_next'})['class']): #go through if the class disabled not there
            rows, sumDv=turnPage(driver, rows) #turn pages and find new rows
            printStar(20, ".")
            j=1
            for row in rows:
                csvWriter.writerow(scraper(row))#the rest pages
                printStar(j, "*")
                j=j+1  
    driver.quit
    csvfile.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()