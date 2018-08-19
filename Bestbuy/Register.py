
import os
import logging
from time import sleep, clock
from selenium.webdriver.support.ui import Select
from webinterface import WebInterface
from random import randint
import random, string
import time
from threading import Thread


def randomName():
    from itertools import product

    first_name = "jay", "jim", "roy", "axel", "billy", "charlie", "jax", "gina", "paul", "ringo", "ally", "nicky", "cam", "ari", "trudie", "cal", "carl", "lady", "lauren", "ichabod", "arthur", "ashley", "drake", "kim", "julio", "lorraine", "floyd", "janet", "lydia", "charles", "pedro", "bradley"
    last_name = "barker", "style", "spirits", "murphy", "blacker", "bleacher", "rogers", "warren", "keller"

    full_names = ["{} {}".format(f, l) for f, l in product(first_name, last_name) if f != l]
    name = random.choice(full_names)
    firstandlast = name.split(' ')
    return firstandlast


class Bestbuy(WebInterface):
    """ Parent Class to hold the operation of multiple pages of ProductLink Web. """
    def __init__(self):
        """ Initialize function for the Parent Class. """
        super(Bestbuy, self).__init__()
        self.base_url = ''


    def Register(self, url="https://www-ssl.bestbuy.com/profile/a/emailsub/student", firstname = "AUTO", lastname = "EDU", password = 'Password!', email = "ggased@creamdeal.biz", phone = "3096751498"):
        firstandlast = randomName()
        firstname = firstandlast[0]
        lastname = firstandlast[1]
        randomstring = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        email = randomstring + '+' + str(randint(1,20))+'@creamdeal.biz'
        password = randomstring + '2606!'
        phone = '877' + ''.join(random.choice(string.digits) for _ in range(7))
        self.init_driver()
        self.base_url = url
        self.enter_url(url)
        sleep(2)
        self.click('//*[@aria-label="Create Account"]')
        self.input('//*[@id="fld-firstName"]', firstname)
        self.input('//*[@id="fld-lastName"]', lastname)
        self.input('//*[@id="fld-e"]', email)
        self.input('//*[@id="fld-p1"]', password)
        self.input('//*[@id="fld-p2"]', password)
        self.input('//*[@id="fld-phone"]', phone)
        self.click('//*[@type="submit"]')
        return True

    def Enroll(self):
        #self.click('//*[@aria-label="describes-you"]')
        self.click('//*[@id="describes-you"]/option[3]')
        randmonth = randint(2, 13)
        self.click('//*[@id="birth-month"]')
        self.click('//*[@id="birth-month"]/option['+str(randmonth)+']')
        randday = randint(2, 25)
        self.click('//*[@id="birth-day"]')
        self.click('//*[@id="birth-day"]/option['+str(randday)+']')
        self.input('//*[@id="school-search"]', 'BRADLEY UNIVERSITY')
        self.click('//*[@id="graduation-month"]')
        self.click('//*[@id="graduation-month"]/option[6]')
        self.click('//*[@id="graduation-year"]')
        self.click('//*[@id="graduation-year"]/option[6]')
        self.click('//*[@id="studentVerification"]/div[2]/div/form/div[7]/div[1]/button')
        if self.find_element_by_xpath('//*[@id="studentVerification"]/div[2]/div/p'):
            print 'Success!'


def run():
    test = Bestbuy()
    try:
        test.Register()
        test.Enroll()
        test.close()
    except:
        test.close()
        pass


if __name__ == '__main__':
    for i in range(10):
        threads = []
        for i in range(8):
            th = Thread(target=run)
            threads.append(th)
        for t in threads:
            t.start()
        sleep(100)
