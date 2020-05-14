import pytest
import requests_mock
from pathlib import Path
from irish_rail_timecheck import station

path = Path(__file__).parent

with open(path / 'test_data/stationInfoCork.xml', "r") as train_data:
    cork_departure_list = train_data.read()

with open(path / 'test_data/stationInfoMidleton.xml', "r") as train_data:
    midleton_departure_list = train_data.read()

with open(path / 'test_data/stationInfoCobh.xml', "r") as train_data:
    cobh_departure_list = train_data.read()

with open(path / 'test_data/stationInfoBelfast.xml', "r") as train_data:
    belfast_departure_list = train_data.read()

with open(path / 'test_data/stationList.xml', "r") as station_data:
    station_list = station_data.read()

get_station_code_test_cases = [
    ("Drogheda", "DGHDA"),
    ("Cork", "CORK"),
    ("thomastown", "THTWN"),
    ("Connolly", "CNLLY")
]

get_station_code_exeption_test_cases = [
    ('Connnly', 'Station Connnly not found')
]

next_train_test_cases = [
    ("Cork", "Cobh", "COBH", cork_departure_list, cobh_departure_list,"The next train to Cobh is 09:00"),
    ("Cork", "Midleton", "MDLTN", cork_departure_list, midleton_departure_list, "The next train to Midleton is 09:15"),
    ("Cork", "Belfast", "BFSTC", cork_departure_list, belfast_departure_list, "No train to Belfast due in the next period"),
    ("Cork", "coob", "", '', '', "Station coob not found"),
    ("Cork", "Cobh", 'COBH', '', '', "No station information available")
]

station_info_test_cases = [
    ("Cork", cork_departure_list, "P289")
]


@pytest.mark.parametrize('common_station_name, expected', get_station_code_test_cases)
def test_get_station_code(common_station_name, expected):
    output = station.get_station_code(common_station_name)
    assert output == expected


@pytest.mark.parametrize('station_name, expected', get_station_code_exeption_test_cases)
def test_get_station_code_exeption(station_name, expected):
    with pytest.raises(Exception) as execinfo:
        station.get_station_code(station_name)
    
    assert str(execinfo.value) == expected

@pytest.mark.parametrize('depart_station, arrive_station, station_code, departure_data, destination_data, expected', next_train_test_cases)
def test_next_train_to(depart_station, arrive_station, station_code, departure_data, destination_data, expected, requests_mock):
    requests_mock.get('/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=' + depart_station, text=departure_data)
    requests_mock.get('/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=' + station_code, text=destination_data)

    output = station.next_train_to(depart_station, arrive_station)
    assert output == expected


def test_get_station_info(requests_mock):
    requests_mock.get('/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=Cork', text=cork_departure_list)
    output = station.get_station_info('Cork')
    assert 'D278' in output
    assert output['D278'] == "10:15"
