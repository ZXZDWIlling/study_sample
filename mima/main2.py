from selenium import webdriver
import xlwt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

xml_file = xlwt.Workbook()
table = xml_file.add_sheet('shu')

driver = webdriver.Firefox()
driver.implicitly_wait(60)
try:
    row = 0
    driver.get('http://www.meiguoshenpo.com/danshengshi/d34576.html')
    WebDriverWait(driver, 30, 0.5).until(ec.visibility_of_element_located((By.XPATH, '//html')))
    ele = driver.find_elements_by_xpath("//*[@id='LEFT_DIV']/div[1]/div[2]/p")
    for i in range(1, len(ele) - 1):
        if i == 2:
            continue
        text = ele[i].text
        table.write(row, 0, '11月')
        table.write(row, 1, '{0}日'.format(row + 1))
        table.write(row, 2, text)
        print(text)
        row += 1
        pass
except:
    xml_file.save('tmp.xls')
    # driver.quit()

xml_file.save('tmp.xls')
# driver.quit()


