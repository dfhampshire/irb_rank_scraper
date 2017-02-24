import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import csv

path_to_chromedriver = r'C:\Path\To\chromedriver.exe'
filename = "rankings"


def open_csv(file):
    csvfile = open('{}.csv'.format(file), 'w')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Team','Date','Score'])
    return writer

    
def connect():
    driver = webdriver.Chrome(executable_path = path_to_chromedriver)
    return driver

    
def dropdown(driver):
    url = 'http://www.worldrugby.org/rankings/mru'
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 1000)")
    element = driver.find_element_by_xpath('/html/body/section[2]/div[6]/div/div/div[3]/section/section/div[2]/div/div/a')
    driver.execute_script("arguments[0].click();", element)

def parse_data(driver, writer):
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")
    al = soup.find("table",class_="fullRankings")
    entries = al.find_all("tr")
    d = soup.find('h3',class_='lastUpdated').get_text().split(":",1)[1].replace(",","")
    for entry in entries[1:]:
        tn = entry.find(class_="teamName").get_text()
        try:
            score = entry.find_all("td")[3].get_text()
        except:
            score = ""
        adata = (tn,d,score)       
        writer.writerow(adata)
    print(d)

    
def get_all(driver, writer, index, function):
    """
    index: 1 for year, 2 for month, 3 for day
    """
    t = driver.find_element_by_xpath("/html/body/section[2]/div[6]/div/div/div[3]/section/div/div/div/div[2]/div[{}]".format(index))
    like = t.find_elements_by_tag_name("li")
    results = []
    for x in range(0,len(like)):
        if not like[x].is_displayed():
            element = t.find_element_by_class_name("current")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.1)
        element = like[x]
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.1)
        function(driver,writer)
   
   
def run():
    driver = connect()
    dropdown(driver)
    writer = open_csv(filename)
    get_all(driver,writer, 1,get_all(driver,writer,2,get_all(driver,writer,3,parse_data(driver,writer))))

    
if __name__ == '__main__':
    path_to_chromedriver = input("path to chromedriver: ")
    filename = "filename: "
    run()
    
