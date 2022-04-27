import ssl
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import json
from requests.structures import CaseInsensitiveDict

urllib3.disable_warnings(InsecureRequestWarning)
def import_access_token():
    url = "https://idserv.marketanalysis.intracen.org/connect/token"
    username = "njord@becquerelsweden.se"
    password = "tull854140"
    data = {"client_id": "TradeMap", "grant_type": "password", "scope": "TradeMap.Data.API", "username": username, "password": password}
    token = requests.post(url, data=data)
    return token.json()


token_test = import_access_token()


def access_yearly_data(token, country_cd, years, level):
    url = "https://www.trademap.org/api/data/yearly"
    header = {"Authorization": "Bearer "+token["access_token"]}
    # header["accept"] = "application/json"
    # header["Authorization"] = "Bearer ".format(token["access_token"])
    params = {"country_cd": country_cd, "product_cd": "854140", "years": years, "hs_level": level}
    result = requests.get(url,  headers=header, params=params)# context=ssl.create_default_context(cafile=certifi.where()))  # , verify=False)
    print(result.json())
    return result.json()

test = access_yearly_data(token_test, '004', '2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021', '6')

def get_countries():
    url = "https://www.trademap.org/api/common/countries"
    countries = requests.get(url, verify=False)
    countries = countries.json()
    country_list = []
    for i in range(len(countries)):
        country_cd = countries[i]['countryCd']
        country = countries[i]['labelEn']
        country_list.append([country_cd, country])
    return country_list


hahe = get_countries()
