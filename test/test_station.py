import pytest
import requests_mock
from pathlib import Path
from irish_rail_timecheck import station

path = Path(__file__).parent / 'stationInfo.xml'
test_date = open(path, "r")
departure_list = test_date.read()

test_cases = [
    ("Cobh", departure_list, "21:00"),
    ("Tralee", departure_list, "20:55"),
    ("Belfast", departure_list, "No train due in the next period"),
    ("Cobh", '', "No train information available")
]


def test_get_station_info(requests_mock):
    requests_mock.get('/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=Cork', text=departure_list)
    output = station.get_station_info('Cork')
    assert len(output) != 0
    assert output == departure_list


@pytest.mark.parametrize('station_name, test_data, expected', test_cases)
def test_next_train_to(station_name, test_data, expected):
    output = station.next_train_to(station_name, test_data)
    assert output == expected
