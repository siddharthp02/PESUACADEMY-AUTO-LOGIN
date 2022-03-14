

from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

topics = open("topics.txt","a+")

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


browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.pesuacademy.com/Academy/")
username = browser.find_element_by_css_selector("#j_scriptusername")
password = browser.find_element_by_css_selector("body > div.login-body > div:nth-child(1) > div > div.login-form > form > fieldset > div:nth-child(3) > input")
btn = browser.find_element_by_css_selector("#postloginform\#\/Academy\/j_spring_security_check")
myuser = "PES1202000449"
mypwd = "siddhu2002"
username.send_keys(myuser)
password.send_keys(mypwd)
btn.click()


time.sleep(1)
courses = browser.find_element_by_css_selector("#menuTab_653 > a > span.menu-name")
courses.click()

if(is_file_empty("topics.txt")):
    print("Empty!")
    time.sleep(1)
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

        

        
        




sem = browser.find_element_by_css_selector("#semesters")
sem = sem.find_elements_by_tag_name("option")

if(sem[0].text != 'Sem-4'):
    select = Select(browser.find_element_by_id("semesters"))
    select.select_by_visible_text('Sem-4')


# time.sleep(2)

#table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
# table.text
#sub = table.find_elements_by_tag_name("tr")
#sub[1].click()
#python -m PyInstaller file.py

topics.close()