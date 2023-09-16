import logging
import logutil
import gpxpy
import gpxpy.gpx
from crag_node import CragNode, CragRoute
from crag_list import CragList

# Get module-level logger
_log = logging.getLogger(__name__)
_log.debug('Log initialized')


def gpx_export(crag_object_list, filename=None, node_expand_children=False):
    if filename is None:
        if len(crag_object_list) == 1 and isinstance(crag_object_list[0], CragList):
            filename = './gpx_files/'+crag_object_list[0].name+'.gpx'
        else:
            filename = './gpx_files/out.gpx'
            _log.warning(f'No filename provided, output will be written to {filename}')

    gpx = gpxpy.gpx.GPX()
    for co in crag_object_list:
        match co:
            case CragRoute():
                route_to_gpx(gpx, co)
            case CragNode():
                if node_expand_children:
                    raise NotImplementedError
            case CragList():
                for cr in co.routes:
                    route_to_gpx(gpx, cr)

    with open(filename, 'w') as file:
        file.write(gpx.to_xml())
        _log.info(f'GPX file written to {filename}')


def route_to_gpx(gpx: gpxpy.gpx.GPX, cr: CragRoute):
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(
        latitude=cr.location[0], longitude=cr.location[1],
        name=cr.route_info['Name'] + ' - ' + cr.route_info["Grade"] + " | " + cr.route_info["Quality"],
        description='\n'.join([
            f'Grade: {cr.route_info["Grade"]}, Quality: {cr.route_info["Quality"]}',
            cr.route_info['Description']
        ]),
        symbol='Climbing'
    ))
    return 