from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import requests
import wget
import os
import fitz
import io


from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


def HuntPeople():

    driver = webdriver.Chrome("utils\chromedriver.exe")
    driver.get("https://pnzgu.ru/Abitur/abitur_2020/prikaz_2020")

    content = driver.find_element_by_class_name("content-page")
    items = content.find_elements_by_tag_name("a")
    for item in items:
        # WebDriverWait(driver, 2).until(expected_conditions.visibility_of_element_located((By.TAG_NAME , "a")))
        # elem = item.find_element_by_tag_name("a")
        if "Политехнический" in item.text:
            link = item.get_attribute('href')
            print(link)
            #download link
            wget.download(link,"buffer_pdf.pdf")
            print('yes')
            #open pdf
            pdf_document = "buffer_pdf.pdf"  
            doc = fitz.open(pdf_document)   

            #write this data to txt for easy reading))))
            datafile = open('buffer_txt.txt','w')
            for page in doc:
                datafile.write(page.getText("text"))
            datafile.close()

            #delete pdf
            os.remove("buffer_pdf.pdf")

            #pasre data
            #maybe to bd of json

            #delete txt
            os.remove("buffer_txt.txt")



    driver.close()


HuntPeople()

class ScrappIOHunter:

    def __init__(self, email, pwd):


        # req_proxy = RequestProxy()
        # self.proxies = req_proxy.get_proxy_list()
        self.email = email
        self.pwd = pwd
        self.iProxy = 0
        self.driver = None
        self.driver = webdriver.Chrome("utils\chromedriver.exe")
        #self.Reload()
        self.driver.get("https://skrapp.io/login")
        #login 
        email = self.driver.find_element_by_name("email")
        pwd = self.driver.find_element_by_name("pwd")
        # "viktor.alekseev.botov1@gmail.com" "_Viktor1_"
        email.send_keys(self.email)
        pwd.send_keys(self.pwd)
        self.driver.find_element_by_css_selector(".btn-info").click()
    

    # def Reload(self):
    #     PROXY = self.proxies[self.iProxy].get_address()
    #     webdriver.DesiredCapabilities.CHROME['proxy']={
    #         "httpProxy":PROXY,
    #         "ftpProxy":PROXY,
    #         "sslProxy":PROXY,
    #         "proxyType":"MANUAL",   
    #     }
    #     self.driver = webdriver.Chrome("C:\WORK\ASSISTANCE\chromedriver.exe")


    def FindRoles(self,domain,roles):
        #here will be find
        jsonData = ''
        self.driver.refresh()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT , "Domain Search")))
        elem = self.driver.find_element_by_link_text("Domain Search")
        self.driver.execute_script("arguments[0].click();", elem)

        dom = self.driver.find_element_by_name("domain")
        dom.send_keys(domain)

        ## there was an error, button not abled to click, but it solved here no-result

        try:
            WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located((By.ID, "undefined")))
            elem = self.driver.find_element_by_id("undefined")
            self.driver.execute_script("arguments[0].click();", elem)

            #clicking  btn "more results"
            WebDriverWait(self.driver, 2).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR , ".showMore")))
            elem = self.driver.find_element_by_css_selector(".showMore")
            while elem.text != "No more results":
                self.driver.execute_script("arguments[0].click();", elem)
                time.sleep(1)
                WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR , ".showMore")))
                elem = self.driver.find_element_by_css_selector(".showMore")

            #here now we are will filter roles
            items = self.driver.find_elements_by_class_name("result")
            resultData=[]
            for item in items:
                name = item.find_element_by_class_name("name").text.split(' ')
                firstname = name[0]
                lastname = name[1]
                #разделить строку name по пробелу
                role = item.find_element_by_class_name("title").text
                if (any(r == role for r in roles)): #потом более умную проверку сделать типо регистры хуистры
                    #email = ScrappHunter.FindEmail("will be api",firstname,lastname,domain)
                    rItem = {
                        "firstname": firstname,
                        "lastname" : lastname,
                        "role":role,
                        "domain": domain,
                        "email": "email"
                        #if here is a role, we can find it at this service
                    }
                    resultData.append(rItem)
                    jsonData=json.dumps(resultData)
        finally:
            return jsonData

    
    def LogOut(self):
        WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located((By.ID, "options")))
        elem = self.driver.find_element_by_id("options")
        self.driver.execute_script("arguments[0].click();", elem)

        WebDriverWait(self.driver, 100).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT , "Logout")))
        elem = self.driver.find_element_by_link_text("Logout")
        self.driver.execute_script("arguments[0].click();", elem)
        self.driver.close()