# coding=utf-8
import requests
from lxml import etree
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Book():
    def __init__(self, name):

        self.name = name
        self.headers = {
            u'User-Agent': u'Mozilla/5.0 (Windows NT 6.3; Win64; x64)' u'AppleWebKit/537.36 (KHTML, like Gecko)' u'Chrome/63.0.3239.84 Safari/537.36',
            u'X-CSRFToken': u'9303a1f4b25e8f2f68d89b1d0e9cf615', u'Referer': u'http://neihanshequ.com/bar/1/',
            u'Cookie': u'uuid="w:99d7c4dc60eb4ae09556c6bc9dc6d253"; tt_webid=6529659478042854919; csrftoken=13753cb398583c33da5be8bf0f7727f7; _ga=GA1.2.1382869523.1520304821; _gid=GA1.2.1200588661.1520422263'}
        # self.name='《'+name+'》正文'

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        html = response.content.decode('gbk')
        return html

    def get_chapter(self, html):

        data = etree.HTML(html)
        book_name = data.xpath(
            u'//div[@style="text-align:center;"]/span[@style="font-size:20px;font-weight:bold;color:#f27622;"]/text()')
        # chapter_list = data.xpath('//li[@class="chapter"]')
        chapter_list = data.xpath(u'//div[text()="《' + self.name.decode() + '》正文"]/parent::div//li[@class="chapter"]')
        # chapter_list.reverse()
        print(chapter_list)
        for chapter in chapter_list:
            href = chapter.xpath(u'./a/@href')[0]
            print(href)
            chapter_name = chapter.xpath(u'./a/text()')[0]
            content = self.get_chapter_content(href)
            with open(book_name[0] + '.txt', 'a') as f:
                f.write(chapter_name + '\r\n')
                for data in content:
                    f.write(data + '\r\n')
                print('写入' + chapter_name + '完成')

    def get_chapter_content(self, url):
        response = requests.get(url=url, headers=self.headers)
        html = response.content.decode('gbk', errors='ignore')
        data = etree.HTML(html)
        content = data.xpath('//div[@class="content"]/text()')
        return content

    def search_book(self, name):
        drive = webdriver.Chrome()
        drive.get('http://www.cuiweijuxing.com/modules/article/search.php')
        search = drive.find_element_by_name('searchkey')
        search.send_keys(name.decode())
        submit = drive.find_element_by_name('submit')
        submit.click()
        # a=drive.find_element_by_class_name('c_subject')
        url = drive.find_element_by_xpath('//span[@class="c_subject"]/a').get_attribute("href")
        drive.close()
        return url

    def run(self):
        url = self.search_book(self.name.decode())
        print(url)
        html = self.parse_url(url)
        self.get_chapter(html)


if __name__ == '__main__':
    name = raw_input("请输入书名：")

    spider = Book(name)
    spider.run()
