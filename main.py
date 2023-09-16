import selenium
import logging
import logutil
from selenium import webdriver
from crag_sesh import create_authenticated_session
from crag_node import *
from crag_list import CragList
import pdf_formatting
from gpx_export import gpx_export


# Get module-level logger
_log = logging.getLogger(__name__)
_log.debug('Log initialized')

# def identify_url_type(url):
#     if

def main(url):
    # URL of the area/list

    # Open the TheCrag.com website in a web browser
    driver = create_authenticated_session()

    # r = CragRoute('https://www.thecrag.com/en/climbing/chile/route/1203163971', driver)
    if 'list' in url:
        cl = CragList(url, driver)
    
    print(pdf_formatting.get_route_list_df(cl.routes))
    gpx_export([cl])


main("https://www.thecrag.com/en/list/8144130849")

"""
<div class="area" data-nid="323218395">
  <div class="loc"><a href="/en/climbing/australia/gibraltar-peak-and-corin-road-crags/snake-rock/area/323218395/locate" title="Located" class="mappin located">1</a></div>
  <div class="name"><a href="/en/climbing/australia/gibraltar-peak-and-corin-road-crags/snake-rock/area/323218395"><span class="primary-node-name">Scooby</span></a>
    <span class="type">sector</span>
  </div>
  <div class="style">
<a title="Filter to 3 Top roping routes" href="/routes/at/323218395/with-gear-style/top rope/"><b class="bullet toprope"></b>&nbsp;All Top roping</a></div>
  <div class="stats">
    <div class="routes"><a href="/routes/at/323218395" title="Search and filter these routes">3</a></div>
    <div class="ticks"><a href="/ascents/at/323218395" title="Search and filter these ascents">50</a></div>
    <div class="height">8m</div>
    <div class="grades"><div class="band grade-band"><b class="gb1" style="width: 100%" title="3 Beginner routes"></b></div>

</div>
    <div class="topos">1    </div>
    <div class="a-pop"><a href="/en/climbing/australia/gibraltar-peak-and-corin-road-crags/snake-rock/area/323218395/ascents" class="iblock pop pop--1" title="Relative popularity (10) - 50 ascents"><span class="va-m"></span></a></div>
  </div>
</div>
"""

pass