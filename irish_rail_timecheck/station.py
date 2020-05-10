"""
Based on parsed input provide responses to station queries.
"""
import logging
from xml.parsers.expat import ExpatError
import requests
import defusedxml.minidom
from irish_rail_timecheck import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_station_code(station_name):
    """Get a train stations code based on its common name
    """
    response = requests.get(config.API_ENDPOINTS['station_list'])
    try:
        dom = defusedxml.minidom.parseString(response.text)
    except ExpatError:
        return 'No Station information available'

    stations = dom.getElementsByTagName("objStation")
    for station in stations:
        common_name = station.getElementsByTagName("StationDesc")[0].childNodes[0].data
        if station_name.lower() in common_name.lower():
            return station.getElementsByTagName("StationCode")[0].childNodes[0].data.strip()

    return 'No such station code found'


def next_train_to(station, destination):
    """ Return the next train to a given station
    """
    response = requests.get(config.API_ENDPOINTS['station_info'] + station)
    try:
        dom = defusedxml.minidom.parseString(response.text)
    except ExpatError:
        return 'No train information available'

    station_events = dom.getElementsByTagName("objStationData")

    for train_info in station_events:
        train_destination = train_info.getElementsByTagName("Destination")[0].childNodes[0].data
        if train_destination == destination:
            return "The next train to " + \
                    destination + " is " + \
                    train_info.getElementsByTagName("Expdepart")[0].childNodes[0].data

    return "No train to " + destination + " due in the next period"


if __name__ == '__main__':
    print(next_train_to(get_station_code('Cork'), "Mallow"))
