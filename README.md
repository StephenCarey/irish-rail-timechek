# Irish Rail time check

![Irish rail timecheck app](https://github.com/StephenCarey/irish-rail-timecheck/workflows/Irish%20rail%20timecheck%20app/badge.svg)

A simple Alex app for polling and providing train information based on the Irish rail API.

This app consists of a lambda function for handling Alex calls and a helper module which
 talks to the Irish Rail API.

## Build

This project uses make as its build tool and requires the following:

* make
* Python 3 (created with 3.7 but compatiable with earlier)
* pip

## Utils

This contains helper scripts.

`create_station_map.py` - Create a dictionary of common station name and station code.
 This is to reduce the need for API calls for static information. It will also produce
 a list of the common station names. This can be used for validation.
