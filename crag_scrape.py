import logging
import logutil
import json
from crag_sesh import create_authenticated_session
from crag_node import CragNode, CragRoute, CragArea
from crag_list import CragList
import datetime
import pickle
import json

_log = logging.getLogger(__name__)
_log.debug('Log initialized')

def get_url_class(url):
    if 'list' in url:
        return CragList
    if 'route' in url:
        return CragRoute
    return CragNode


class CragScrape():
    def __init__(self, folder=None, do_load=True, expand_lists=True, expand_subareas=False, expand_area_routes=True) -> None:
        if folder is None:
            folder = './default-scrape/'
        self.folder = folder
        self.json_name = 'scrape.json'

        self._unsaved_keys = ['log', 'driver', 'update_interval']
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Log initialized')

        self.expand_lists = expand_lists
        self.expand_subareas = expand_subareas
        self.expand_area_routes = expand_area_routes

        self.last_update = datetime.datetime(2000,1,1)

        self.driver = create_authenticated_session()
        self.update_interval = {
            CragArea: datetime.timedelta(1 * 7),
            CragRoute: datetime.timedelta(1 * 30),
            CragList: datetime.timedelta(0)
        }
        self.objs = {} # url: object, last update
        self.outputs = {}

        try:
            if do_load:
                self = self.load(filename=self.folder + self.json_name)
        except FileNotFoundError:
            pass


    def scrape_url(self, url):
        url_class = get_url_class(url)
        if url in self.objs.keys():
            if self.objs[url].last_update + self.update_interval[url_class] < datetime.datetime.now():
                self.log.debug(f'Updating {url}')
                self.objs[url].update(self.driver)
            else:
                self.log.debug(f'Not updating {url}: recently updated')
        else:
            self.log.debug(f'Creating {url}')
            self.objs[url] = url_class(url, driver=self.driver)
   
    def scrape(self, url_list=None, check_updates=True): #, expand_list_override=None, expand_subarea_override=None):
        if check_updates:
            if url_list is None:
                url_list = []
            url_list = list(set(url_list+list(self.objs.keys())))

        if url_list is not None:
            for url in url_list:
                self.scrape_url(url)
        
        if self.expand_lists:# and (expand_list_override is None or expand_list_override == True):
            this_url_list = list(self.objs.keys()).copy()
            for url in this_url_list:
                cl = self.objs[url]
                if isinstance(cl, CragList):
                    for url in cl.route_url_list:
                        self.scrape_url(url)

        need_to_rerun = False
        if self.expand_subareas:# and (expand_subarea_override is None or expand_subarea_override == True):
            this_url_list = list(self.objs.keys()).copy()
            for url in this_url_list:
                ca = self.objs[url]
                if isinstance(ca, CragArea):
                    for url in ca.area_url_list:
                        self.scrape_url(url)
                        if self.objs[url].area_url_list != []:
                            need_to_rerun = True

        if self.expand_area_routes:# and (expand_subarea_override is None or expand_subarea_override == True):
            this_url_list = list(self.objs.keys()).copy()
            for url in this_url_list:
                ca = self.objs[url]
                if isinstance(ca, CragArea):
                    for url in ca.route_url_list:
                        self.scrape_url(url)
        
        if need_to_rerun:
            self.log.info('Scraping again to expand subareas')
            self.scrape(check_update=False)
        else:
            self.last_update = datetime.datetime.now()
            self.save()
    
    def save(self):
        with open(self.folder + self.json_name, 'w') as file:
            # pickle.dump(self, file)
            file.write(json.dumps(self, default=self._default_serialization))

    def load(self, filename):           
        with open(filename, 'r') as file:
            json_dict = json.load(file)
            pass

        def parse_date_times(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    if list(value.keys()) == ['year', 'month', 'day', 'hour', 'minute', 'second']:
                        d[key] = datetime.datetime(**value)
                    else:
                        d[key] = parse_date_times(value)
            return d
        # Parse all datetimes
        json_dict = parse_date_times(json_dict)

        for url, object_dict in json_dict['objs'].items():
            obj = get_url_class(url)()
            obj.__dict__.update(object_dict)
            json_dict['objs'][url] = obj
        
        self.__dict__.update(json_dict)



    def get_routes(self):
        return [obj for obj in self.objs.values() if isinstance(obj, CragRoute)]
    

    def _default_serialization(self, obj):
        if isinstance(obj, datetime.datetime):
            return dict(year=obj.year, month=obj.month, day=obj.day, hour=obj.hour, minute=obj.minute, second=obj.second)
        if isinstance(obj, CragScrape):
            return {key: value for key, value in obj.__dict__.items() if key not in obj._unsaved_keys}
        if isinstance(obj, (CragNode, CragArea, CragRoute, CragList)):
            return {key: value for key, value in obj.__dict__.items() if key not in obj._unsaved_keys}
    
    # def _default_serialization(obj):
    #     if isinstance(obj, datetime.datetime):
    #         return {'datetime': dict(year=obj.year, month=obj.month, day=obj.day, hour=obj.hour, minute=obj.minute, second=obj.second)}
    #     if isinstance(obj, CragScrape):
    #         return {key: value for key, value in obj.__dict__.items() if key not in obj._unsaved_keys}
    #     if isinstance(obj, (CragNode, CragArea, CragRoute, CragList)):
    #         return {key: value for key, value in obj.__dict__.items() if key not in obj._unsaved_keys}


