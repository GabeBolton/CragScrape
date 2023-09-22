import logging
import logutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import ast
from crag_node import *
import datetime

# Get module-level logger
_log = logging.getLogger(__name__)
_log.debug('Log initialized')

class CragList():
    def __init__(self, url=None, driver=None) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Log initialized')
        self._unsaved_keys = ['log']

        self.url = url

        self.name = ''
        self._unsaved_keys = []
        self.last_update = datetime.datetime(2000,1,1)
        self.routes = []
        self.route_url_list = []
        if url is not None and driver is not None:
            self.update(driver)
    
    def update(self, driver):
        self.get_routes(driver)
        self.last_update = datetime.datetime.now()

    def get_name(self, driver):
        driver.get(self.url)
        self.name = driver.find_element(By.CLASS_NAME , 'list-container').get_attribute('data-list-name')

    def get_routes(self, driver, make_routes=False):
        driver.get(self.url)
        route_el_list = driver.find_elements(By.CLASS_NAME , 'list-item.route')
        
        self.route_comments = []
        self.route_url_list = []
        for r in route_el_list:
            this_href = re.findall('(?:<a href=")([^"]*)', r.get_attribute('innerHTML'))
            assert len(this_href) == 1 # Probably need to move the mouse so no routes are highlighted
            self.route_url_list.append('https://www.thecrag.com'+this_href[0])
            self.route_comments.append(r.find_element(By.CLASS_NAME , 'markdown.desc.item-comment').get_attribute('data-comment'))

        if make_routes:
            for url in self.route_url_list:
                self.routes.append(CragRoute(url, driver))