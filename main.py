from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from login import username, password
from time import sleep
from random import randint
import re


def Login():

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--disable_extensions")
    firefox_options.add_argument('--profile-directory=Default')
    firefox_options.add_argument("--incognito")
    firefox_options.add_argument("--disable-plugins-discovery")
    firefox_options.add_argument("--start-maximized")
    driver = webdriver.Firefox(options=firefox_options)
 
    driver.delete_all_cookies()

    driver.get("https://ro79.grepolis.com/game/index?login=1&p=848900178&ts=1635939919")
    username_box = driver.find_element_by_xpath('//*[@id="login_userid"]')
    username_box.send_keys(username)
    password_box = driver.find_element_by_xpath('//*[@id="login_password"]')
    password_box.send_keys(password)
    login_box = driver.find_element_by_xpath('//*[@id="login_Login"]')
    login_box.click()
    delay = 5 # seconds, we wait for the login to occur
    try:
        world_box = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '.world_name > div:nth-child(1)')))
        world_box.click()
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    world_box = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/div[4]/form/div[2]/div/ul/li[1]/div')
    world_box.click()
    print("Deschide tu pagina de resurse si las-o minimizata ca primul entry.")
    input()
    return driver

def one_town_per_resource(isle_dict):
    parsed_isle_dict = {}
    for isle in isle_dict:
        min = 200000
        min_town = None
        for town in isle_dict[isle]:
            if isle_dict[isle][town] < min:
                min = isle_dict[isle][town]
                min_town = town  
        parsed_isle_dict[isle] = min_town
    return parsed_isle_dict

def create_dictionary_optimal_resource_collection(items): 
    isle_dict = {}
    current_isle = None
    current_town = None
    for item in items:
        item = item.text
        if re.search("Insula (\d+)",item):
            current_isle = re.search("Insula (\d+)",item).group(1)
            isle_dict[current_isle] = {}
            continue
        if re.search("(.+)\s(\(\d+\sPuncte\))",item):
            current_town = re.search("(.+)\s(\(\d+\sPuncte\))",item).group(1)
            isle_dict[current_isle][current_town] = None
            match = re.search("\\n(\d+)\\n(\d+)\\n(\d+)\\n",item)
            total = int(match.group(1))  + int(match.group(2)) + int(match.group(3))
            isle_dict[current_isle][current_town] = total
    parsed_isle_dict = one_town_per_resource(isle_dict)
    return parsed_isle_dict


def resource_collection(driver):
    #TODO CHECK HOW EVENT LISTENERS WORK
    # centralizator = driver.find_element_by_xpath("/html/body/div[1]/div[14]/div[3]/div")
    # centralizator.location_once_scrolled_into_view
    # hover = ActionChains(driver).move_to_element(centralizator)
    # hover.perform()
    # sleep(1)
    # villages_box = driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div/ul/li[2]/ul/li[2]/a")
    # villages_box.click()    
    # Open the overview tab
    village_overview = driver.find_element_by_xpath("/html/body/div[1]/div[26]/div/div[3]/div/div/div[3]/div[3]")
    village_overview.click()
    town_list = driver.find_element_by_id("fto_town_list")
    items = town_list.find_elements_by_tag_name("li")
    parsed_isle_dict = create_dictionary_optimal_resource_collection(items)
    #Script will only work for unique town names
    towns_to_collect_from = [value for (key, value) in parsed_isle_dict.items()]
    for town in items:
        for town_name in towns_to_collect_from:
            if town_name in town.text:
                print("gasit")
                collect_checkbox = town.find_element_by_class_name("town_checkbox") 
                sleep(randint(1,6))
                collect_checkbox.click()
    collect_button = driver.find_element_by_css_selector('#fto_claim_button > div:nth-child(3)')
    collect_button.click()
    #RESOURCE OVERFLOW MESSAGE?
    resource_overflow = None
    resource_overflow = driver.find_element_by_css_selector('.btn_confirm > div:nth-child(3)')
    if resource_overflow:
        sleep(randint(1,3))
        resource_overflow.click()
    #Minimize resource page:
    minimize_box = driver.find_element_by_xpath("/html/body/div[13]/div[1]/a")
    sleep(randint(1,4))
    minimize_box.click()

def organize_town_festival(driver):
    """
    Method used to organize town festivals.
    """
    town_festival_maximize_box = driver.find_element_by_xpath("/html/body/div[1]/div[26]/div/div[3]/div/div[1]/div[3]/div[3]")
    town_festival_maximize_box.click()

    # Leave it by default to "Festivalul orasului"
    start_all_festivals = driver.find_element_by_id("start_all_celebrations")
    sleep(randint(1,10))
    start_all_festivals.click()


    # town_festival_list = driver.find_elements_by_class_name("culture_overview_wrapper")
    # towns = town_festival_list.find_elements_by_class_name("celebration")

    # parades_checkboxes = []
    # for town in towns:
    #     try:
    #         if town.find_element_by_class_name("type_party"):
    #             button_wrapper = town.find_element_by_class_name("button_wrapper")
    #             parades_checkboxes.append(town.find_element_by_class_name("type_party"))
    #             if button_wrapper.find_element_by_class_name("disabled"):
    #                 del(parades_checkboxes[-1])
    #     except NoSuchElementException as e:
    #         pass
    
    # actions = ActionChains(town_festival_list)
    # for parade in parades_checkboxes:
    #     actions = ActionChains(driver)
    #     actions.move_to_element(parade).perform()
    #     parade.click()
 
    #Minimize Culture Page:
    minimize_box = driver.find_element_by_xpath("/html/body/div[14]/div[1]/a")
    sleep(randint(1,2))
    minimize_box.click()


driver = Login()
while(1):
    resource_collection(driver)
    sleep(randint(1,4))
    organize_town_festival(driver)
    print("Sleeping for 10 minutes")
    sleep(randint(275,309))
    print("Sleeping for 5 minutes")
    sleep(180)
    print("Sleeping for 2 minutes")
    sleep(60)
    print("Sleeping for 1 minute")
    sleep(50)
    print("Sleeping for 10 seconds")
    sleep(10)

