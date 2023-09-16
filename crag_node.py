import logging
import logutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import ast

# Get module-level logger
_log = logging.getLogger(__name__)
_log.debug('Log initialized')

class CragNode():
    def __init__(self, url, driver) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Log initialized')

        self.url = url

        self.node_info_list = ['description', 'access-issues', 'approach']        
        self.node_info = {}
        self.get_node_info(driver)
        self.get_location(driver)
    
    def get_node_info(self, driver):
        driver.get(self.url)

        for info in self.node_info_list:
            try:
                markdown = driver.find_element(By.CLASS_NAME , f'node-info.{info}').find_element(By.CLASS_NAME, 'markdown')
                self.node_info[info] = markdown
                # self.node_info[info] = markdown.text
            except NoSuchElementException:
                self.node_info[info] = None
    
    def get_location(self, driver):
        driver.get(self.url)
        self.location = [
            float(driver.find_element(By.XPATH, "//meta[@property='place:location:latitude']").get_attribute('content')),
            float(driver.find_element(By.XPATH, "//meta[@property='place:location:longitude']").get_attribute('content'))
        ]

    # def get_area_poly(self, driver):
    #     try:
    #         # This is actually the bounding box for the map, not the area polygon
    #         map_script = driver.find_element(By.XPATH , f'/html/body/div[1]/div[3]/div[3]/div/div[3]/div/div[1]/script[6]')
    #         bound_string = re.findall('bbox: (.*),', map_script.get_attribute('innerHTML'))
    #         self.bounds = 
    #     except NoSuchElementException:
    #         self.bounds = None

    def get_sub_areas(self, driver):
        driver.get(self.url)
        area_el_list = driver.find_elements(By.CLASS_NAME , 'area')

    def get_photo_topos(self, driver):
        driver.get(self.url)
        self.photo_topos =[]

        pt_el_list = driver.find_elements(By.CLASS_NAME , 'phototopo')

        for pt in pt_el_list:
            tid = pt.get_attribute('data-tid')
            # self.photo_topos.append(tid)

            pt.screenshot(f'./phototopos/{tid}.png')


    # def get_parent_areas(self, driver):
    #     parent_el_list = driver.find_elements(By.CLASS_NAME , 'crumb.crumb--children')
    #     parent_el_list = parent_el_list.reverse()
    #     self.parents = []
    #     for parent in parent_el_list:
    #         pdict = {
    #             'name': 
    #         }
    #         self.parents

class CragRoute(CragNode):
    def __init__(self, url, driver) -> None:

        super().__init__(url, driver)
        self.route_info = {}
        self.get_route_info(driver)

    def get_route_info(self, driver):
        driver.get(self.url)
        # driver.find_elements(By.CLASS_NAME , 'heading__t')
        headline = driver.find_element(By.CLASS_NAME , 'headline')
        self.route_info['Name'] = re.findall('(?:<span itemprop="name">)(.*)(?=</span>)', headline.get_attribute('innerHTML'))

        self.route_info['Grade'] = driver.find_element(By.CLASS_NAME , 'grade').text
        # self.route_info['Grade Shade']

        headline_guts = driver.find_element(By.CLASS_NAME , 'headline__guts')
        self.route_info['Quality'] = re.findall('(?:"ratingValue" content=")([^"]*)', headline_guts.get_attribute('innerHTML'))
        self.route_info['Length'] = re.findall('(?:Length:</strong> )(.*)(?=</li>)', headline_guts.get_attribute('innerHTML'))
        self.route_info['Pitches'] = re.findall('(?:<li><strong>Pitches:</strong> )(.*)(?=<i class="icon-pitches"></i>)', headline_guts.get_attribute('innerHTML'))
        self.route_info['Bolts'] = re.findall('(?:<li><strong>Bolts:</strong> )(.*)(?=</li>)', headline_guts.get_attribute('innerHTML'))
        self.route_info['Ascents'] = re.findall('(?:<li><strong>Ascents:</strong> .*?>)(.*)(?=</a>)', headline_guts.get_attribute('innerHTML'))

        markdown = driver.find_element(By.CLASS_NAME , f'description.node-beta').find_element(By.CLASS_NAME, 'markdown')
        self.route_info['Description'] = markdown.text


        # Parse everything that should be just a string
        for key, value in self.route_info.items():
            try:
                if len(value) == 1:
                    self.route_info[key] = value[0]
            except:
                pass
            
            if value == []:
                self.route_info[key] = ''
        # self.route_info['Lists'] = 
        
        