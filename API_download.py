import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
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
# print(token_test)

def access_yearly_data(token):
    url = "https://www.trademap.org/api/data/yearly"
    header = CaseInsensitiveDict() # {"Authorization": "Bearer"+token["access_token"]}
    header["accept"] = "application/json"
    header["Authorization"] = "Bearer "+token["access_token"]
    data = {"product_cd": "854140", "years": "2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020", "hs_level": "6"}
    result = requests.post(url,  headers=header, data=data)
    print(result.json())
    return result

test = access_yearly_data(token_test)


def get_countries():
    url = "https://www.trademap.org/api/common/countries"
    countries = requests.get(url, verify=False)
    print(countries.json())
    return countries.json()



