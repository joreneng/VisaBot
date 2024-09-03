from telnetlib import EC

import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time

def send_telegram_message(chat_id, message, bot_token):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(send_text)
    return response.json()

def available_appt():
    firstrow_xpath = '//*[@id="content"]/app-booking-search/app-proposal-table/div/table/tbody/tr[1]/td[1]'
    try:
        # Wait a maximum of 10 seconds until the page title contains 'Example'
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, firstrow_xpath)))
    except TimeoutException:
        print("Timed out waiting for first row to load")

    firstrow_element = driver.find_element(By.XPATH, firstrow_xpath)

    # Sample date string
    date_string = firstrow_element.text
    global date_part
    date_part = date_string.split(' ', 1)[1]

    return int(date_part.split('.', 2)[1]) <= 7

def book_appt():
    appt_xpath = '//*[@id="content"]/app-booking-search/app-proposal-table/div/table/tbody/tr[1]/td[1]'
    try:
        # Wait a maximum of 10 seconds until the page title contains 'Example'
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, appt_xpath))).click()
    except TimeoutException:
        print("Timed out waiting for first row to load")

    bookBtn_xpath = '// *[ @ id = "bookBtn"]'
    try:
        # Wait a maximum of 10 seconds until the page title contains 'Example'
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, bookBtn_xpath))).click()
    except TimeoutException:
        print("Timed out waiting for Confirm Appointment to load")

    # Get the text from the element
    text = "Appointment for " + date_part + " booked!"

    # Telegram chat details
    chat_id = 'chatID'  # Replace with your chat ID
    bot_token = 'botToken'  # Replace with your bot token

    # Send the extracted text to the Telegram chat
    response = send_telegram_message(chat_id, text, bot_token)

def get_to_booking_list():
   # Locate the token input field and submit button, then input the token and log in
    token = 'token' # Replace with token
    token_input_xpath = '//*[@id="accessToken"]'  # Replace with the actual XPath
    submit_button_xpath = '//*[@id="loginBtn"]'  # Replace with the actual XPath

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, token_input_xpath))).send_keys(token)
    except TimeoutException:
        print("Timed out waiting for token input to load")

    time.sleep(1)

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath))).click()
    except TimeoutException:
        print("Timed out waiting for Submit to load")


# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Replace 'login_url' with the URL of the login page
login_url = 'login_url'
driver.get(login_url)

listBtn_xPath = '//*[@id="bookingListBtn"]'
date_part = " "

try:
    # Wait a maximum of 10 seconds until the page title contains 'Example'
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, listBtn_xPath))).click()
except TimeoutException:
    print("Timed out waiting for Booking List button to load")

while not available_appt():
    driver.refresh()
    time.sleep(300)
    get_to_booking_list()

book_appt()
driver.quit()
