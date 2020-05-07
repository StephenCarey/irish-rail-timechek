"""
Common configuration.
"""
API_ENDPOINTS = {
    'station_list': 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML',
    'station_info': "http://api.irishrail.ie/realtime/realtime.asmx/"
                    "getStationDataByCodeXML?StationCode="
}
