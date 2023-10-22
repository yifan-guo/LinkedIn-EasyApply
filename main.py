from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json
import os

from selenium.webdriver.chrome.options import Options


class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""

        print("data: {}".format(data))
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.phone_number = data['phone_number']
        self.resume_path = data['resume_path']
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=yifan")
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(options=chrome_options)

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
    
    def job_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""

        # go to Jobs
        # jobs_link = self.driver.find_element(By.LINK_TEXT, 'Jobs')
        # jobs_link.click()
        self.driver.get("https://www.linkedin.com/jobs/search")

        time.sleep(5)

        # search_keywords = self.driver.find_element(By.CSS_SELECTOR, "jobs-search-box__text-input[aria-label='Search by title, skill, or company']")
        # search_keywords.clear()
        # search_keywords.send_keys(self.keywords)
        # search_keywords.send_keys(Keys.RETURN)

        # time.sleep(5)

        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='Search by title, skill, or company']")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_keywords.send_keys(Keys.RETURN)
        search_location = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='City, state, or zip code']")
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        """This function filters all the job results by 'Easy Apply'"""

        # select all filters, click on Easy Apply and apply the filter
        # all_filters_button = self.driver.find_element(By.XPATH, "//button[@data-control-name='all_filters']")
        # all_filters_button.click()
        # time.sleep(1)
        # easy_apply_button = self.driver.find_element(By.XPATH, "//label[@for='f_LF-f_AL']")
        # easy_apply_button.click()
        # time.sleep(1)
        # apply_filter_button = self.driver.find_element(By.XPATH, "//button[@data-control-name='all_filters_apply']")
        # apply_filter_button.click()
        # easy_apply_button = self.driver.find_element(By.XPATH, "//button[normalize-space()='Easy Apply']").click()
        # easy_apply_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Easy Apply filter.']")
        all_filters_button =  WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'artdeco-pill artdeco-pill--slate artdeco-pill--2 artdeco-pill--choice ember-view search-reusables__filter-pill-button')]")))
        all_filters_button.click()
        time.sleep(1)

    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        # total_results = self.driver.find_element("display-flex.t-12.t-black--light.t-normal")
        total_results = self.driver.find_element(By.CSS_SELECTOR, ".display-flex.t-normal.t-12.t-black--light.jobs-search-results-list__text")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(total_results_int)

        # time.sleep(2)
        # get results for the first page
        current_page = self.driver.current_url
        # results = self.driver.find_elements(By.CLASS_NAME, "occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")
        results = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container.relative")

        # for each job add, submits application if no questions asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            # titles = result.find_elements(By.CLASS_NAME, 'job-card-search__title.artdeco-entity-lockup__title.ember-view')
            titles = result.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__title.ember-view')
            for title in titles:
                # self.submit_apply(title)
                pass

        # if there is more than one page, find the pages and apply to the results of each page
        page_state = self.driver.find_element(By.CLASS_NAME, "artdeco-pagination__page-state")
        page_state_text = page_state.get_attribute("innerHTML").strip()
        total_pages_int = int(page_state_text.split(' ')[-1])
        print("total_pages: {}".format(total_pages_int))
        current_page = 1
        while current_page < total_pages_int:
            current_page += 1
            time.sleep(2)

            # go to the next page
            get_next_page = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Page "+str(current_page)+"']")))
            get_next_page.click()
        
            # go through all available job offers on this page and apply
            results_ext = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container.relative")
            for result_ext in results_ext:
                hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                hover_ext.perform()
                # titles_ext = result_ext.find_elements(By.CLASS_NAME, 'job-card-search__title.artdeco-entity-lockup__title.ember-view')
                titles_ext = result_ext.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__title.ember-view')
                for title_ext in titles_ext:
                    self.submit_apply(title_ext)

        else:
            self.close_session()

    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""

        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(2)
        # already_applied = self.driver.find_element(By.XPATH, "//a[@href='/jobs/tracker/applied']")
        
        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
            
            
            # in_apply = self.driver.find_element(By.CLASS_NAME, "jobs-apply-button")
            # time.sleep(20)
            wait = WebDriverWait(self.driver, 10, ignored_exceptions=[StaleElementReferenceException])
            # in_apply = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")))
            # in_apply = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")))
            print("got jobs apply element")
            in_apply.click()
        except NoSuchElementException:
            print('Could not find EasyApply button. You already applied to this job, go to next...')
            return
        except StaleElementReferenceException:
            print('retry getting stale element')
            time.sleep(20)
            in_apply = self.driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
            in_apply.click()

        
        # try to enter phone number if present
        try:
            # phone_number = self.driver.find_element(By.CSS_SELECTOR, ".artdeco-text-input--input[id?='phoneNumber-nationalNumber']")
            # phone_number = self.driver.find_element(By.XPATH, "//input[ends-with(@id, 'phoneNumber-nationalNumber')]") # The string '//input[ends-with(@id, 'phoneNumber-nationalNumber')]' is not a valid XPath expression.
            phone_number = self.driver.find_element(By.XPATH, "//input[contains(@id, 'phoneNumber')]")

            phone_number.send_keys(self.phone_number)
            # phone_number.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print('Could not find phone number field, skipping...')

        time.sleep(5)

        # try to upload resume if present
        try:
            upload_resume = self.driver.find_element(By.CLASS_NAME, "jobs-document-upload__upload-button.artdeco-button.artdeco-button--secondary.artdeco-button--2.mt2")
            upload_resume.click()
            wait = WebDriverWait(self.driver, 5)
            time.sleep(3)
            upload_resume.send_keys(os.getcwd() + "/{}".format(self.resume_path))
            time.sleep(3)
            upload_resume.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print('Could not find upload resume button, skipping...')

        time.sleep(5)
        # try to submit if submit application is available...
        try:
            # submit = self.driver.find_element(By.XPATH, "//button[@data-control-name='submit_unify']")
            submit = self.driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
            print("found submit application button")
            time.sleep(10)
            submit.send_keys(Keys.RETURN)
            done_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Done']]")))
            self.driver.find_element(By.XPATH, "")
            done_button.click()
        
        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                # discard = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                # wait = WebDriverWait(self.driver, 5)
                # discard = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-modal-close-btn]")))
                # discard_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-dialog-secondary-btn]")))
                # discard.send_keys(Keys.RETURN)
                # time.sleep(1)
                # discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-test-dialog-primary-btn]")
                # discard_confirm.send_keys(Keys.RETURN)
                time.sleep(5)
                discard = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
                time.sleep(1)
                confirm_discard = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']").click()
            except TimeoutException:
                print('Could not find the close button, skipping...')

        time.sleep(1)

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        # self.login_linkedin()
        self.job_search()
        time.sleep(2)
        self.filter()
        time.sleep(10)
        self.find_offers()
        time.sleep(2)
        self.close_session()


if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()