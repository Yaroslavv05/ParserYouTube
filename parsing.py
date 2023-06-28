import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import undetected_chromedriver as webdriver
from config import accounts, channel_links
from selenium_recaptcha_solver import RecaptchaSolver
from selenium_recaptcha_solver.exceptions import RecaptchaException


class YouTube:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self, email, password):
        self.driver.get('https://www.youtube.com/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//a[@class='yt-spec-button-shape-next yt-spec-button-shape-next--outline yt-spec-button-shape-next--call-to-action yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading ']").click()
        time.sleep(2)

        email_field = self.driver.find_element(By.XPATH, "//input[@class='whsOnd zHQkBf']")
        email_field.send_keys(email)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']").click()
        time.sleep(2)

        password_field = self.driver.find_element(By.XPATH, "//input[@class='whsOnd zHQkBf']")
        password_field.send_keys(password)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']").click()
        time.sleep(5)

    def get_email(self, channel_link):
        self.driver.get(channel_link)
        time.sleep(2)

        try:
            email_button = self.driver.find_element(By.XPATH, "//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--align-by-text ']")
            email_button.click()
            time.sleep(2)

            solver = RecaptchaSolver(driver=self.driver)
            recaptcha_iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)

            email = self.driver.find_element(By.XPATH, "//a[@id='email']")
            print(email.text)
            time.sleep(2)

            self.driver.back()
            time.sleep(2)
        except (NoSuchElementException, RecaptchaException, Exception):
            print("Email not found on this channel.")

    def run(self):
        for acc_name, acc_data in accounts.items():
            email = acc_data['email']
            password = acc_data['pass']
            self.login(email, password)
            for channel_link in channel_links:
                self.get_email(channel_link)
            self.driver.quit()


Y = YouTube()
Y.run()
