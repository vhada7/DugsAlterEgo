from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random

COMMENTS = list(map(lambda x: x.strip(), open("comments_raw.txt").readlines()))

def get_credentials():
    return list(map(lambda x: x.strip(), open("credentials.txt").readlines()))


def typing(s, element):
    typing_speed = random.randint(10,20)
    time_to_take = len(s)/typing_speed 
    for ch in s:
        sleep_time = random.uniform(0, time_to_take)
        time.sleep(sleep_time)
        element.send_keys(ch)
        time_to_take -= sleep_time

def parent(element):
    return element.find_element(By.XPATH, "..")

def comment(comment_section):
    textarea = comment_section.find_element(By.TAG_NAME, "textarea")
    textarea.click()
    # find the text area again
    textarea = comment_section.find_element(By.TAG_NAME, "textarea")
    typing(random.choice(COMMENTS), textarea)
    time.sleep(0.25)
    textarea.send_keys(Keys.ENTER)
    time.sleep(3)


def comment_recent_posts(driver):
    comment_buttons = WebDriverWait(driver, 3).until(lambda x: x.find_elements(By.XPATH, '//textarea[contains(@aria-label, "Add a comment")]')) 
    comment_sections = list(map(lambda x: parent(parent(parent(parent(parent(parent(x)))))), comment_buttons))
    print("Commenting on {} posts...".format(len(comment_sections)))
    i = 0
    for comment_button in comment_sections:
        # check if we have already commented
        if "keepyourdamnpotato" not in str(comment_button.text):
            comment(comment_button)
        else:
            print("Skipping\n\n{}\n\nAlready commented...\n".format(comment_button.text))
        i+=1

def click(driver, element):
    driver.execute_script("arguments[0].click();", element)

# need to find a way to comment on posts we haven't commented on

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://instagram.com")
    a = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.TAG_NAME , "input"))

    USERNAME = get_credentials()[0]
    typing(get_credentials()[0], a[0])
    typing(get_credentials()[1], a[1])

    buttons = driver.find_elements(By.TAG_NAME , "button")
    click(driver, buttons[1])
    # find "Not now" button
    not_now_button1 = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//div[text()="Not now"]')) 
    not_now_button1.click()
    # same thing for popup 
    not_now_button2 = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//button[text()="Not Now"]')) 
    not_now_button2.click()
    try:
        view_older_posts = WebDriverWait(driver, 3).until(lambda x: x.find_element(By.XPATH, '//span[contains(text(), "View older posts")]'))
    # press view older posts if it can be seen
        view_older_posts.click()
        time.sleep(5)
    except:
        None

    comment_recent_posts(driver) 
    time.sleep(5)
    driver.close()
