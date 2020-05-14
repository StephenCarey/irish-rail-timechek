#!/usr/bin/env python3
"""
Build a local map of station codes so you do not need to call the API for this
static information
"""
from xml.parsers.expat import ExpatError
import json
import requests
import defusedxml.minidom


def build_map():
    """Get a train stations code based on its common name
    """
    response = requests.get('http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML')
    try:
        dom = defusedxml.minidom.parseString(response.text)
    except ExpatError:
        raise ValueError('No station information available')

    stations = dom.getElementsByTagName("objStation")
    station_map = {}

    for station_tag in stations:
        common_name = station_tag.getElementsByTagName("StationDesc")[0].childNodes[0].data
        station_map[common_name.lower()] = \
            station_tag.getElementsByTagName("StationCode")[0].childNodes[0].data.strip()

        if ' ' in common_name:
            abbreviations = common_name.split()
            for phrase in abbreviations:
                station_map[phrase.lower()] = \
                    station_tag.getElementsByTagName("StationCode")[0].childNodes[0].data.strip()

    return station_map


if __name__ == "__main__":
    stations_dict = build_map()
    json = json.dumps(stations_dict, indent=4, sort_keys=True)

    f = open("station_map.json", "w")
    f.write(json)
    f.close()
