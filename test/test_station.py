import pytest
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


@pytest.mark.parametrize('station_name, test_data, expected', test_cases)
def test_next_train_to(station_name, test_data, expected):
    output = station.next_train_to(station_name, test_data)
    assert output == expected
