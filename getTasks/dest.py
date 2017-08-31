# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select


class DesUnit:
    VAL_ORDO = 23
    VAL_SCANCIT = 24
    VAL_MISSA = 25
    VAL_MATUTINUM = 26
    VAL_LAUDES = 27
    VAL_HORA_MEDIA = 28
    VAL_VESPERAE = 29
    VAL_COMPLETORIUM = 30

    def __init__(self, username, password, driver=None):
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver.implicitly_wait(30)
        self.driver.get('https://www.baiibai.com/static/manager/#/login')

        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.TAG_NAME, 'form')))
        self.driver.find_element_by_xpath("//*[@id='app']/div/div/div[2]/form/div[1]/input").send_keys(username)
        self.driver.find_element_by_xpath("//*[@id='app']/div/div/div[2]/form/div[2]/input").send_keys(password)
        self.driver.find_element_by_tag_name('button').click()
        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'logo')))

        self.driver.find_element_by_xpath("//*[@id='home']/div/div[2]/div[7]/div[1]").click()
        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.LINK_TEXT, '功课管理')))
        self.driver.find_element_by_xpath("//*[@id='home']/div/div[2]/div[7]/div[2]/a[2]").click()

        Select(self.driver.find_element_by_tag_name('select')).select_by_value('3')

    @staticmethod
    def date_to_str(date):
        ret = ''
        for i in date:
            if '0' <= str(i) <= '9':
                ret += i
        ret = '2017-' + ret[:2] + '-' + ret[2:]
        return ret

    def insert(self, task):
        """插入一条功课"""
        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.XPATH, "//form/button")))
        self.driver.find_element_by_xpath("//form/button").click()
        WebDriverWait(self.driver, 30, 0.5)\
            .until(ec.visibility_of_element_located((By.XPATH, "//*[@id='home']/div/div[3]/div/div/div/span")))

        Select(self.driver.find_element_by_xpath("//*[@id='home']/div/div[3]/div/div/form/div[1]/select"))\
            .select_by_value('3')
        Select(self.driver.find_element_by_xpath("//*[@id='home']/div/div[3]/div/div/form/div[2]/select"))\
            .select_by_value(str(task['col'] + 19))

        edit_lines = self.driver.find_elements_by_xpath("//*[@id='home']/div/div[3]/div/div/form/div/input")
        edit_lines[0].send_keys(task['title'])
        edit_lines[1].send_keys(task['subject'])
        edit_lines[2].send_keys(self.date_to_str(task['date']))
        edit_lines[3].send_keys('0')

        self.driver.find_element_by_xpath("//*[@id='home']/div/div[3]/div/div/form/div[7]/textarea")\
            .send_keys(task['content'])
        self.driver.find_element_by_xpath("//*[@id='home']/div/div[3]/div/div/form/button").click()
        WebDriverWait(self.driver, 30, 0.5).until(ec.alert_is_present())
        self.driver.switch_to.alert.accept()
        pass

    def insert_day_task(self, task_list):
        """"插入一天的功课"""
        for i in range(len(task_list)):
            self.insert(task_list[i])
        pass

if __name__ == '__main__':
    exec(open('main.py', encoding='utf-8').read())
    pass
