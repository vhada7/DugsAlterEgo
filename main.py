from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random

COMMENTS = list(map(lambda x: x.strip(), open("comments_raw.txt").readlines()))
POSTS_TO_COMMENT_ON = 10

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


def comment_on_x_posts(driver, x):
    commented = 0
    commented_set = set()
    scroll_height = 0
    # scroll until we find enough posts
    while commented < x:
        # find comment buttons
        tmp = WebDriverWait(driver, 3).until(lambda x: x.find_elements(By.XPATH, '//textarea[contains(@aria-label, "Add a comment")]')) 
        comment_sections = list(map(lambda x: parent(parent(parent(parent(parent(parent(x)))))), tmp))
        print(list(map(lambda x: x.text, comment_sections)), sep = "\n\n\n")
        # comment on first one (if we haven't already and keep scrolling)
        if get_credentials()[0] not in str(comment_sections[0].text) and comment_sections[0] not in commented_set and "jules" not in comment_sections[0].text:
           comment(comment_sections[0])
           commented_set.add(comment_sections[0])
           commented+=1
           print("Commented on {} posts; {} to go...".format(commented, POSTS_TO_COMMENT_ON - commented))
        else:
           print("Skipping\n\n{}\n\nAlready commented...\n".format(comment_sections[0].text))
            
        # scroll
        scroll_height+=250
        driver.execute_script("window.scrollTo(0, {});".format(scroll_height))

def click(driver, element):
    driver.execute_script("arguments[0].click();", element)

# don't comment on sponsored posts

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

    posts = comment_on_x_posts(driver, POSTS_TO_COMMENT_ON)
    time.sleep(5)
    driver.close()
