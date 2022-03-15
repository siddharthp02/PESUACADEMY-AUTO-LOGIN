from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#Set Variables Here
sleep_time = 2  #set sleep time (1 or 0 for fast internet. 3 onwards for slow internet)
myuser = "PES1202000449"     #Set username here
mypwd = "Siddhu2002"      #Set password here
semester = 'Sem-4'   #Choose semester eg: 'Sem-1' or 'Sem-2' or 'Sem-3' or 'Sem-4' 
browser_type = "msedge" # "msedge" or "chrome"  or "firefox"
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

def go_to_subject(n):
    time.sleep(sleep_time+1)
    table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
    sub = table.find_elements_by_tag_name("tr")
    inner = sub[n].find_elements_by_tag_name("td")
    topics.write(inner[1].text+"\n\n")
    print(inner[1].text)
    sub[n].click()


def go_to_unit():
    time.sleep(sleep_time+2)
    unit_list = browser.find_element_by_css_selector("#courselistunit")
    units = unit_list.find_elements_by_tag_name("li")
    topics.write("UNIT "+ str(i+1) + "\n\n")
    print("UNIT ",i+1)
    units[i].click()


def check_vid():
    try:
        time.sleep(sleep_time+1)
        vid_icon = av_summary.find_element_by_class_name("pesu-icon-play-button")
        vid_icon.click()
        time.sleep(sleep_time+1)
        wrapper = browser.find_element_by_tag_name("body")
        videlement = wrapper.find_elements_by_id("embedVideoSrc")
            
        link = [x.get_attribute("src") for x in videlement]#videlement.get_attribute("src")
        [topics.write(x+"\n") for x in link]
            
        wrapper = browser.find_element_by_tag_name("body")
        backlink = wrapper.find_element_by_css_selector("#StudentProfilePESUContent > div.cmc_breadcrum > a.muted_link")
            
            
        browser.execute_script("window.scrollTo(0, 0);")
        backlink.click()
            
    except Exception as e:
        topics.write("None\n")
#Main
init_website()
login()
go_to_courses()
#write_topics_to_file() #for future use
choose_sem(semester)

# GET EVERY AV SUMMARY ON PESUACADEMY
# for subj in range(4,6):
#     time.sleep(sleep_time)
#     go_to_subject(subj)
#     #within subject
#     time.sleep(sleep_time)
#     unit_list = browser.find_element_by_css_selector("#courselistunit")
#     units = unit_list.find_elements_by_tag_name("li")
#     #for loop
#     for i in range(5):
#         go_to_unit()

#     #next for loop
#         time.sleep(sleep_time)
#         content_list = browser.find_element_by_css_selector("#CourseContentId > div > div.table-responsive > table")
#         contents = content_list.find_elements_by_tag_name("tr")
        
#         for j in range(1,len(contents)):
#             time.sleep(sleep_time)
#             unit_list = browser.find_element_by_css_selector("#courselistunit")
#             units = unit_list.find_elements_by_tag_name("li")
#             units[i].click()
#             time.sleep(sleep_time+1)
#             content_list = browser.find_element_by_css_selector("#CourseContentId > div > div.table-responsive > table")
#             contents = content_list.find_elements_by_tag_name("tr")
#             row = contents[j]
#             topics.write(str(j)+ " : ")
#             print(j)
#             row_contents = row.find_elements_by_tag_name("td")
#             topics.write(row_contents[0].text+"\n")
#             print(row_contents[0].text)
#             av_summary = row_contents[1]
#             check_vid()
    
#     wrapper = browser.find_element_by_tag_name("body")
#     course_link = wrapper.find_element_by_css_selector("#StudentProfilePESUContent > div.cmc_breadcrum > a")
#     browser.execute_script("window.scrollTo(0, 0);")
#     course_link.click()


#Close file
topics.close()
