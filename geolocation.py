from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup

browser = webdriver.Chrome(executable_path=r"C:\Users\sramamo3\Projects\tempe-graffiti\chromedriver.exe")
browser.get('http://192.168.1.1/gps/') 
sleep(3)
password = browser.find_element_by_name("inputPassword")
password.send_keys("3dfb460d")      
browser.find_element_by_id("loginSubmit").click()
sleep(3)
while True:
    sleep(3)
    html=browser.page_source
    soup = BeautifulSoup(html)
    latitude=soup.find(id="gpsStatusLatitude").getText()
    longditude=soup.find(id="gpsStatusLongitude").getText()
    print(latitude)
    print(longditude)
    print("------------------------------")

