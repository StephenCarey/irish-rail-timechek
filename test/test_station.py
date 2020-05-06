import pytest
import requests_mock
from pathlib import Path
from irish_rail_timecheck import station

path = Path(__file__).parent

with open(path / 'stationInfo.xml', "r") as train_data:
    departure_list = train_data.read()

with open(path / 'stationList.xml', "r") as station_data:
    station_list = station_data.read()

get_station_code_test_cases = [
    ("Drogheda", station_list, "DGHDA"),
    ("Cork", station_list, "CORK"),
    ("thomastown", station_list, "THTWN"),
    ("Connolly", station_list, "CNLLY")
]

next_train_test_cases = [
    ("Cobh", departure_list, "21:00"),
    ("Tralee", departure_list, "20:55"),
    ("Belfast", departure_list, "No train due in the next period"),
    ("Cobh", '', "No train information available")
]

station_info_test_cases = [
    ("Cobh", departure_list, departure_list),
    ("Cobh", '', '')
]


@pytest.mark.parametrize('common_station_name, test_data, expected', get_station_code_test_cases)
def test_get_station_code(common_station_name, test_data, expected, requests_mock):
    requests_mock.get('/realtime/realtime.asmx/getAllStationsXML', text=test_data)
    output = station.get_station_code(common_station_name)
    assert output == expected


@pytest.mark.parametrize('station_name, test_data, expected', station_info_test_cases)
def test_get_station_info(station_name, test_data, expected, requests_mock):
    requests_mock.get('/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=' + station_name, text=test_data)
    output = station.get_station_info(station_name)
    assert output == expected


@pytest.mark.parametrize('station_name, test_data, expected', next_train_test_cases)
def test_next_train_to(station_name, test_data, expected):
    output = station.next_train_to(station_name, test_data)
    assert output == expected
