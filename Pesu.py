import os
import json
import re
import time
import getpass
import requests
import lxml
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

FORMAT = 'utf-8'
CURRENT_DIRECTORY = Path.cwd()
VIDEOS_DIRECTORY = CURRENT_DIRECTORY / 'videos'
VIDEOS_FILE = CURRENT_DIRECTORY / 'videos.json'
PESU_URL = 'https://www.pesuacademy.com/Academy/'

# Functions

def init():
    """Initial function run to setup the environment file"""
    global SLEEP_TIME
    global MY_USER
    global MY_PWD
    global SEMESTER
    global BROWSER_TYPE

    if (CURRENT_DIRECTORY / '.env').exists():
        load_dotenv()
        print('Reading from the environment file')
        SLEEP_TIME = int(os.getenv('SLEEP_TIME'))
        MY_USER = os.getenv('MY_USER')
        MY_PWD = os.getenv('MY_PWD')
        SEMESTER = os.getenv('SEMESTER')
        BROWSER_TYPE = os.getenv('BROWSER_TYPE')
    else:
        print('Environment file doesn\'t exist\nEnter the details')
        SLEEP_TIME = int(input('Enter the sleep time (1 or 0 for fast internet. 3 onwards for slow internet): '))
        MY_USER = input('USN or SRN: ')
        MY_PWD = getpass.getpass('Password: ')
        SEMESTER = input('Semester [1:8]: ')
        BROWSER_TYPE = input('Browser (msedge, chrome, firefox): ')
        with open('.env', 'w', encoding=FORMAT) as f:
            f.write(f'SLEEP_TIME={SLEEP_TIME}\n')
            f.write(f'MY_USER={MY_USER}\n')
            f.write(f'MY_PWD={MY_PWD}\n')
            f.write(f'SEMESTER=Sem-{SEMESTER}\n')
            f.write(f'BROWSER_TYPE={BROWSER_TYPE}\n')


def init_website():
    """Initalize the website for selenium"""

    global browser
    if(BROWSER_TYPE == "chrome"):
        browser = webdriver.Chrome(ChromeDriverManager().install())
    elif(BROWSER_TYPE == "msedge"):
        browser = webdriver.Edge(EdgeChromiumDriverManager().install())
    elif(BROWSER_TYPE == "firefox"):
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        browser = webdriver.Chrome(ChromeDriverManager().install())
    
    browser.maximize_window()
    browser.get(PESU_URL)

def login():
    time.sleep(SLEEP_TIME)
    username = browser.find_element_by_css_selector("#j_scriptusername")
    password = browser.find_element_by_css_selector("body > div.login-body > div:nth-child(1) > div > div.login-form > form > fieldset > div:nth-child(3) > input")
    btn = browser.find_element_by_css_selector("#postloginform\#\/Academy\/j_spring_security_check")
    username.send_keys(MY_USER)
    password.send_keys(MY_PWD)
    btn.click()

def go_to_courses():
    time.sleep(SLEEP_TIME)
    courses = browser.find_element_by_css_selector("#menuTab_653 > a > span.menu-name")
    courses.click()

def write_topics_to_file():
    topics_file = CURRENT_DIRECTORY / 'topics.txt'
    if not topics_file.exists():
        print("Empty!")
        time.sleep(SLEEP_TIME)
        sem = browser.find_element_by_css_selector("#semesters")
        sem = sem.find_elements_by_tag_name("option")
        for semnum, semester in enumerate(sem,1):
            select = Select(browser.find_element_by_id("semesters"))
            select.select_by_visible_text(semester.text)
            time.sleep(1)
            table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
            table.text
            sub = table.find_elements_by_tag_name("tr")
            print(str(semnum) + ' : ' + semester.text + "\n")
            # topics.write("\n" + str(semnum) + ' : ' + semester.text + "\n")
            for subnum,subject in enumerate(sub,0):
                if(subject.text == "Course Code Course Title Course Type Status"):
                    pass
                else:
                    print(str(subnum)+' : '+subject.text + "\n")
                    # topics.write(str(subnum)+' : '+subject.text + "\n")
    else:
        topics_file.touch()

