import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
import os.path
import time

# Get module-level logger
_log = logging.getLogger(__name__)
_log.debug('Log initialized')

class CragDriver(webdriver.Chrome):
    def __init__(self, rate_limit=0, no_double_get=True, options: Options = None, service: Service = None, keep_alive: bool = True) -> None:
        self.rate_limit = rate_limit
        self.no_double_get = no_double_get

        super().__init__(options, service, keep_alive)

    def get(self, url: str) -> None:
        if self.current_url == url and self.no_double_get:
            return
        if self.rate_limit > 0:
            time.sleep(self.rate_limit)
        return super().get(url)

def create_authenticated_session(sesh_dir=None, save_sesh=False, rate_limit=0, no_double_get=True, dpi=1.0) -> CragDriver:
    # not implemented
    if sesh_dir is None:
        sesh_dir = f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data\\CragScrape'

    if save_sesh or os.path.exists(sesh_dir):
        options_ = webdriver.ChromeOptions()
        options_.add_argument(f"user-data-dir={sesh_dir}")
        options_.add_argument(f"--force-device-scale-factor={dpi}")
        options_.add_argument("window-size=1980,960")
        options_.add_argument("headless")
        # options_.add_argument("screenshot")
        driver = CragDriver(rate_limit=rate_limit, no_double_get=no_double_get, options=options_)
    else:
        driver = CragDriver()


    driver.get("https://www.thecrag.com/dashboard")
    try:
        driver.find_element(By.ID, 'loginInputLogin').send_keys(input("Username: "))
        driver.find_element(By.ID, 'loginInputPassword').send_keys(getpass.getpass("Password: "))
        driver.find_element(By.ID, 'btnLogin').click()
    except:
        pass
    return driver

