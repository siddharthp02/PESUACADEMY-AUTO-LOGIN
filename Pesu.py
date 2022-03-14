

from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

try:
    username= WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#j_scriptusername")) #This is a dummy element
    )
except:
    browser.quit()
    quit()
finally:
    password = browser.find_element_by_css_selector("body > div.login-body > div:nth-child(1) > div > div.login-form > form > fieldset > div:nth-child(3) > input")
    btn = browser.find_element_by_css_selector("#postloginform\#\/Academy\/j_spring_security_check")

btn = browser.find_element_by_css_selector("#postloginform\#\/Academy\/j_spring_security_check")
myuser = "PES1202000449"
mypwd = "siddhu2002"
username.send_keys(myuser)
password.send_keys(mypwd)
btn.click()

try:
    courses= WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#menuTab_653 > a > span.menu-name")) #This is a dummy element
)
except:
    browser.quit()
    quit()

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
select = Select(browser.find_element_by_id("semesters"))
select.select_by_visible_text('Sem-4')

    


# time.sleep(2)

#table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
# table.text
#sub = table.find_elements_by_tag_name("tr")
#sub[1].click()
#python -m PyInstaller file.py

topics.close()
# topics = open("topics.txt","a+")

# def is_file_empty(file_name):
#     """ Check if file is empty by reading first character in it"""
#     # open ile in read mode
#     with open(file_name, 'r') as read_obj:
#         # read first character
#         one_char = read_obj.read(1)
#         # if not fetched then file is empty
#         if not one_char:
#            return True
#     return False


# browser = webdriver.Chrome()
# browser.maximize_window()
# browser.get("https://www.pesuacademy.com/Academy/")
# try:
#     username= WebDriverWait(browser, 30).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "#j_scriptusername")) #This is a dummy element
# )
# except:
#     browser.quit()
# finally:
#     password = browser.find_element_by_css_selector("body > div.login-body > div:nth-child(1) > div > div.login-form > form > fieldset > div:nth-child(3) > input")
#     btn = browser.find_element_by_css_selector("#postloginform\#\/Academy\/j_spring_security_check")



# myuser = "PES1202000449"
# mypwd = "siddhu2002"
# username.send_keys(myuser)
# password.send_keys(mypwd)
# btn.click()

# try:
#     courses= WebDriverWait(browser, 30).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "#menuTab_653 > a > span.menu-name")) #This is a dummy element
# )
# except:
#     browser.quit()

# courses.click()

# if(is_file_empty("topics.txt")):
#     print("Empty!")
#     try:
#         sem = WebDriverWait(browser, 30).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#semesters")) #This is a dummy element
# )
#     except:
#         browser.quit()
        
    
    

#     sem = sem.find_elements_by_tag_name("option")
#     for semnum,semester in enumerate(sem,1):
#         select = Select(browser.find_element_by_id("semesters"))
#         select.select_by_visible_text(semester.text)
              
#         table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
#         table.text
#         sub = table.find_elements_by_tag_name("tr")
#         print(str(semnum)+' : ' + semester.text + "\n")
#         topics.write("\n"+str(semnum)+' : '+semester.text + "\n")
#         for subnum,subject in enumerate(sub,0):
#             if(subject.text == "Course Code Course Title Course Type Status"):
#                 pass
#             else:
#                 print(str(subnum)+' : '+subject.text + "\n")
#                 topics.write(str(subnum)+' : '+subject.text + "\n")

        

        
        




# sem = browser.find_element_by_css_selector("#semesters")
# sem = sem.find_elements_by_tag_name("option")

# if(sem[0].text != 'Sem-4'):
#     select = Select(browser.find_element_by_id("semesters"))
#     select.select_by_visible_text('Sem-4')


# # time.sleep(2)

# #table = browser.find_element_by_css_selector("#getStudentSubjectsBasedOnSemesters > div > div > table")
# # table.text
# #sub = table.find_elements_by_tag_name("tr")
# #sub[1].click()
# #python -m PyInstaller file.py

# topics.close()