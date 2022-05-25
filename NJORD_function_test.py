import os

import numpy as np
import pandas as pd

# unit = "weight"
# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

os.makedirs(path_output, exist_ok=True)
# nations_list = os.listdir(path_input + "\\Export\\")

# period = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
#             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
#             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
#             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
#             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]

# Generic functions for both weight and price calculations, name_cleanup,


def name_clean_up(nation_list):  # NOT USED!!!
    # Clean up the names of nations from the raw database and return a list of countries
    # print(nation_list)
    nation_list = [sub.replace("Bolivia__Plurinational_State_of", "Bolivia") for sub in nation_list]
    nation_list = [sub.replace("Congo__Democratic_Republic_of", "Democratic Republic of the Congo") for sub in nation_list]
    nation_list = [sub.replace("Côte_d'Ivoire", "Côte dIvoire") for sub in nation_list]
    nation_list = [sub.replace("Falkland_Islands_(Malvinas)", "Falkland Islands") for sub in nation_list]
    nation_list = [sub.replace("Hong_Kong__China", "Hong Kong") for sub in nation_list]
    nation_list = [sub.replace("Iran__Islamic_Republic_of", "Iran") for sub in nation_list]
    nation_list = [sub.replace("Korea__Democratic_People's_Republic_of", "North_Korea") for sub in nation_list]
    nation_list = [sub.replace("Korea__Republic_of", "South Korea") for sub in nation_list]
    nation_list = [sub.replace("Lao_People's_Democratic_Republic", "Laos") for sub in nation_list]
    nation_list = [sub.replace("Libya__State_of", "Libya") for sub in nation_list]
    nation_list = [sub.replace("Macedonia__North", "Macedonia") for sub in nation_list]
    nation_list = [sub.replace("Micronesia__Federated_States_of", "Micronesia") for sub in nation_list]
    nation_list = [sub.replace("Moldova__State_of", "Moldova") for sub in nation_list]
    nation_list = [sub.replace("Palestine__State_of", "Palestine") for sub in nation_list]
    nation_list = [sub.replace("Russian_Federation", "Russia") for sub in nation_list]
    nation_list = [sub.replace("Syrian_Arab_Republic", "Syria") for sub in nation_list]
    nation_list = [sub.replace("Taipei__Chinese", "Taiwan") for sub in nation_list]
    nation_list = [sub.replace("Tanzania__United_Republic_of", "Tanzania") for sub in nation_list]
    nation_list = [sub.replace("Venezuela__United_Republic_of", "Venezuela") for sub in nation_list]
    nation_list = [sub.replace("Viet_Nam", "Vietnam") for sub in nation_list]
    # Add a way to handle Sudan

    nation_list = [name.split(".") for name in nation_list]
    nation_list = [name[0] for name in nation_list]
    for name in nation_list:
        if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
            nation_list.remove(name)
    nation_list = [name.replace("_", " ") for name in nation_list]
    # print(nation_list)
    return nation_list


def name_cleanup(name, year):
    name = name.replace("_", " ")
    if name == "Bolivia, Plurinational State of":
        name = "Bolivia"
    if name == "Congo, Democratic Republic of the":
        name = "Democratic Republic of the Congo"
    if name == "Côte d'Ivoire":
        name = "Côte dIvoire"
    if name == "Falkland Islands Malvinas":
        name = "Falkland Islands"
    if name == "Hong Kong, China":
        name = "Hong Kong"
    if name == "Iran, Islamic Republic of":
        name = "Iran"
    if name == "Korea, Democratic People's Republic of":
        name = "North Korea"
    if name == "Korea, Republic of":
        name = "South Korea"
    if name == "Lao People's Democratic Republic":
        name = "Laos"
    if name == "Libya, State of":
        name = "Libya"
    if name == "Macedonia, North":
        name = "Macedonia"
    if name == "Micronesia, Federated States of":
        name = "Micronesia"
    if name == "Moldova, Republic of":
        name = "Moldova"
    if name == "Palestine, State of":
        name = "Palestine"
    if name == "Russian Federation":
        name = "Russia"
    if name == "Syrian Arab Republic":
        name = "Syria"
    if name == "Taipei, Chinese":
        name = "Taiwan"
    if name == "Tanzania, United Republic of":
        name = "Tanzania"
    if name == "Venezuela, Bolivarian Republic of":
        name = "Venezuela"
    if name == "Viet Nam":
        name = "Vietnam"
    if int(year) <= 2016 and "before" in name:
        # print("\n\nit is Sudan before, so I change name for the reference\n\n", name)
        name = "Sudan"
    return name


