from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import xlwt


xml_file = xlwt.Workbook()
table = xml_file.add_sheet('xingzuo')

desired_caps = dict()
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = '93ee2ab6'
desired_caps['platformVersion'] = '5.1.1'
desired_caps['appPackage'] = 'net.xingfuxingzuo.android'
desired_caps['appActivity'] = 'com.wintegrity.listfate.base.activity.StartActivity'


driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver_wait = WebDriverWait(driver, 30, 0.5)


driver.wait_activity('com.wintegrity.listfate.base.activity.MainTabActivity', 30)
driver.find_element_by_name('星座专区').click()

driver.wait_activity('com.wintegrity.listfate.base.activity.ConstellationDetailActivity', 30)
driver.find_element_by_id('net.xingfuxingzuo.android:id/tv_click3').click()
sleep(1)

while True:
    try:
        driver.find_element_by_name('星座+生肖+血型=?')
        break
    except NoSuchElementException:
        driver.swipe(285, 785, 285, 285, 500)


driver.find_element_by_name('星座+生肖+血型=?').click()
driver.wait_activity('com.wintegrity.listfate.base.activity.XingZuoTestActivity', 30)
button = driver.find_element_by_id('net.xingfuxingzuo.android:id/tv_look')
man_sel = driver.find_element_by_id('net.xingfuxingzuo.android:id/sp_your_col')
woman_sel = driver.find_element_by_id('net.xingfuxingzuo.android:id/sp_your_animal')
xue_sel = driver.find_element_by_id('net.xingfuxingzuo.android:id/sp_your_blood_type')
try:
    row = 0
    for i in range(11, 12):
        man_sel.click()
        driver_wait.until(ec.visibility_of_element_located((By.NAME, '请选择星座')))
        driver.find_elements_by_id('android:id/text1')[i].click()
        driver.wait_activity('com.wintegrity.listfate.base.activity.XingZuoTestActivity', 30)
        for j in range(5, 12):
            woman_sel.click()
            driver_wait.until(ec.visibility_of_element_located((By.NAME, '请选择生肖')))
            driver.find_elements_by_id('android:id/text1')[j].click()
            driver.wait_activity('com.wintegrity.listfate.base.activity.XingZuoTestActivity', 30)
            for k in range(4):
                xue_sel.click()
                driver_wait.until(ec.visibility_of_element_located((By.NAME, '请选择血型')))
                driver.find_elements_by_id('android:id/text1')[k].click()
                driver.wait_activity('com.wintegrity.listfate.base.activity.XingZuoTestActivity', 30)
                button.click()
                driver.wait_activity('com.wintegrity.listfate.base.activity.XZYSResultDetailActivity', 30)
                text = driver.find_elements_by_class_name("android.widget.TextView")[-1].text
                print(text)
                table.write(row, 0, text)
                row += 1
                print('-------------------------------------------------------------------------------')
                driver.press_keycode('4')
                driver.wait_activity('com.wintegrity.listfate.base.activity.XingZuoTestActivity', 30)
except:
    xml_file.save('tmp.xls')
    driver.quit()

xml_file.save('tmp.xls')
driver.quit()

