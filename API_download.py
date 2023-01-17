import warnings
import pandas as pd
import requests
# import certifi
import urllib3
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter(action='ignore', category=FutureWarning)

path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"

urllib3.disable_warnings(InsecureRequestWarning)

# print(certifi.where())


def import_access_token():
    url = "https://idserv.marketanalysis.intracen.org/connect/token"
    username = "njord@becquerelsweden.se"
    password = "tull854140"
    data = {"client_id": "TradeMap", "grant_type": "password", "scope": "TradeMap.Data.API", "username": username,
            "password": password}
    token = requests.post(url, data=data)
    return token.json()
# token_test = import_access_token()
# print(token_test)


def access_yearly_data(token, years, level):  # country_cd,
    url = "https://www.trademap.org/api/data/yearly"
    header = {"Authorization": "Bearer " + token["access_token"]}
    params = {"product_cd": "854140", "years": years, "hs_level": level}  # "country_cd": country_cd,
    result = requests.get(url, headers=header, params=params, verify=False)
    return result.json()

# test = access_yearly_data(token_test, '2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021', '6')


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


def access_monthly_data(token, year, month, level):
    url = "https://www.trademap.org/api/data/monthly"
    header = {"Authorization": "Bearer " + token["access_token"]}
    # change the value after product_cd to change which code is downloaded. As this is written, only 854140 available.
    params = {"product_cd": "854140", "months": str(year)+str(month), "hs_level": level}  # "country_cd": country_cd,
    result = requests.get(url, headers=header, params=params, verify=False)  # This is the call to the server side!
    return result.json()


def download_yearly_data():
    # Download the data from ITC using the API
    access_token = import_access_token()
    country_list = pd.DataFrame(get_countries()).set_index(0)
    # Has to go through yearly data.
    years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
    yearly_data_all = pd.DataFrame()
    for year in years:
        # Important to keep reporterCd, partnerCd, exportValue, importValue
        yearly_data = access_yearly_data(access_token, year, '10')
        yearly_data_all = yearly_data_all.append(yearly_data, ignore_index=True)
    yearly_data_all.rename(columns={'reporterCd': 'Reporting Country', "partnerCd": 'Partner Country'}, inplace=True)
    for code in country_list.index:  # Rename the codes to country names for easier understanding in the document.
        yearly_data_all['Reporting Country'].replace(code, country_list.loc[code][1], inplace=True)
        yearly_data_all['Partner Country'].replace(code, country_list.loc[code][1], inplace=True)
    return yearly_data_all


# yearly_data_all = download_yearly_data()
# yearly_data_all.to_csv(path_output+"ITC_yearly_data_HS_6_854140.csv")


def download_monthly_data():
    # Download the data from ITC using the API
    access_token = import_access_token()
    country_list = pd.DataFrame(get_countries()).set_index(0)
    # Has to go through yearly data.
    years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021',
             '2022'] # Change to the years one is interested here, now 2009-2022
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']  # Signifying the months
    monthly_data_all = pd.DataFrame()
    for year in years:
        for month in months:
            # Important to keep reporterCd, partnerCd, exportValue, importValue
            monthly_data = access_monthly_data(access_token, year, month, '10')  # Downloads a month worth of data
            monthly_data_all = monthly_data_all.append(monthly_data, ignore_index=True)  # Store all downloaded data in 1 file
    monthly_data_all.rename(columns={'reporterCd': 'Reporting Country', "partnerCd": 'Partner Country'}, inplace=True)
    for code in country_list.index:
        # Changes the country code to the country name for readability
        monthly_data_all['Reporting Country'].replace(code, country_list.loc[code][1], inplace=True)
        monthly_data_all['Partner Country'].replace(code, country_list.loc[code][1], inplace=True)
    return monthly_data_all


monthly = download_monthly_data()
monthly.to_csv(path_output+"ITC_Monthly_data_HS_10.csv")


def download_quantity_units():
    url = "https://www.trademap.org/api/common/quantity-units"
    quantity_units = requests.get(url, verify=False)
    quantity_units = pd.DataFrame(quantity_units.json())
    return quantity_units

# quantity_units = download_quantity_units()
# quantity_units.to_excel(path_output+"ITC_Quantity_units.xlsx")


def download_NTL_codes():  # Way too big, don't use for all countries.
    url = "https://www.trademap.org/api/common/products-ntl"
    params = {"product_cd": "854140"}
    NTL = requests.get(url, params=params, verify=False)
    NTL = pd.DataFrame(NTL.json())
    # Rename the codes to country names
    country_list = pd.DataFrame(get_countries()).set_index(0)
    for code in country_list.index:
        NTL['countryCd'].replace(code, country_list.loc[code][1], inplace=True)
    return NTL


# NTL_codes = download_NTL_codes()
# NTL_codes.to_csv("NTL_codes_850790.csv")
