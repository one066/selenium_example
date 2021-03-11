import time
from selenium import webdriver
from lxml import html
import json

# -*- coding: utf-8 -*-
# @type    ：selenium实例
# @Time    : 2019/12/18 14:58
# @Author  : one

def read_message():
    '''
    读取答案
    '''

    ls = []
    with open("daan.txt", "r", encoding="utf-8") as f:
        for lines in f.readlines():
            line = lines.strip().split(" ")
            chapter = line[0]
            line.pop(0)
            ls.append([chapter, line])
        f.close()
    return ls

def read_cookies():
    '''
    读取用户cookie
    '''
    with open("cookie.txt", "r", encoding="utf-8") as f:
        js = f.read()
        dic = json.loads(js)
        f.close()
    return dic

def start_exercise(leaf, tree, dict_ls):
    '''
    开始模拟做题
    '''

    num = leaf[0]
    for number in tree:
        if num in number:
            num = number
            break

    url = dict_ls['{}'.format(num)]
    driver.get(url)

    try:
        driver.find_element_by_xpath(
            '//div[@class="sequence-list-wrapper"]/ol/li/a[@class="seq_html inactive  text-center"]').click()  # 选择做题
    except:
        driver.find_element_by_xpath(
            '//div[@class="sequence-list-wrapper"]/ol/li/a[@class="seq_html inactive active text-center"]').click()  # 选择做题
    driver.find_element_by_class_name("test-btn").click()
    time.sleep(1)
    for index,i in enumerate(leaf[1]):
        for x in i:
            num1 = int(chr(ord(x) - 17))
            driver.find_elements_by_xpath('//div[@class="row bg-row"]/section/label/i')[num1].click()  # 选择答案
        if index != len(leaf[1]) - 1:
            driver.find_element_by_xpath('//div[@class="text-right padding-10"]/button[@class="btn btn-primary"]').click() # 下一题
            time.sleep(1)
        else:
            driver.find_element_by_xpath('//div[@class="text-right padding-10"]/button[@class="btn btn-primary btn-xs"]').click() # 提交
            time.sleep(1)
            driver.find_element_by_xpath('//div[@class="ui-dialog_art-button"]/button[@data-id="ok"]').click() # 确定
            time.sleep(1)
            driver.find_element_by_xpath('//div[@class="ui-dialog_art-button"]/button[@data-id="cancel"]').click() # 取消
    print('{}--->已完成'.format(num))


def init(driver):
    '''
    初始化操作
    '''
    value = input('是否第一次登录：   （Y/N）')
    if value == 'Y':

        driver.get(url)
        user = input('输入账号：')
        password = input('输入密码：')
        driver.find_element_by_name('userName').send_keys("{}".format(user))
        driver.find_element_by_name('password').send_keys("{}".format(password))
        print('输入验证码并登录')
        print('登录到主页，确保要做的科目在第一个')
        input('任意键继续：')

        '''
        保存cookies
        '''
        cookies = driver.get_cookies()
        with open("cookie.txt", "a", encoding="utf-8") as f:
            js = json.dumps(cookies)
            f.write(js)
        f.close()

    if value == 'N':
        '''
        读取cookies
        '''
        driver.get(url)
        driver.delete_all_cookies()
        for cookie in read_cookies():
            driver.add_cookie(cookie)


def start():
    '''
    引擎
    '''
    tree_dict = {}
    driver.maximize_window()
    driver.get(url)

    driver.find_element_by_xpath('//td[@style="border-top: none;"]/span/a[@class="btn btn-primary pull-right"]').click()
    source = driver.page_source
    s2 = html.etree.HTML(source)
    chapter_url =  s2.xpath('//div[@class="tree"]/ul/li/ul/li/a/@href')
    chapter_name = s2.xpath('//div[@class="tree"]/ul/li/ul/li/a/text()')

    for index, dict1 in enumerate(chapter_name):
        xx = {'{}'.format(dict1):'{}'.format('http://mooc.neumooc.com/' + chapter_url[index])}
        tree_dict.update(xx)

    for line in read_message():
        start_exercise(line, chapter_name, tree_dict)


if __name__ == '__main__':
    url = 'http://mooc.neumooc.com/personal/index'
    driver = webdriver.Chrome()
    init(driver)
    start()
