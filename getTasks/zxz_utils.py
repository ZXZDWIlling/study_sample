# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from time import sleep

m_driver = None


def get_driver(is_new=False):
    global m_driver
    if is_new or m_driver is None:
        m_driver = webdriver.Firefox()
    return m_driver


def get_last_day():
    """获取上一次添加的记录的功课日期"""
    driver = get_driver()
    driver.implicitly_wait(30)
    driver.get('https://www.baiibai.com/static/manager/#/login')
    WebDriverWait(driver, 30, 0.5).until(ec.visibility_of_element_located((By.TAG_NAME, 'form')))
    driver.find_element_by_xpath("//*[@id='app']/div/div/div[2]/form/div[1]/input").send_keys('05521397022')
    driver.find_element_by_xpath("//*[@id='app']/div/div/div[2]/form/div[2]/input").send_keys('123456')
    driver.find_element_by_tag_name('button').click()
    WebDriverWait(driver, 30, 0.5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'logo')))

    driver.find_element_by_xpath("//*[@id='home']/div/div[2]/div[7]/div[1]").click()
    WebDriverWait(driver, 30, 0.5).until(ec.visibility_of_element_located((By.LINK_TEXT, '功课管理')))
    driver.find_element_by_xpath("//*[@id='home']/div/div[2]/div[7]/div[2]/a[2]").click()

    Select(driver.find_element_by_tag_name('select')).select_by_value('3')
    sleep(2)
    last_day = driver.find_element_by_xpath("//*[@id='home']/div/div[3]/div/div/table/tbody/tr[1]/td[7]").text.split('-')
    last_day = last_day[1] + ' 月 ' + last_day[2] + ' 日'
    print('last day：' + last_day)
    return last_day
    pass


def quit_driver():
    if m_driver is not None:
        m_driver.quit()
    pass


def get_config():
    """读取配置文件"""
    config_file = open("config.txt", 'r', encoding='utf-8')
    config = dict()
    for line in config_file:
        if line.startswith('#') or line.startswith('.#'):
            continue
        try:
            config[line.split(':')[0]] = line.split(':')[1].rstrip()
        except IndexError:
            pass
    print(config)
    config_file.close()
    return config


def close():
    m_driver.close()

if __name__ == '__main__':
    exec(open('main.py', encoding='utf-8').read())
    pass


