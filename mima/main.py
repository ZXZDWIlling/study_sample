from selenium import webdriver
import xlwt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

xml_file = xlwt.Workbook()
table = xml_file.add_sheet('mima')

driver = webdriver.Firefox()
driver.implicitly_wait(60)
days = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
try:
    row = 0
    for month in range(len(days)):
        for day in range(days[month]):
            url = 'http://www.meiguoshenpo.com/mima/%02d%02d.html' % (month + 1, day + 1)
            print(url)
            driver.get(url)
            WebDriverWait(driver, 30, 0.5).until(ec.visibility_of_element_located((By.XPATH, '//html')))
            text = driver.find_element_by_xpath("//*[@id='LEFT_DIV']/div[1]/div[2]").text
            print(text)
            print('------------------------------------------------------------------')
            table.write(row, 0, '{0}月'.format(month + 1))
            table.write(row, 1, '{0}日'.format(day + 1))
            table.write(row, 2, url)
            table.write(row, 3, text)
            row += 1
        row += 1
except:
    xml_file.save('tmp.xls')
    driver.quit()

xml_file.save('tmp.xls')
driver.quit()


