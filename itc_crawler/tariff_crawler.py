import configparser
import json
import os
import psutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchWindowException


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

        objective_page_html = 'http://www.macmap.org/AdvancedSearch/TariffAndTrade/AdvancedQueryResultForProducts.aspx?id={}'.format(
            query_html_id)
        browser.get(objective_page_html)

    def circuit_all_country(self):
        def choose_import_country(country):
            browser = self.browser
            input_import = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_cmbReporter_Input')))
            input_import.clear()
            print(country)
            input_import.send_keys(country)

        def choose_export_country(country):
            browser = self.browser
            input_export = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_cmbPartner_Input')))
            input_export.clear()
            # print(country)
            input_export.send_keys(country)

        def get_country_list():
            browser = self.browser
            choose_import_country_bar = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_cmbReporter_Arrow')))
            choose_import_country_bar.click()
            country = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_cmbReporter_DropDown')))
            import_country = country.find_elements_by_css_selector('li')

            country_list = []
            for each_country in import_country:
                country_list.append(each_country.text)
            return country_list
        
        country_list = get_country_list()
        browser = self.browser
        page_choosing = WebDriverWait(browser,5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_grdProductView_ctl00_ctl03_ctl01_PageSizeComboBox_Arrow')
                )           
        ).click()
        page_drop_down = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_grdProductView_ctl00_ctl03_ctl01_PageSizeComboBox_DropDown')
                )
        )
        pagesize = page_drop_down.find_element_by_css_selector('')

        for index, country in enumerate(country_list):
            choose_import_country(country)
            for index2, country2 in enumerate(country_list):
                
                if country == country2:
                    continue
                print(country2)
                try:
                    choose_export_country(country2)
                except:
                    print('error!!!!!!!!!!!!!!!!!!!!!!!!!')
                    browser.back()
                else:
                    WebDriverWait(browser, 20).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_btnShowResults'))
                    ).click()
            time.sleep(300)
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
    crawler.circuit_all_country()

    time.sleep(10)
    crawler.kill_process()
