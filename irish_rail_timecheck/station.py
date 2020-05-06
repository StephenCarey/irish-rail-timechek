"""
Based on parsed input provide responses to station queries.
"""
from xml.parsers.expat import ExpatError
import requests
import defusedxml.minidom


def get_station_code(station_name):
    """Get a train stations code based on its common name
    """
    station_list_api = "http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML"
    response = requests.get(station_list_api)
    try:
        dom = defusedxml.minidom.parseString(response.text)
    except ExpatError:
        return 'No Station information available'

    stations = dom.getElementsByTagName("objStation")
    for station in stations:
        common_name = station.getElementsByTagName("StationDesc")[0].childNodes[0].data
        if station_name == common_name:
            return station.getElementsByTagName("StationCode")[0].childNodes[0].data

    return 'No suche station code found'


def get_station_info(station):
    """Poll the Irish rail API to get current station information
    """
    station_info_api = "http://api.irishrail.ie/" \
                       "realtime/realtime.asmx/getStationDataByCodeXML?StationCode="
    response = requests.get(station_info_api + station)
    return response.text


def next_train_to(station, departures):
    """ Return the next train to a given station
    """
    try:
        dom = defusedxml.minidom.parseString(departures)
    except ExpatError:
        return 'No train information available'

    station_events = dom.getElementsByTagName("objStationData")

    for train_info in station_events:
        destination = train_info.getElementsByTagName("Destination")[0].childNodes[0].data
        if destination == station:
            return train_info.getElementsByTagName("Expdepart")[0].childNodes[0].data

    return 'No train due in the next period'
