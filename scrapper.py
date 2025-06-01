from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

# get the id of the place
ID = input()
url = f"https://www.google.com/maps/place/data={ID}"

# chrome options to not load images, makes the script more efficient
chrome_options = ChromeOptions()
prefs = {
    "profile.managed_default_content_settings.images": 2  # 2 means do not load images
}
chrome_options.add_experimental_option("prefs", prefs)

driver = Chrome(options=chrome_options)

# get the page
driver.get(url)
input("Proceed with scrapping?")

# switch to review tab
review_tab = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Reviews']")
review_tab.click()
sleep(0.1)

# locate the wrapper
scrollable = driver.find_element(By.CSS_SELECTOR, "div[role='main'] > div[tabindex='-1']")
last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable)

# start scrolling
while True:
    driver.execute_script("arguments[0].scrollBy(0, 10000)", scrollable)
    sleep(3)
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable)
    if new_height == last_height:
        break
    last_height = new_height

# write the page source to a file, to be read by extract.py
page_source = driver.page_source
with open("test.html", "w", encoding="utf-8") as file:
    file.write(page_source)

driver.close()