import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

class Page:
    _url = None
    _driver = None
    _companies = {}
    _stack = []
    def __init__(self, url):
        self._url = url

    def load(self):
        print("pagesToCrawl:"+str(len(Page._stack))+" CurrentPage: " + self._url)
        Page._driver.get(self._url)

    def scrape(self):
        pass

    def isNot404(self):
        error_selector = "#page-layout > div.content-cover > div.content-inner > div:nth-child(3)"
        return Page._driver.find_element_by_css_selector(error_selector).text == ""

    @staticmethod
    def setDriver(driver):
        Page._driver = driver

    @staticmethod
    def getCompanies():
        return Page._companies

    @staticmethod
    def run():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = Chrome(executable_path=os.path.abspath('chromedriver'), options=chrome_options)
        driver.implicitly_wait(3)

        Page._driver = driver

        while Page._stack:
            page = Page._stack.pop()
            page.load()
            page.scrape()

        driver.close()
        driver.quit()

    @staticmethod
    def addPage(page):
        Page._stack.append(page)