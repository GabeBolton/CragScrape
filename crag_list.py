import logging
import logutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import ast
from crag_node import *

# Get module-level logger
_log = logging.getLogger(__name__)
_log.debug('Log initialized')

class CragList():
    def __init__(self, url, driver) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Log initialized')

        self.url = url
        
        self.routes = []
        self.get_routes(driver)

    def get_routes(self, driver):
        driver.get(self.url)
        route_el_list = driver.find_elements(By.CLASS_NAME , 'list-item.route')
        
        self.route_comments = []
        route_url_list = []
        for r in route_el_list:
            this_href = re.findall('(?:<a href=")([^"]*)', r.get_attribute('innerHTML'))
            assert len(this_href) == 1
            route_url_list.append('https://www.thecrag.com'+this_href[0])
            self.route_comments = r.find_element(By.CLASS_NAME , 'markdown.desc.item-comment').get_attribute('data-comment')

        for url in route_url_list:
            self.routes.append(CragRoute(url, driver))