def manufacturing(nation, year, manufacturing_df):  # Extract the manufacturing for a nation in a specific year
    # print(manufacturing_df)
    # year = year.split("-")
    # year = year[0]
    if nation in manufacturing_df.index.values:
        if year == "2009":
            manufacturing_value = manufacturing_df[year][nation]
        else:
            manufacturing_value = manufacturing_df[year][nation]/4
    else:
        manufacturing_value = 0
    return manufacturing_value
# print(manufacturing(test, period))


def imports_or_export_in_period(dataset, country, year, export_import, value_or_quantity):
    data = dataset.loc[dataset["Reporting Country"] == country]
    datatest = data.loc[data["period"] == year]
    trade_data = datatest[export_import + value_or_quantity]
    trade_data = trade_data.set_axis(datatest["Partner Country"])
    return trade_data


def create_mirror_data(data, country, year, import_export, value_or_quantity):
    data = data.loc[data["Partner Country"] == country]
    data = data.loc[data["period"] == year]
    mirror_data = data[import_export + value_or_quantity]
    mirror_data = mirror_data.set_axis(data["Reporting Country"])
    return mirror_data


def combine_reported_and_mirror(reported, mirror):
    merged = reported.combine_first(mirror).fillna(0)
    return merged


def calc_percentage_import_or_export(nations_within, imp_or_exp):
    if "World" in nations_within:
        sum_trade = imp_or_exp.drop(["World"]).to_numpy().sum()
    else:
        sum_trade = imp_or_exp.to_numpy().sum()
    percentage_trade = []
    for item in imp_or_exp.index:
        # print(item)
        if item == "DataType":
            continue
        if sum_trade == 0:
            percentage_trade.append(0)
            continue
        if item == "World":
            percentage_trade.append(0)
            continue
        else:
            value = (imp_or_exp.loc[item] / sum_trade)  # percentage for each country
            percentage_trade.append(value)
    return percentage_trade, sum_trade


def calc_PV_factor(year, pv_share_unit, nations_within, percentage, import_export):
    pv_share_unit_list = pv_share_unit.index.values
    cont = 0
    pv_factor = 0
    if import_export == "Import":
        for nation in nations_within:
            # print(nation)
            if nation == "DataType":
                continue
            if nation in pv_share_unit_list:
                single_value = pv_share_unit[year][nation] * percentage[cont]
            else:
                single_value = pv_share_unit[year]["RoW"] * percentage[cont]
            pv_factor += single_value
            cont = cont + 1
    if import_export == "Export":  # Why is this different?
        for nation in nations_within:
            if nation == "DataType":
                continue
            single_value = pv_share_unit[year]["RoW"] * percentage[cont]
            pv_factor += single_value
    return pv_factor, pv_share_unit


def add_quarter(year, month):
    if int(month) <= 3:
        quarter = "-Q1"
    elif int(month) <= 6:
        quarter = "-Q2"
    elif int(month) <= 9:
        quarter = "-Q3"
    else:
        quarter = "-Q4"
    return year + quarter


def add_time_shift(months_shift, year, month):
    if month+months_shift > 12:
        month = months_shift-(12-month)
        year = year+1
    else:
        month = month+months_shift
    if month < 10:
        month = f"0{str(month)}"
    return str(year), str(month)


def create_quarterly_data(data):
    for name in data.columns:
        if "NJORD" in name:
            if int(name[-2:]) <= 3:
                temp_name = name[:-2]+"-Q1"
            elif 3 < int(name[-2:]) <= 6:
                temp_name = name[:-2]+"-Q2"
            elif 6 < int(name[-2:]) <= 9:
                temp_name = name[:-2]+"-Q3"
            else:
                temp_name = name[:-2]+"-Q4"
            if temp_name in data.columns:
                data[temp_name] += data[name]
            else:
                data[temp_name] = data[name]
    return data


