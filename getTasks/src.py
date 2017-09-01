# coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from dictionary_tool.langconv import *
from time import sleep
from json.decoder import JSONDecodeError

COL_ORDO = 4
COL_SCANCIT = 5
COL_MISSA = 6
COL_MATUTINUM = 7
COL_LAUDES = 8
COL_HORA_MEDIA = 9
COL_VESPERAE = 10
COL_COMPLETORIUM = 11


class SrcUnit:
    task_col = (COL_ORDO, COL_SCANCIT, COL_MISSA, COL_MATUTINUM,
                COL_LAUDES, COL_HORA_MEDIA, COL_VESPERAE, COL_COMPLETORIUM,)

    def __init__(self, driver=None):
        # # 初始化字典
        # self.translator = Translator(service_urls=['translate.google.cn'])
        # 初始化selenium
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver.get('http://www.mhchina.net/index.html')
        # 点击普世教会
        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_all_elements_located((By.XPATH, '*')))
        ActionChains(self.driver)\
            .move_to_element(self.driver.find_element_by_xpath("//*[@id='qm0']/a[1]/span/span[5]")).perform()
        self.driver.find_element_by_link_text('普世教會').click()
        # 功课列表共有11列
        WebDriverWait(self.driver, 30, 0.5).until(ec.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))
        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'wkheader')))
        self.dates = self.driver.find_elements_by_xpath("html/body/table/tbody/tr/td[1]")
        self.subjects = self.driver.find_elements_by_xpath("html/body/table/tbody/tr/td[3]")
        # print(len(self.dates), len(self.subjects))
        # 日期to主题的字典
        self.date_to_subject = dict()
        # 日期to行号的字典
        self.date_to_row = dict()
        for row in range(len(self.dates)):
            self.date_to_subject[self.dates[row].text] = self.subjects[row].text
            self.date_to_row[self.dates[row].text] = row + 1
        print(len(self.date_to_subject))
        pass

    def get_content_by_row(self, row, col, block_size=1000):
        if col == 4:
            return ''
        # 滑动到要获取的行
        ele = self.driver.find_element_by_xpath("html/body/table/tbody/tr[{0}]/td[{1}]/a"
                                                .format(row, col))
        js = "window.scrollTo({0},{1})".format(ele.location_once_scrolled_into_view['x'],
                                               ele.location_once_scrolled_into_view['y'])
        self.driver.execute_script(js)

        sleep(5)
        ele.click()
        sleep(5)
        text = self.driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        body = ''
        try:
            while len(text) > block_size:
                # body += self.translator.translate(text[:block_size], 'zh-cn').text
                body += Converter('zh-hans').convert(text[:block_size])
                text = text[block_size:]
            else:
                # body += self.translator.translate(text, 'zh-cn').text
                body += Converter('zh-hans').convert(text)
                self.driver.back()
        except JSONDecodeError:
            s = body
            body = ''
            for i in s.split('</p>')[:-1]:
                body += i
            body += '</p></div>'
            self.driver.back()
        WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'wkheader')))
        # print(date, body)
        return body

    def get_content_by_date(self, date, col, block_size=1000):
        """"根据日期查找内容"""
        # if col == 4:
        #     return ''
        # # 滑动到要获取的行
        # ele = self.driver.find_element_by_xpath("html/body/table/tbody/tr[{0}]/td[{1}]/a"
        #                                         .format(self.date_to_row[date], col))
        # js = "window.scrollTo({0},{1})".format(ele.location_once_scrolled_into_view['x'],
        #                                        ele.location_once_scrolled_into_view['y'])
        # self.driver.execute_script(js)
        #
        # sleep(5)
        # ele.click()
        # sleep(5)
        # text = self.driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        # body = ''
        # try:
        #     while len(text) > block_size:
        #         body += self.translator.translate(text[:block_size], 'zh-cn').text
        #         text = text[block_size:]
        #     else:
        #         body += self.translator.translate(text, 'zh-cn').text
        #
        #         self.driver.back()
        # except JSONDecodeError:
        #     s = body
        #     body = ''
        #     for i in s.split('</p>')[:-1]:
        #         body += i
        #     body += '</p></div>'
        #     self.driver.back()
        # WebDriverWait(self.driver, 30, 0.5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'wkheader')))
        # # print(date, body)
        return self.get_content_by_row(self.date_to_row[date], col, block_size)

    def get_day_task_by_date(self, date):
        """"获取每日内容"""
        day_task = []
        for col in SrcUnit.task_col:
            content = self.get_content_by_date(date, col)
            # 去掉多余的注释
            try:
                while True:
                    i, j = content.index('<!--'), content.index('-->')
                    content = content[:i] + content[j + 3:]
            except ValueError:
                print(content)
            title = '礼仪' if col == COL_ORDO else content.split('</')[0].split('>')[-1]
            # 去掉末尾可能的空格
            title = title[:-6] if title.endswith('&nbsp;') else title
            day_task.append(dict(title=title, subject=self.date_to_subject[date],
                                 content=content, date=date, col=col))
        return day_task
        pass

    def get_day_task_by_row(self, row):
        """"获取每日内容"""
        # date = self.dates[row - 1].text
        # day_task = []
        # for col in SrcUnit.task_col:
        #     content = self.get_content_by_date(date, col)
        #     title = '礼仪' if col == COL_ORDO else content.split('</')[0].split('>')[-1]
        #     day_task.append(dict(title=title, subject=self.date_to_subject[date],
        #                          content=content, date=date, col=col))
        self.dates = self.driver.find_elements_by_xpath("html/body/table/tbody/tr/td[1]")
        return self.get_day_task_by_date(self.dates[row - 1].text)
        pass

    def get_tasks(self, start_date):
        """抓取最新功课"""
        tasks = list()
        print('start:', self.date_to_row[start_date] + 1, 'end', self.date_to_row[self.dates[-1].text])
        for i in range(self.date_to_row[start_date] + 1, self.date_to_row[self.dates[-1].text] + 1):
            tasks.append(self.get_day_task_by_row(i))
        return tasks
        pass

# print(SrcUnit().get_content_by_date('09 月 16 日', COL_COMPLETORIUM, 1000))
# print(SrcUnit().get_content_by_row(20, COL_COMPLETORIUM, 1000))

# SrcUnit().get_tasks('09 月 16 日')

    def close(self):
        self.driver.close()

if __name__ == '__main__':
    exec(open('main.py', encoding='utf-8').read())
    pass
