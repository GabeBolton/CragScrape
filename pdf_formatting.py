import logging
import logutil
import pandas as pd
from crag_node import CragRoute


def get_route_list_df(route_list: [CragRoute]):
    
    ls = []
    for r in route_list:
        d = r.route_info.copy()
        d['loc'] = r.location
        ls.append(d)
        
    rldf = pd.DataFrame(ls)

    return rldf