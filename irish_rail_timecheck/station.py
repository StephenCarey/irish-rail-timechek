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
    station_code = config.station_code.get(station_name.lower(), 'not found')
    if station_code == 'not found':
        raise ValueError('Station ' + station_name + ' not found')
    return station_code


def next_train_to(station, destination):
    """ Return the next train to a given station
    """
    try:
        trains_from_departure = get_station_info(get_station_code(station))
        trains_from_destination = get_station_info(get_station_code(destination))
    except ValueError as message:
        return str(message)

    if len(trains_from_departure) == 0 or len(trains_from_destination) == 0:
        return "No station information available"

    for train_id in trains_from_departure:
        # A time of 00:00 signals the train in inbound rather than out.
        if train_id in trains_from_destination and trains_from_departure.get(train_id) != "00:00":
            return "The next train to " + \
                    destination + " is " + \
                    trains_from_departure.get(train_id)

    return "No train to " + destination + " due in the next period"


def get_station_info(station):
    """ Get trains for a given station
    """
    trains = {}
    response = requests.get(config.API_ENDPOINTS['station_info'] + station)
    try:
        dom = defusedxml.minidom.parseString(response.text)
    except ExpatError:
        return trains

    station_events = dom.getElementsByTagName("objStationData")

    for train_info in station_events:
        trains[train_info.getElementsByTagName("Traincode")[0].childNodes[0].data.strip()] \
            = train_info.getElementsByTagName("Expdepart")[0].childNodes[0].data

    return trains


if __name__ == '__main__':
    print(next_train_to(get_station_code('Cork'), "Mallow"))
