import subprocess

subprocess.call(['pip', 'install', 'selenium'])

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

AMIZONE_LINK = "https://s.amizone.net/"

with open('data.txt', "r") as file:
    lines = file.read().split("\n")
    USERNAME = lines[0]
    PASSWORD = lines[1]
    GRADE = lines[2]
    MESSAGE = lines[3]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()

driver.get(AMIZONE_LINK)

UsernameInput = driver.find_element(By.XPATH, '//*[@id="loginform"]/div[1]/input[1]')
PasswordInput = driver.find_element(By.XPATH, '//*[@id="loginform"]/div[2]/input')

UsernameInput.send_keys(USERNAME)
PasswordInput.send_keys(PASSWORD)

LoginBtn = driver.find_element(By.XPATH, '//*[@id="loginform"]/div[4]/button')
LoginBtn.click()

popups = driver.find_elements(By.CLASS_NAME, "close")

for close_btn in popups[::-1]:
    try:
        close_btn.click()
    except:
        pass
    else:
        time.sleep(0.25)

FacultyBtn = driver.find_element(By.XPATH, '//*[@id="M27"]/span')
FacultyBtn.click()
time.sleep(2)

FacultyList = driver.find_elements(By.XPATH, '//*[@id="Div_Partial"]/div/div/div[2]/div[2]/div/ul/li')

i=0

while i<len(FacultyList):
    try:
        Btn = driver.find_element(By.XPATH, f'//*[@id="Div_Partial"]/div/div/div[2]/div[2]/div/ul/li[{i+1}]/div[3]/div[1]')
        Btn.click()
    except:
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        Btn = driver.find_element(By.XPATH, f'//*[@id="Div_Partial"]/div/div/div[2]/div[2]/div/ul/li[{i+1}]/div[3]/div[1]')
        Btn.click()

    try:
        FeedbackBtn = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, "Feedback")))
        actions = ActionChains(driver)
        actions.move_to_element(FeedbackBtn).perform()
        FeedbackBtn.click()
        time.sleep(2)
    except:
        i += 1
        continue
    
    Rating_Buttons = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, f'//input[@value="{GRADE}"]/following-sibling::span[@class="lbl"]')))
    driver.execute_script("window.scrollTo(0, 0);")

    for button in Rating_Buttons:
        button.click()

    for j in range(1, 4):
        driver.find_element(By.XPATH, f'//input[@id="rdbQuestion{j}"][@value="1"]/following-sibling::span[@class="lbl"]').click()

    TextBox = driver.find_element(By.XPATH, '//*[@id="FeedbackRating_Comments"]')
    TextBox.send_keys(MESSAGE)

    SubmitBtn = driver.find_element(By.XPATH, '//*[@id="btnSubmit"]')
    SubmitBtn.click()

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 0);")
    i = 0   

driver.quit()
print("All Forms Filled.")