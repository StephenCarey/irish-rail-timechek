"""
Based on parsed input provide responses to station queries.
"""
import xml.dom.minidom
from xml.parsers.expat import ExpatError


def next_train_to(station, departures):
    """ Return the next train to a given station
    """
    try:
        dom = xml.dom.minidom.parseString(departures)
    except ExpatError:
        return 'No train information available'

    station_events = dom.getElementsByTagName("objStationData")

    for train_info in station_events:
        destination = train_info.getElementsByTagName("Destination")[0].childNodes[0].data
        if destination == station:
            return train_info.getElementsByTagName("Expdepart")[0].childNodes[0].data

    return 'No train due in the next period'
