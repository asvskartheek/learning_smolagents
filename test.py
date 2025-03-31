from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from helium import *
import time

import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
chrome_profile = "/Users/asvs/Library/Application Support/Google/Chrome"
options.add_argument(f"--user-data-dir={chrome_profile}")
options.add_argument("--profile-directory=Default")

driver = uc.Chrome(options=options)
set_driver(driver)

go_to("https://linkedin.com")

# Print the entire HTML of the page
print(driver.page_source)
