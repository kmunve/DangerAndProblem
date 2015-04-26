# -*- coding: utf-8 -*-
__author__ = 'raek'


import requests
import datetime
import AvalancheDanger as AD
from fEncoding import *

def get_warnings_as_json(region_id, start_date, end_date):
    '''
    Selects warnings and returns the json structurd result as given on the api.

    :param region_id:   [int]       RegionID as given in the forecast api [1-99] or in regObs [101-199]
    :param start_date:  [string]    date as yyyy-mm-dd
    :param end_date:    [string]    date as yyyy-mm-dd
    :return warnings:   [string]    String as json

    http://api01.nve.no/hydrology/forecast/avalanche/v2.0.1/api/AvalancheWarningByRegion/Detail/10/1/2013-01-10/2013-01-20
    '''

    if region_id > 100:
        region_id = region_id - 100

    print"Getting AvalancheWarnings for {0} from {1} til {2}".format(region_id, start_date, end_date)

    url = "http://api01.nve.no/hydrology/forecast/avalanche/v2.0.1/api/AvalancheWarningByRegion/Detail/{0}/1/{1}/{2}"\
        .format(region_id, start_date, end_date)
    warnings = requests.get(url).json()

    print(".. {} warnings found.".format(len(warnings)))

    return warnings

def get_warnings(region_id, start_date, end_date):
    '''
    Selects warnings and returns a list of AvalancheDangerObsjecs

    :param region_id:   [int]       RegionID as given in the forecast api [1-99] or in regObs [101-199]
    :param start_date:  [string]    date as yyyy-mm-dd
    :param end_date:    [string]    date as yyyy-mm-dd

    :return avalanche_danger_list: List of AvalancheDanger objects
    '''

    warnings = get_warnings_as_json(region_id,start_date, end_date)
    avalanche_danger_list = []

    for w in warnings:
        __region_id = int(w['RegionId'])
        __region_name = remove_norwegian_letters(w['RegionName'])
        __date = datetime.datetime.strptime(w['ValidFrom'][0:10], '%Y-%m-%d').date()
        __danger_level = int(w['DangerLevel'])
        __danger_level_name = remove_norwegian_letters(w['DangerLevelName'])

        __danger = AD.AvalancheDanger(__region_id, __region_name, 'Forecast API', __date, __danger_level, __danger_level_name)
        avalanche_danger_list.append(__danger)

    return avalanche_danger_list

def get_valid_regids(region_id, start_date, end_date):
    '''
    Method looks up all forecasts for a region and selects and returns the RegIDs used in regObs. Thus, the list of
    RegIDs are for published forcastes.

    :param region_id:   [int]       RegionID as given in the forecast api [1-99] or in regObs [101-199]
    :param start_date:  [string]    date as yyyy-mm-dd
    :param end_date:    [string]    date as yyyy-mm-dd
    :return:
    '''

    warnings = get_warnings_as_json(region_id, start_date, end_date)
    valid_regids = {}

    for w in warnings:
        dangerLevel = int(w["DangerLevel"])
        if dangerLevel > 0:
            valid_regids[w["RegId"]] = w["ValidFrom"]

    return valid_regids

if __name__ == "__main__":

    # get data for bardu (112) and tamok (129)
    warnings = get_warnings(129, "2014-12-01", "2015-06-01")
    # p = get_valid_regids(10, "2013-03-01", "2013-03-09")


    a = 1