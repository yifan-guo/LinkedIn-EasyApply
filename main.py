from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

import json
import os

import time, random, csv, traceback


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
                self.apply_to_job(title)
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

        self.my_send_resume()

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

    def apply_to_job(self, job_add):
            print('You are applying to the position of: ', job_add.text)
            job_add.click()
            time.sleep(2)
            
            easy_apply_button = None

            try:
                easy_apply_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
            except:
                return False

            # try:
            #     job_description_area = self.driver.find_element(By.CLASS_NAME, "jobs-search__job-details--container")
            #     self.scroll_slow(job_description_area, end=1600)
            #     self.scroll_slow(job_description_area, end=1600, step=400, reverse=True)
            # except:
            #     pass

            print("Applying to the job....")
            easy_apply_button.click()

            button_text = ""
            submit_application_text = 'submit application'
            while submit_application_text not in button_text.lower():
                retries = 3
                while retries > 0:
                    try:
                        self.fill_up()
                        next_button = self.driver.find_element(By.CLASS_NAME, "artdeco-button--primary")
                        button_text = next_button.text.lower()
                        if submit_application_text in button_text:
                            try:
                                self.unfollow()
                            except:
                                print("Failed to unfollow company!")
                        time.sleep(random.uniform(1.5, 2.5))
                        next_button.click()
                        time.sleep(random.uniform(3.0, 5.0))

                        if 'please enter a valid answer' in self.driver.page_source.lower() or 'file is required' in self.driver.page_source.lower():
                            retries -= 1
                            print("Retrying application, attempts left: " + str(retries))
                        else:
                            break
                    except:
                        traceback.print_exc()
                        raise Exception("Failed to apply to job!")
                if retries == 0:
                    traceback.print_exc()
                    self.driver.find_element(By.CLASS_NAME, 'artdeco-modal__dismiss').click()
                    time.sleep(random.uniform(3, 5))
                    self.driver.find_elements(By.CLASS_NAME, 'artdeco-modal__confirm-dialog-btn')[1].click()
                    time.sleep(random.uniform(3, 5))
                    raise Exception("Failed to apply to job!")

            closed_notification = False
            time.sleep(random.uniform(3, 5))
            try:
                self.driver.find_element(By.CLASS_NAME, 'artdeco-modal__dismiss').click()
                closed_notification = True
            except:
                pass
            try:
                self.driver.find_element(By.CLASS_NAME, 'artdeco-toast-item__dismiss').click()
                closed_notification = True
            except:
                pass
            time.sleep(random.uniform(3, 5))

            if closed_notification is False:
                raise Exception("Could not close the applied confirmation window!")

            return True

    def home_address(self, element):
        print('in home address')
        try:
            groups = element.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
            if len(groups) > 0:
                for group in groups:
                    lb = group.find_element(By.TAG_NAME, 'label').text.lower()
                    input_field = group.find_element(By.TAG_NAME, 'input')
                    if 'street' in lb:
                        self.enter_text(input_field, self.personal_info['Street address'])
                    elif 'city' in lb:
                        self.enter_text(input_field, self.personal_info['City'])
                        time.sleep(3)
                        input_field.send_keys(Keys.DOWN)
                        input_field.send_keys(Keys.RETURN)
                    elif 'zip' in lb or 'postal' in lb:
                        self.enter_text(input_field, self.personal_info['Zip'])
                    elif 'state' in lb or 'province' in lb:
                        self.enter_text(input_field, self.personal_info['State'])
                    else:
                        pass
        except:
            pass

    def get_answer(self, question):
        if self.checkboxes[question]:
            return 'yes'
        else:
            return 'no'

    def additional_questions(self):
        # pdb.set_trace()
        print('in additional_questions')
        frm_el = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
        if len(frm_el) > 0:
            for el in frm_el:
                # Radio check
                try:
                    radios = el.find_element(By.CLASS_NAME, 'jobs-easy-apply-form-element').find_elements(By.CLASS_NAME, 'fb-radio')

                    radio_text = el.text.lower()
                    radio_options = [text.text.lower() for text in radios]
                    answer = "yes"

                    if 'driver\'s licence' in radio_text or 'driver\'s license' in radio_text:
                        answer = self.get_answer('driversLicence')
                    elif 'gender' in radio_text or 'veteran' in radio_text or 'race' in radio_text or 'disability' in radio_text or 'latino' in radio_text:
                        answer = ""
                        for option in radio_options:
                            if 'prefer' in option.lower() or 'decline' in option.lower() or 'don\'t' in option.lower() or 'specified' in option.lower() or 'none' in option.lower():
                                answer = option

                        if answer == "":
                            answer = radio_options[len(radio_options) - 1]
                    elif 'north korea' in radio_text:
                        answer = 'no'
                    elif 'sponsor' in radio_text:
                        answer = self.get_answer('requireVisa')
                    elif 'authorized' in radio_text or 'authorised' in radio_text or 'legally' in radio_text:
                        answer = self.get_answer('legallyAuthorized')
                    elif 'urgent' in radio_text:
                        answer = self.get_answer('urgentFill')
                    elif 'commuting' in radio_text:
                        answer = self.get_answer('commute')
                    elif 'background check' in radio_text:
                        answer = self.get_answer('backgroundCheck')
                    elif 'level of education' in radio_text:
                        for degree in self.checkboxes['degreeCompleted']:
                            if degree.lower() in radio_text:
                                answer = "yes"
                                break
                    elif 'level of education' in radio_text:
                        for degree in self.checkboxes['degreeCompleted']:
                            if degree.lower() in radio_text:
                                answer = "yes"
                                break
                    elif 'data retention' in radio_text:
                        answer = 'no'
                    else:
                        answer = radio_options[len(radio_options) - 1]

                    i = 0
                    to_select = None
                    for radio in radios:
                        if answer in radio.text.lower():
                            to_select = radios[i]
                        i += 1

                    if to_select is None:
                        to_select = radios[len(radios)-1]

                    self.radio_select(to_select, answer, len(radios) > 2)

                    if radios != []:
                        continue
                except:
                    pass
                # Questions check
                try:
                    question = el.find_element(By.CLASS_NAME, 'jobs-easy-apply-form-element')
                    question_text = question.find_element(By.CLASS_NAME, 'fb-form-element-label').text.lower()

                    txt_field_visible = False
                    try:
                        txt_field = question.find_element(By.CLASS_NAME, 'fb-single-line-text__input')

                        txt_field_visible = True
                    except:
                        try:
                            txt_field = question.find_element(By.CLASS_NAME, 'fb-textarea')

                            txt_field_visible = True
                        except:
                            pass

                    if txt_field_visible != True:
                        txt_field = question.find_element(By.CLASS_NAME, 'multi-line-text__input')

                    text_field_type = txt_field.get_attribute('name').lower()
                    if 'numeric' in text_field_type:
                        text_field_type = 'numeric'
                    elif 'text' in text_field_type:
                        text_field_type = 'text'

                    to_enter = ''
                    if 'experience do you currently have' in question_text:
                        no_of_years = self.industry_default

                        for industry in self.industry:
                            if industry.lower() in question_text:
                                no_of_years = self.industry[industry]
                                break

                        to_enter = no_of_years
                    elif 'many years of work experience do you have using' in question_text:
                        no_of_years = self.technology_default

                        for technology in self.technology:
                            if technology.lower() in question_text:
                                no_of_years = self.technology[technology]

                        to_enter = no_of_years
                    elif 'grade point average' in question_text:
                        to_enter = self.university_gpa
                    elif 'first name' in question_text:
                        to_enter = self.personal_info['First Name']
                    elif 'last name' in question_text:
                        to_enter = self.personal_info['Last Name']
                    elif 'name' in question_text:
                        to_enter = self.personal_info['First Name'] + " " + self.personal_info['Last Name']
                    elif 'phone' in question_text:
                        to_enter = self.personal_info['Mobile Phone Number']
                    elif 'linkedin' in question_text:
                        to_enter = self.personal_info['Linkedin']
                    elif 'website' in question_text or 'github' in question_text or 'portfolio' in question_text:
                        to_enter = self.personal_info['Website']
                    else:
                        if text_field_type == 'numeric':
                            to_enter = 0
                        else:
                            to_enter = " ‏‏‎ "

                    if text_field_type == 'numeric':
                        if not isinstance(to_enter, (int, float)):
                            to_enter = 0
                    elif to_enter == '':
                        to_enter = " ‏‏‎ "

                    self.enter_text(txt_field, to_enter)
                    continue
                except:
                    pass
                # Date Check
                try:
                    date_picker = el.find_element(By.CLASS_NAME, 'artdeco-datepicker__input ')
                    date_picker.clear()
                    date_picker.send_keys(date.today().strftime("%m/%d/%y"))
                    time.sleep(3)
                    date_picker.send_keys(Keys.RETURN)
                    time.sleep(2)
                    continue
                except:
                    pass
                # Dropdown check
                try:
                    question = el.find_element(By.CLASS_NAME, 'jobs-easy-apply-form-element')
                    question_text = question.find_element(By.CLASS_NAME, 'fb-form-element-label').text.lower()

                    dropdown_field = question.find_element(By.CLASS_NAME, 'fb-dropdown__select')

                    select = Select(dropdown_field)

                    options = [options.text for options in select.options]

                    if 'proficiency' in question_text:
                        proficiency = "Conversational"

                        for language in self.languages:
                            if language.lower() in question_text:
                                proficiency = self.languages[language]
                                break

                        self.select_dropdown(dropdown_field, proficiency)
                    elif 'country code' in question_text:
                        self.select_dropdown(dropdown_field, self.personal_info['Phone Country Code'])
                    elif 'north korea' in question_text:

                        choice = ""

                        for option in options:
                            if 'no' in option.lower():
                                choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'sponsor' in question_text:
                        answer = self.get_answer('requireVisa')

                        choice = ""

                        for option in options:
                            if answer == 'yes':
                                choice = option
                            else:
                                if 'no' in option.lower():
                                    choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'authorized' in question_text or 'authorised' in question_text:
                        answer = self.get_answer('legallyAuthorized')

                        choice = ""

                        for option in options:
                            if answer == 'yes':
                                # find some common words
                                choice = option
                            else:
                                if 'no' in option.lower():
                                    choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'citizenship' in question_text:
                        answer = self.get_answer('legallyAuthorized')

                        choice = ""

                        for option in options:
                            if answer == 'yes':
                                if 'no' in option.lower():
                                    choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'gender' in question_text or 'veteran' in question_text or 'race' in question_text or 'disability' in question_text or 'latino' in question_text:

                        choice = ""

                        for option in options:
                            if 'prefer' in option.lower() or 'decline' in option.lower() or 'don\'t' in option.lower() or 'specified' in option.lower() or 'none' in option.lower():
                                choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    else:
                        choice = ""

                        for option in options:
                            if 'yes' in option.lower():
                                choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    continue
                except:
                    pass

                # Checkbox check for agreeing to terms and service
                try:
                    question = el.find_element(By.CLASS_NAME, 'jobs-easy-apply-form-element')

                    clickable_checkbox = question.find_element(By.TAG_NAME, 'label')

                    clickable_checkbox.click()
                except:
                    pass

    def unfollow(self):
        try:
            follow_checkbox = self.driver.find_element(By.XPATH, "//label[contains(.,\'to stay up to date with their page.\')]").click()
            follow_checkbox.click()
        except:
            pass

    def my_send_resume(self):
        print('in my_send_resume')
        # try to upload resume if present
        try:
            upload_resume = self.driver.find_element(By.CLASS_NAME, "jobs-document-upload__upload-button.artdeco-button.artdeco-button--secondary.artdeco-button--2.mt2")
            # upload_resume.click()
            wait = WebDriverWait(self.driver, 5)
            time.sleep(3)
            print("path: {}".format(os.getcwd() + "/{}".format(self.resume_path)))
            upload_resume.send_keys(os.getcwd() + "/{}".format(self.resume_path))
            # time.sleep(3)
            # upload_resume.send_keys(Keys.RETURN)
        except Exception as e:
            print('Could not find upload resume button, skipping...')
            print(e)

    def send_resume(self):
        print('in send_resume')
        try:
            file_upload_elements = (By.CSS_SELECTOR, "input[name='file']")
            if len(self.driver.find_elements(file_upload_elements[0], file_upload_elements[1])) > 0:
                input_buttons = self.driver.find_elements(file_upload_elements[0], file_upload_elements[1])
                for upload_button in input_buttons:
                    upload_type = upload_button.find_element(By.XPATH, "..").find_element(By.XPATH, "preceding-sibling::*")
                    if 'resume' in upload_type.text.lower():
                        upload_button.send_keys(self.resume_path)
                    elif 'cover' in upload_type.text.lower():
                        if self.cover_letter_dir != '':
                            upload_button.send_keys(self.cover_letter_dir)
                        elif 'required' in upload_type.text.lower():
                            upload_button.send_keys(self.resume_path)
        except Exception as e:
            print("Failed to upload resume or cover letter!")
            print(e)
            pass


    def enter_text(self, element, text):
        element.clear()
        element.send_keys(text)

    def select_dropdown(self, element, text):
        select = Select(element)
        select.select_by_visible_text(text)

    # Radio Select
    def radio_select(self, element, label_text, clickLast=False):
        print('in radio select')
        label = element.find_element(By.TAG_NAME, 'label')
        if label_text in label.text.lower() or clickLast == True:
            label.click()
        else:
            pass

    # Contact info fill-up
    def contact_info(self):
        print('in contact info')
        frm_el = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
        if len(frm_el) > 0:
            print('found contact info questions')
            for el in frm_el:
                text = el.text.lower()
                print("text: {}".format(text))
                if 'email address' in text:
                    continue
                elif 'phone number' in text:
                    try:
                        country_code_picker = el.find_element(By.CLASS_NAME, 'fb-dropdown__select')
                        self.select_dropdown(country_code_picker, self.personal_info['Phone Country Code'])
                    except:
                        print("Country code " + self.personal_info['Phone Country Code'] + " not found! Make sure it is exact.")
                    try:
                        phone_number_field = el.find_element(By.XPATH, "//input[contains(@id, 'phoneNumber')]")
                        self.enter_text(phone_number_field, self.personal_info['Mobile Phone Number'])
                    except:
                        print("Could not input phone number.")

    def fill_up(self):
        print('in fill up')
        try:
            easy_apply_content = self.driver.find_element(By.CLASS_NAME, 'jobs-easy-apply-content')
            # b4 = easy_apply_content.find_element(By.CLASS_NAME, 'pb4')
            pb4 = easy_apply_content.find_elements(By.CLASS_NAME, 'pb4')
            if len(pb4) > 0:
                for pb in pb4:
                    try:
                        label = pb.find_element(By.TAG_NAME, 'h3').text.lower()
                        print("label: {}".format(label))
                        try:
                            self.additional_questions()
                        except:
                            pass

                        try:
                            # self.send_resume()
                            self.my_send_resume()
                        except:
                            pass

                        if 'home address' in label:
                            self.home_address(pb)
                        elif 'contact info' in label:
                            self.contact_info()
                    except:
                        print('could not find h3 element, skipping...')
                        pass
        except:
            pass

    def write_to_file(self, company, job_title, link, location, search_location):
        to_write = [company, job_title, link, location]
        file_path = self.output_file_directory + self.file_name + search_location + ".csv"

        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(to_write)

    def scroll_slow(self, scrollable_element, start=0, end=3600, step=100, reverse=False):
        if reverse:
            start, end = end, start
            step = -step

        for i in range(start, end, step):
            self.driver.execute_script("arguments[0].scrollTo(0, {})".format(i), scrollable_element)
            time.sleep(random.uniform(1.0, 2.6))

    def avoid_lock(self):
        if self.disable_lock:
            return

        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(1.0)
        pyautogui.press('esc')

    def get_base_search_url(self, parameters):
        remote_url = ""

        if parameters['remote']:
            remote_url = "f_CF=f_WRA"

        level = 1
        experience_level = parameters.get('experienceLevel', [])
        experience_url = "f_E="
        for key in experience_level.keys():
            if experience_level[key]:
                experience_url += "%2C" + str(level)
            level += 1

        distance_url = "?distance=" + str(parameters['distance'])

        job_types_url = "f_JT="
        job_types = parameters.get('experienceLevel', [])
        for key in job_types:
            if job_types[key]:
                job_types_url += "%2C" + key[0].upper()

        date_url = ""
        dates = {"all time": "", "month": "&f_TPR=r2592000", "week": "&f_TPR=r604800", "24 hours": "&f_TPR=r86400"}
        date_table = parameters.get('date', [])
        for key in date_table.keys():
            if date_table[key]:
                date_url = dates[key]
                break

        easy_apply_url = "&f_LF=f_AL"

        extra_search_terms = [distance_url, remote_url, job_types_url, experience_url]
        extra_search_terms_str = '&'.join(term for term in extra_search_terms if len(term) > 0) + easy_apply_url + date_url

        return extra_search_terms_str

    def next_job_page(self, position, location, job_page):
        self.driver.get("https://www.linkedin.com/jobs/search/" + self.base_search_url +
                         "&keywords=" + position + location + "&start=" + str(job_page*25))

        self.avoid_lock()


if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()