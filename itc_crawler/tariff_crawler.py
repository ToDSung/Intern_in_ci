import configparser
import json
import os
import psutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


class base_crawler1(object):

    def __init__(self):

        self.url = 'http://www.macmap.org/Default.aspx'

        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.email = config['itc']['username']
        self.passwd = config['itc']['password']

    def create_browser_on_windows(self):
        self.driver_name = 'chromedriver_2.37.exe'
        self.browser_name = 'GoogleChromePortable.exe'
        self.driver_path = os.path.join('src', self.driver_name)
        self.app_path = os.path.join('src', 'chrome_32_65', self.browser_name)
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.binary_location = self.app_path
        #webdriver.Chrome(chrome_options=chrome_options, executable_path=self.driver_path)
        self.browser = webdriver.Chrome(
            chrome_options=chrome_options, executable_path=self.driver_path)

    def do_login(self):
        """
        頁面登入
        """
        browser = self.browser
        browser.get(self.url)
        login_if = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#iframe_login')))
        browser.switch_to.frame(login_if)

        element = browser.find_element_by_css_selector(
            '#PageContent_Login1_UserName')
        element.send_keys(self.email)

        element = browser.find_element_by_css_selector(
            '#PageContent_Login1_Password')
        element.send_keys(self.passwd)

        element = browser.find_element_by_css_selector(
            '#PageContent_Login1_Button')
        element.click()

        # browser.switch_to.default_content()

    def to_setted_up_query_page(self):
        time.sleep(5)
        browser = self.browser
        browser.get(
            'http://www.macmap.org/AdvancedSearch/TariffAndTrade/Manage.aspx')

        element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_grdAnalysisQueries_ctl00__0')))

        element = browser.find_element_by_css_selector(
            '#ctl00_ContentPlaceHolder1_grdAnalysisQueries_ctl00__0 > td:nth-child(1) > a')
        query_html = element.get_attribute('href')
        query_html_id = query_html.split('=')[1]

        objective_page_html = 'http://www.macmap.org/AdvancedSearch/TariffAndTrade/AdvancedQueryResultForProducts.aspx?id={}'.format(query_html_id)
        browser.get(objective_page_html)

    

        

    def kill_process(self):
        try:
            self.browser.close()
            self.browser.quit()

            PROCNAME = self.driver_name
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()
        except:
            print('except')
            pass


if __name__ == '__main__':

    crawler = base_crawler1()
    crawler.create_browser_on_windows()
    crawler.do_login()
    crawler.to_setted_up_query_page()
    
    
    
    #time.sleep(10)
    #crawler.kill_process()
