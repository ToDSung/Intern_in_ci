import datetime
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from np_json import NumpyEncoder


def create_browser():
    driver_name = 'chromedriver_2.37.exe'
    browser_name = 'GoogleChromePortable.exe'
    driver_path = os.path.join('src', driver_name)
    app_path = os.path.join('src', 'chrome_32_65', browser_name)
    assert os.path.isfile(
        driver_path), f"Driver must exists: '{driver_path}'"
    assert os.path.isfile(
        app_path), f"browser must exists: '{app_path}'"
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.binary_location = app_path
    browser = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=driver_path)
    return browser


def get_region_information(browser):
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "#breadcrumb > li:nth-child(4) > a")))

    locations = browser.find_element_by_id('breadcrumb').text.split('>')
    region = locations[1].strip()
    country = locations[2].strip()
    city = locations[3]

    rh_value = browser.find_element_by_class_name('present_rh_value').text
    result = [region, country, city, rh_value]
    return result


def get_daily_forecast(browser):
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "city_container")))
    daily_result_list = []
    try:
        # find_elements_by_class_name 沒東西會回傳空list 不會報錯
        browser.find_element_by_class_name('city_forecast_day_object')
    except:
        daily_result_list = ['暫無天氣預測資料']
        return daily_result_list
    else:
        daily_forecasts = browser.find_elements_by_class_name(
            'city_forecast_day_object')
        for daily_forecast in daily_forecasts:
            date = daily_forecast.find_element_by_class_name(
                'city_fc_date').text.split('(')[0].strip('\n')
            day = daily_forecast.find_element_by_class_name(
                'city_fc_date').text.split('(')[1].strip(')')

            min_temp = daily_forecast.find_element_by_class_name(
                'min_temp_box').text
            max_temp = daily_forecast.find_element_by_class_name(
                'max_temp_icon').text
            daily_result = [date, day, min_temp, max_temp]
            daily_result_list.append(daily_result)
        return daily_result_list


# http://worldweather.wmo.int/tc/city.html?cityId=354 目前台北的統計資料會有問題
def get_months_statistics(browser):
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "climateTable_container")))

    each_statistics_result_list = []
    try:
        months_statistic_table = browser.find_element_by_class_name(
            'climateTable')
    except:
        each_statistics_result_list = ['該頁無統計資料']
        return each_statistics_result_list
    else:
        each_months_statistics = months_statistic_table.find_elements_by_tag_name(
            'tr')
        # Separate to row

        for i in range(1, len(each_months_statistics)):
            each_statistic_row = each_months_statistics[i].find_elements_by_tag_name(
                'td')
            # Separate to cell
            each_row_result_list = []
            for j in range(0, len(each_statistic_row)-1):
                each_row_result_list.append(each_statistic_row[j].text)
            each_statistics_result_list.append(each_row_result_list)
        return each_statistics_result_list


#Now is useless
# def is_page_have_data():
#     try:
#         WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located(
#             (By.CSS_SELECTOR, "#favButton > span")))
#     except BaseException as e:
#         print(e)
#         return False
#     else:
#         return True


def kill_process(browser):
    browser.close()
    browser.quit()


def generate_dict(region_information, daily_forecast, months_statistics):
    months_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    item_dict = {}
    item_dict['region'] = region_information[0]
    item_dict['country'] = region_information[1]
    item_dict['city'] = region_information[2]
    item_dict['rain_chance'] = region_information[3]
    item_dict['daily_forecast'] = daily_forecast
    item_dict['months_statistics'] = {}
    if months_statistics == ['該頁無統計資料']:
        item_dict['months_statistics'] = months_statistics
    else:
        for index, months in enumerate(months_abbr):
            item_dict['months_statistics'][months] = months_statistics[index]
    return item_dict


def crawl_single_page(href):

    last_web_html = browser.get(href)
    region_information = get_region_information(browser)
    daily_forecast = get_daily_forecast(browser)
    months_statistics = get_months_statistics(browser)

    single_page_dict = generate_dict(
        region_information, daily_forecast, months_statistics)

    return single_page_dict


def get_city_href_list(browser):
    url = 'http://worldweather.wmo.int/tc/home.html'
    browser.get(url)

    # Make sure the region and country option bar finish loading
    region_option = Select(WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.region_select'))))
    country_option = Select(WebDriverWait(browser, 20).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.country_select'))))

    href_list = []

    # Choose region option
    for i in region_option.options[1:]:
        region_option.select_by_visible_text(i.text)
        # Need three seconds for unkown error
        time.sleep(3)

    # Choose country option
        for j in country_option.options[1:]:
            country_option.select_by_visible_text(j.text)
            citylist = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.place_list_area')))

    # Below for loop is used to click the next button in the situation that too many cities in a country.
            for page_num in browser.find_elements_by_css_selector('#page_num > li'):

                # Get city url
                for city in citylist.find_elements_by_css_selector('div.col-12 > ul > li > a'):
                    href_list.append(city.get_attribute('href'))
                    print(city.text)
                browser.find_element_by_css_selector(
                    'body > div > div:nth-child(7) > div > div.col-3.main_right_panel > div > div.place_list_area > table > tbody > tr > td:nth-child(5) > a').click()
    return href_list


if __name__ == '__main__':

    browser = create_browser()

    '''
    unsorted_url_list = get_city_href_list(browser)
    url_list = sorted(set(unsorted_url_list), key=unsorted_url_list.index)

    url_json = json.dumps(url_list, ensure_ascii=0,
                          indent=2, cls=NumpyEncoder)
    with open('./url.json', 'wt', encoding='utf-8') as fd:
        fd.write(url_json)
    print('Get all url done')
    '''
    with open('./url.json', 'r', encoding='utf-8') as fd:
        href_list = json.load(fd)

    

    # 目前會在爬取出錯時會嘗試3次仍然失敗後，會跳過當前頁面繼續爬取，但不會有中斷程式的方式
    total_data_list = []
    for href in href_list:

        for attempt in range(1,4):
            print(href)
            try:
                total_data_list.append(crawl_single_page(href))
            except BaseException as e:
                print(e)
                print('Attempt times: {}'.format(attempt))
                kill_process(browser)
                browser = create_browser()
            else:
                break
        else:
            print('All attempt fail in cralw url: {}'.format(href))

    total_data_json = json.dumps(
        total_data_list, ensure_ascii=0, indent=2, cls=NumpyEncoder)
    with open('./weather.json', 'wt', encoding='utf-8') as fd:
        fd.write(total_data_json)
    print('done')
    kill_process(browser)
