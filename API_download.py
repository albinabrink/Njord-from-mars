import ssl
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


def access_yearly_data(token):
    url = "https://www.trademap.org/api/data/yearly"
    header = {"Authorization": "Bearer "+token["access_token"]}
    # header["accept"] = "application/json"
    # header["Authorization"] = "Bearer ".format(token["access_token"])
    params = {"country_cd": "004", "product_cd": "854140", "years": "2019", "hs_level": "6"}
    result = requests.get(url,  headers=header, params=params)# context=ssl.create_default_context(cafile=certifi.where()))  # , verify=False)
    print(result.text)
    return result

test = access_yearly_data(token_test)


def get_countries():
    url = "https://www.trademap.org/api/common/countries"
    countries = requests.get(url, verify=False)
    print(countries.json())
    return countries.json()


# hahe = get_countries()
