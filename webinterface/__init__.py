"""
Package for acting as a wrapper for Webinterface for Selenium Driver .
"""
import logging
import json
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains, DesiredCapabilities

class WebInterface(object):
    """ Parent Class for WebInterface. """
    def __init__(self, driver_type="Chrome"):
        """ Method to Instance for Webinterface. """
        mainpath = os.path.dirname(os.path.realpath(__file__))
        self.is_performance = False
        self.screenshot = ""
        if driver_type == 'Chrome':
            self._chromeops = webdriver.ChromeOptions()
            prefs = {"download.default_directory": mainpath + r"\bin\download_files",
                     "download.prompt_for_download": False,
                     'credentials_enable_service': False,
                     'profile': {
                         'password_manager_enabled': False
                     },
                     "applicationCacheEnabled": True,
                     "safebrowsing": {"enabled": True, "malware": {"enabled": True}}}
            self._caps = DesiredCapabilities.CHROME
            if self.is_performance:
                self._caps['loggerPrefs'] = {'performance': 'ALL'}
            self._chromeops.add_experimental_option("prefs", prefs)
            self._chromeops.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            self._chromeops.add_argument("--start-maximized")
            self._chromeops.add_argument("--disable-plugins")
            self._chromeops.add_argument("--disable-extensions")
            self._chromeops.add_argument("--disable-infobars")
            self._chromedriver = r"{}\bin\chromedriver.exe".format(mainpath)
        self.driver = None
        self.actionChains = None

    def init_driver(self, driver_type="Chrome"):
        """ Initialize the driver for the Webinterface. """
        mainpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        if driver_type == "Chrome":
            self.driver = webdriver.Chrome(executable_path=self._chromedriver,
                                           chrome_options=self._chromeops,
                                           desired_capabilities=self._caps)
        elif driver_type == "IE":
            ie_driver = r"{0}\bin\IEDriverServer.exe".format(mainpath)
            self.driver = webdriver.Ie(executable_path=ie_driver)
        self.driver.implicitly_wait(3)
        self.driver.maximize_window()
        self.actionChains = ActionChains(self.driver)

    def close(self):
        """ Method to Close the Webinterface. """
        if self.is_performance:
            logs = [json.loads(log['message'])['message'] for log in self.driver.get_log('performance')]
            with open(r'C:\Tools\devtools.json', 'wb') as filepointer:
                json.dump(logs, filepointer, indent=4)
        self.driver.close()
        self.driver.quit()

    def enter_url(self, url):
        """ Method to Enter the URL. """
        self.driver.get(url)
        return True

    def is_element_present(self, xpath):
        """ Method to verify Is the Element is present. """
        xpath = self.generate_xpath_structure(xpath)
        element_present = self.driver.find_element_by_xpath(xpath)
        sleep(1)
        return element_present.is_enabled()

    def find_element_by_xpath(self, xpath):
        """ Method to find the Element by Xpath. """
        xpath = self.generate_xpath_structure(xpath)
        if self.is_element_present(xpath):
            return self.driver.find_element_by_xpath(xpath)
        else:
            return False

    def find_element_by_id(self, attrib_id):
        """ Method to find the Element by ID. """
        elem = self.driver.find_element_by_id(attrib_id)
        return elem

    def click(self, xpath):
        """ Method to find and click element by Xpath."""
        try:
            xpath = self.generate_xpath_structure(xpath)
            element = self.find_element_by_xpath(xpath)
            element.click()
        except Exception as err:
            logging.error("Error while Clicking {}".format(xpath))
            logging.error("Error information {}".format(str(err)))
        return True

    def input(self, xpath, value):
        """ Method to enter the value"""
        xpath = self.generate_xpath_structure(xpath)
        element = self.find_element_by_xpath(xpath)
        element.clear()
        sleep(0.5)
        for i in value:
            element.send_keys(i)
            sleep(0.1)

    def input_action(self, xpath, value):
        """ Method to enter the value using action. """
        element = self.find_element_by_xpath(xpath)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.click()
        action.send_keys(value)
        action.perform()

    def enter_key(self, xpath):
        """ Method to enter the ENTER KEY to the  Webpage. """
        element = self.find_element_by_xpath(xpath)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.click()
        action.send_keys(Keys.ENTER)
        action.perform()

    def wait_till_delay(self, xpath, delay=20):
        """ Method to Wait for the Xpath element to available for processing. """
        xpath = self.generate_xpath_structure(xpath)
        WebDriverWait(self.driver, delay).until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))

    @staticmethod
    def generate_xpath_structure(xpath):
        """ Simplified Method to Create the Xpath, by attribute and value."""
        if isinstance(xpath, tuple) or isinstance(xpath, list):
            return ".//*[@{}='{}']".format(xpath[0], xpath[1])
        else:
            return xpath