def choose_sem(SEMESTER):
    time.sleep(SLEEP_TIME + 1)
    select = Select(browser.find_element_by_id("semesters"))
    select.select_by_visible_text(SEMESTER)

def go_to_subject(n):
    time.sleep(SLEEP_TIME + 1)
    table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
    sub = table.find_elements_by_tag_name("tr")
    inner = sub[n].find_elements_by_tag_name("td")
    # topics.write(inner[1].text + "\n\n")
    print(inner[1].text)
    sub[n].click()

def go_to_unit(i):
    time.sleep(SLEEP_TIME + 2)
    unit_list = browser.find_element_by_css_selector("#courselistunit")
    units = unit_list.find_elements_by_tag_name("li")
    # topics.write("UNIT "+ str(i+1) + "\n\n")
    print("UNIT ", i + 1)
    units[i].click()

def get_vid_links(links, i, j):
        res = requests.get(links[0])
        soup = bs(res.content, 'lxml')
        script = soup.find_all('script')
        script_req = script[2].contents[0]

        text = re.search("(config.*?;)", script_req)
        obj = json.loads(str(script_req)[text.span()[0] + 8 : text.span()[1] - 1])
        with open(f'links_{i}_{j}.json', 'w', encoding=FORMAT) as f:
            json.dump(obj, f, indent=4)

def check_vid(i, j):
    try:
        time.sleep(SLEEP_TIME + 1)
        vid_icon = browser.find_element_by_class_name("pesu-icon-play-button")
        vid_icon.click()
        time.sleep(SLEEP_TIME + 1)
        wrapper = browser.find_element_by_tag_name("body")
        videlement = wrapper.find_elements_by_id("embedVideoSrc")
            
        link = [x.get_attribute("src") for x in videlement] # videlement.get_attribute("src")
        # [topics.write(x+"\n") for x in link]
        get_vid_links(link, i, j)

        wrapper = browser.find_element_by_tag_name("body")
        backlink = wrapper.find_element_by_css_selector("#StudentProfilePESUContent > div.cmc_breadcrum > a.muted_link")
        
        browser.execute_script("window.scrollTo(0, 0);")
        backlink.click()
            
    except Exception as e:
        # topics.write("None\n")
        print(e)

def main():
    init()
    init_website()
    login()
    go_to_courses()
    # write_topics_to_file() #for future use
    choose_sem(SEMESTER)

    # GET EVERY AV SUMMARY ON PESUACADEMY
    for subj in range(4,6):
        time.sleep(SLEEP_TIME)
        go_to_subject(subj)

        # within subject
        time.sleep(SLEEP_TIME)
        unit_list = browser.find_element_by_css_selector("#courselistunit")
        units = unit_list.find_elements_by_tag_name("li")

        for i in range(5):
            go_to_unit(i)
            time.sleep(SLEEP_TIME)
            content_list = browser.find_element_by_css_selector("#CourseContentId > div > div.table-responsive > table")
            contents = content_list.find_elements_by_tag_name("tr")
            
            for j in range(1, len(contents)):
                time.sleep(SLEEP_TIME)
                unit_list = browser.find_element_by_css_selector("#courselistunit")
                units = unit_list.find_elements_by_tag_name("li")
                units[i].click()
                time.sleep(SLEEP_TIME + 1)
                content_list = browser.find_element_by_css_selector("#CourseContentId > div > div.table-responsive > table")
                contents = content_list.find_elements_by_tag_name("tr")
                row = contents[j]
                # topics.write(str(j)+ " : ")
                print(j)
                row_contents = row.find_elements_by_tag_name("td")
                # topics.write(row_contents[0].text+"\n")
                print(row_contents[0].text)
                av_summary = row_contents[1]
                check_vid(i, j)
        
        wrapper = browser.find_element_by_tag_name("body")
        course_link = wrapper.find_element_by_css_selector("#StudentProfilePESUContent > div.cmc_breadcrum > a")
        browser.execute_script("window.scrollTo(0, 0);")
        course_link.click()

if __name__ == '__main__':
    main()