def direct_or_mirror(data, unit, import_export, year, name):  # Do not need to check direct or mirror data, rewritten in ...
    # print(data+import_export+"\\"+name+".xlsx")
    # print(data)
    data = pd.read_excel(data+import_export+"\\"+name+".xlsx", index_col=0, na_values=['NA'])  # Needs to be changed now.
    data = data.fillna(0)  # filling empty spaces with 0
    data = data.replace(to_replace="No Quantity", value=0)  # replacing no quantity with 0
    source = []
    d_count = 0
    m_count = 0
    if unit == "Price":
        add1 = "value in "
        word1 = "Imported "
        word2 = "Exported "
    else:
        add2 = ""
        add1 = ""
        word1 = ""
        word2 = ""
    time_window = [word1+add1+str(year)]
    if import_export == "Export":
        time_window = [word2+add1+str(year)]
    data_period = data[time_window]
    # print(data_period)
    nations_within = data_period.index.values
    # print(nations_within)
    for letter in data_period.loc["DataType"]:
        source.append(letter)
        if letter == "D":
            d_count += 1
        else:
            m_count += 1
    t = True
    while t is True:
        if d_count == 4:
            source_data = "D"
            t = False
            continue
        if m_count == 4:
            source_data = "M"
            t = False
            continue
        if m_count < d_count:
            source_data = "D*"
            t = False
            continue
        if m_count > d_count:
            source_data = "M*"
            t = False
        if m_count == d_count:
            source_data = "M*"
            t = False
            continue
    return source_data, data_period, time_window, nations_within


# Functions for combined model


#def decide_ref(ref, name, year):
#    if ref[PVPS][name] == 0: #Check if there is data from PVPS, if there is use it as ref value else other, then IRENA, then No Ref.
#        ref_value = ref[other][name]
#        source = "Other"
#        if ref[other][name] == 0:
#            ref_value = ref[Irena][name]
#            source = "Irena"
#            if ref[Irena][name] == 0:
#                ref_value = 0
#                source = "No Ref"
#    else:
#        ref_value = ref[PVPS][name]
#        source = "PVPS"
#    combined_MF.at[name, "Ref " + str(2009)] = ref_value
#    combined_MF.at[name, "Source " + str(2009)] = source
#    combined_MF.at[name, "IRENA " + str(2009)] = reference_data_year[Irena][name]
#    combined_MF.at[name, "IRENA s " + str(2009)] = reference_data_year[str(2009) + " - IRENA s"][name]
#    combined_MF.at[name, "PVPS " + str(2009)] = reference_data_year[PVPS][name]
#    combined_MF.at[name, "Other " + str(2009)] = reference_data_year[other][name]


def extract_one_country(country):
    data = pd.read_csv("ITC_yearly_data_HS_6.csv")
    country_data = data.loc[(data["Reporting Country"] == country)]
    country_data = country_data.loc[(country_data["period"] == 2012)]
    country_data_import = country_data["exportValue"]
    # print(country_data_import)
    return country_data

# country = "Sweden"
# extract_one_country(country)


def acc_year(data):
    for name in data.columns:
        if "NJORD" in name:
            if "Q" not in name:
                temp_name = name[:-2]
                if temp_name in data.columns:
                    data[temp_name] += data[name]
                else:
                    data[temp_name] = data[name]
    return data

def remove_large_exporters(exports):
    large_exporters = ["China", "Korea, Republic of", "Taipei, Chinese", "Malaysia", "India", "Indonesia"]
    for country in large_exporters:
        if country in exports.index:
            # print(exports.index)
            exports = exports.drop(country)
            # print(exports)
    return exports


# test1 = weight(nations_list, path_output)
# test1.to_excel(path_output+"test123.xlsx")
# os.makedirs(path_output, exist_ok=True)
# nations_list = os.listdir(path_input + "\\Export\\")
# test1, test2 = price(path_input, period)
# test1.to_excel(path_output+"test2.xlsx")
# test_price1, test_price2 = price(nations_list, period)
# test2.to_excel(path_output+"vadihelafriden.xlsx")

