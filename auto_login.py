from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

#Set Variables Here
sleep_time = 1  #set sleep time (1 or 0 for fast internet. 3 onwards for slow internet)
myuser = ""     #Set username here
mypwd = ""      #Set password here
semester = ''   #Choose semester eg: 'Sem-1' or 'Sem-2' or 'Sem-3' or 'Sem-4' 
browser_type = "" # "msedge" or "chrome"  or "firefox"
#Open file
topics = open("topics.txt","a+")

#Functions

def is_file_empty(file_name):
    """ Check if file is empty by reading first character in it"""
    # open ile in read mode
    with open(file_name, 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
           return True
    return False

def init_website():
    global browser
    if(browser_type == "chrome"):
        browser = webdriver.Chrome(ChromeDriverManager().install())
    elif(browser_type == "msedge"):
        browser = webdriver.Edge(EdgeChromiumDriverManager().install())
    elif(browser_type == "firefox"):
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        browser = webdriver.Chrome(ChromeDriverManager().install())
    
    browser.maximize_window()
    browser.get("https://www.pesuacademy.com/Academy/")

def login():
    # time.sleep(sleep_time)
    username = browser.find_element_by_css_selector("#j_scriptusername")
    password = browser.find_element_by_css_selector("body > div.login-body > div:nth-child(1) > div > div.login-form > form > fieldset > div:nth-child(3) > input")
    btn = browser.find_element_by_css_selector("#postloginform\#\/Academy\/j_spring_security_check")
    username.send_keys(myuser)
    password.send_keys(mypwd)
    btn.click()

def go_to_courses():
    time.sleep(sleep_time)
    courses = browser.find_element_by_css_selector("#menuTab_653 > a > span.menu-name")
    courses.click()

def write_topics_to_file():
    if(is_file_empty("topics.txt")):
        print("Empty!")
        time.sleep(sleep_time)
        sem = browser.find_element_by_css_selector("#semesters")
        sem = sem.find_elements_by_tag_name("option")
        for semnum,semester in enumerate(sem,1):
            select = Select(browser.find_element_by_id("semesters"))
            select.select_by_visible_text(semester.text)
            time.sleep(1)
            table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
            table.text
            sub = table.find_elements_by_tag_name("tr")
            print(str(semnum)+' : ' + semester.text + "\n")
            topics.write("\n"+str(semnum)+' : '+semester.text + "\n")
            for subnum,subject in enumerate(sub,0):
                if(subject.text == "Course Code Course Title Course Type Status"):
                    pass
                else:
                    print(str(subnum)+' : '+subject.text + "\n")
                    topics.write(str(subnum)+' : '+subject.text + "\n")
    else:
        pass

def choose_sem(semester):
    time.sleep(sleep_time+1)
    select = Select(browser.find_element_by_id("semesters"))
    select.select_by_visible_text(semester)


#Main
init_website()
login()
go_to_courses()
# write_topics_to_file() #for future use
choose_sem(semester)

#Close file
topics.close()
