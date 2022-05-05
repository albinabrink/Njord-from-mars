import numpy as np
import pandas as pd
import os
import NJORD_function_test
import API_download

#### This script calculates the installed capacity
import Validation_functions

unit = "Price"

### change path also in lines  453 -454####
path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Price\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

######

os.makedirs(path_output, exist_ok=True)
# nation_list = os.listdir(path_input + "\\Export\\")
periods = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]


# Functions only used in Price calculations
def price(raw_data, periods):  # Main function calculating the price model.
    unit = "Price"
    # nations_list = os.listdir(input + "\\Export\\")
    reference = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
    pv_share_unit = pd.read_excel("Share_in_PV_" + unit + ".xlsx", index_col=0)
    change1 = pd.read_excel("PVxchange.xlsx", index_col=0)
    output_P_each_year = pd.DataFrame()
    output_P_MF_each_year = pd.DataFrame()
    Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
              "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
              "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
              "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands", "Norway", "Poland", "Portugal",
              "Romania", "Russian_Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
              "Ukraine", "United_Kingdom"]
    period = list(dict.fromkeys(raw_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = Validation_functions.check_missing_countries(raw_data, all_countries)
    nation_list = set(all_countries[1])-set(country_not_in_data)
    for year in period:
        if year == 2021:
            continue
        for name in nation_list:
            # if name == "Macao, China" or name == "Eswatini" or name == "Netherlands Antilles" or name == "Guinea-Bissau" or name == "Timor-Leste" or name == "Sudan (before 2012)":
            #    continue
            manufacturing_value = NJORD_function_test.manufacturing(name, str(year))
            # nations_within_imp = create_nations_within(raw_data, name, int(year), "import")
            # nations_within_exp = create_nations_within(raw_data, name, int(year), "export")
            imports_period = imports_or_export_in_period(raw_data, name, int(year), "import")
            exports_period = imports_or_export_in_period(raw_data, name, int(year), "export")
            # Handle missing data/mirror data
            exports_period_mirror = create_mirror_data(raw_data, name, int(year), "import")
            imports_period_mirror = create_mirror_data(raw_data, name, int(year), "export")
            imports_period = combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = combine_reported_and_mirror(exports_period, exports_period_mirror)

            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values

            percentage_imp, sum_imports = calc_percentage_import_or_export(nations_within_imp, imports_period)
            percentage_exp, sum_exports = calc_percentage_import_or_export(nations_within_exp, exports_period)
            # import_source, imports_period, time_window_import, nations_within_imp = NJORD_function_test.direct_or_mirror(inputs, unit, "Import", year_quarter, name)
            # export_source, exports_period, time_window_export, nations_within_exp = NJORD_function_test.direct_or_mirror(inputs, unit, "Export", year_quarter, name)
            #percentage_imp, percentage_exp, sum_imports, sum_exports = NJORD_function_test.calc_percentage_import_export(imports_period,
            #                                                                                         exports_period,
            #                                                                                         time_window_import,
            #                                                                                         time_window_export)
            PV_factor_imp, PV_share_unit = calc_PV_factor(str(year), pv_share_unit, nations_within_imp, percentage_imp, "Import")
            PV_factor_exp, PV_share_unit = calc_PV_factor(str(year), pv_share_unit, nations_within_exp, percentage_exp, "Export")

            if sum(percentage_imp) < 1:
                waste = 1-sum(percentage_imp)  # calc the wasted PV per year
                lack_PV = waste*PV_share_unit[str(year)]["RoW"]  # The lacking PV that comes from the waste
                PV_factor_imp += lack_PV  # Update PV_factor_imp

            net_trade = (sum_imports*PV_factor_imp)-(sum_exports*PV_factor_exp)*1000
            PV_market_price = calc_PV_market_price(nations_within_imp, change1, percentage_imp, str(year)+"-Q4", Europe)
            market_factor = prel_market_size(net_trade, change1, str(year))

            if PV_market_price == 0:
                installed_capacity = 0
                installed_capacity_MF = 0
            else:
                installed_capacity = ((net_trade/PV_market_price)/10**6)+manufacturing_value  # /4 on manufacturing value, check if should be removed?
                installed_capacity_MF = ((net_trade/(PV_market_price*market_factor))/10**6)+manufacturing_value
            name = NJORD_function_test.name_cleanup(name, year)
            # print(reference)
            if name in reference.index.values:
                output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(year)+"-Q4", str(year), name, installed_capacity, installed_capacity_MF, output_P_each_year, output_P_MF_each_year)
        print(year)
    return output_P_each_year, output_P_MF_each_year


def calc_PV_market_price(nations_within, change, percentage, year_quarter, Europe):
    cont = 0
    PV_market_price = 0
    change_list = change.index.values
    for item in nations_within:
        if item == "DataType":
            continue
        if item in change_list:
            single_value = change[year_quarter][item] * percentage[cont]  # value for each single nation
        else:
            if item in Europe:
                single_value = change[year_quarter]["EU"] * percentage[cont]  # value for each single nation
            else:
                single_value = change[year_quarter]["RoW"] * percentage[cont]

            # print(item, change[year_quarter]["RoW"], percentage[cont], year_quarter)

        PV_market_price = PV_market_price + single_value
        # print(PV_market_price,year,single_value,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        cont = cont + 1

    return PV_market_price


def prel_market_size(net_trade, change, year):
    # Preliminary Market size:
    prel_MS = (net_trade/change[year+"-Q4"]["RoW"])/10**6
    # print(prel_MS)
    all_market_factors = pd.read_excel("Market_size_factor.xlsx", index_col=0)

    # print(prel_MS,"prel")
    if prel_MS <= 1:
        market_factor = all_market_factors["0-1MW"]["Factor"]
    if 1 < prel_MS <= 5:
        market_factor = all_market_factors["1-5MW"]["Factor"]
    if 5 < prel_MS <= 10:
        market_factor = all_market_factors["5-10MW"]["Factor"]
    if 10 < prel_MS <= 100:
        market_factor = all_market_factors["10-100MW"]["Factor"]
    if prel_MS > 100:
        market_factor = all_market_factors[">100 MW"]["Factor"]
    return market_factor


def create_output_price(reference, year_quarter, year, name, installed_capacity, installed_capacity_MF, output_P_each_year, output_P_MF_each_year):
    PVPS = year + " - PVPS"
    other = year + " - Other"
    Irena = year + " - IRENA"
    if reference[PVPS][name] == 0:
        ref_value = reference[other][name]
        source = "Other"
        if reference[other][name] == 0:
            ref_value = reference[Irena][name]
            source = "Irena"
            if reference[Irena][name] == 0:
                ref_value = 0
                source = "No Ref"
    else:
        ref_value = reference[PVPS][name]
        source = "PVPS"

    if "Q4" in year_quarter:
        year_output = str(int(year) + 1) + "-Q1"
    if "Q1" in year_quarter:
        year_output = str(year) + "-Q2"
    if "Q2" in year_quarter:
        year_output = str(year) + "-Q3"
    if "Q3" in year_quarter:
        year_output = str(year) + "-Q4"

    output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
    output_P_each_year.at[name, "Ref " + year] = ref_value
    output_P_each_year.at[name, "Source " + year] = source
    output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
    output_P_MF_each_year.at[name, "Ref " + year] = ref_value
    output_P_MF_each_year.at[name, "Source " + year] = source
    output_P_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    output_P_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][name]
    output_P_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_P_each_year.at[name, "Other " + year] = reference[other][name]
    output_P_MF_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    output_P_MF_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][name]
    output_P_MF_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_P_MF_each_year.at[name, "Other " + year] = reference[other][name]
    return output_P_each_year, output_P_MF_each_year


def create_nations_within(dataset, country, year, export_import):  # Doesn't use this now
    nations_within = dataset.loc[country]
    partner_countries = []
    for row in range(len(nations_within)):
        if nations_within.iloc[row]["period"] == year:
            if nations_within.iloc[row][export_import+"Value"] != np.nan:
                partner_countries.append(nations_within.iloc[row]["Partner Country"])
    nations_within = list(dict.fromkeys(partner_countries))
    return nations_within


def imports_or_export_in_period(dataset, country, year, export_import):
    data = dataset.loc[dataset["Reporting Country"] == country]
    datatest = data.loc[data["period"] == year]
    trade_data = datatest[export_import+"Value"]
    trade_data = trade_data.set_axis(datatest["Partner Country"])
    # print(trade_datatest)
    # for row in range(len(data)):
    #    if data.iloc[row]["period"] == year:
    #        if not np.isnan([data.iloc[row][export_import+"Value"]]):
    #            trade_data = trade_data.append([data.iloc[row][export_import + "Value"]])
    #            countries_list = countries_list.append([data.iloc[row]["Partner Country"]])
    #        else:
    #            continue
    #if not countries_list.empty:
    #    trade_data = trade_data.set_axis(countries_list[0])
    #    trade_data.rename(columns={0: year}, inplace=True)
    # print(trade_data)
    return trade_data


def create_mirror_data(data, country, year, import_export):
    # mirror_data = pd.DataFrame()
    # countries_list = pd.DataFrame()
    data = data.loc[data["Partner Country"] == country]
    data = data.loc[data["period"] == year]
    mirror_data = data[import_export+"Value"]
    mirror_data = mirror_data.set_axis(data["Reporting Country"])
    # for row in range(len(data)):
    #    if data.iloc[row]["period"] == year:
    #        mirror_data = mirror_data.append([data.iloc[row][import_export+"Value"]])
    #        countries_list = countries_list.append([data.iloc[row].name])
    # if len(countries_list.index) > 0:
    #    mirror_data = mirror_data.set_axis(countries_list[0])
    # mirror_data.rename(columns={0: year}, inplace=True)
    # print(mirror_data)
    return mirror_data


def combine_reported_and_mirror(reported, mirror):
    # print(reported)
    # print(mirror)
    merged = reported.combine_first(mirror).fillna(0)
    # print(merged)
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
    # print(nations_within)
    # print(len(percentage))
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


periods = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]

raw_data = pd.read_csv("ITC_yearly_data_HS_6.csv")
output_P_each_year, output_P_MF_each_year = price(raw_data, periods)
output_P_each_year.to_excel(path_output+"Test_Price_max_model_results.xlsx")
# output_P_MF_each_year.to_excel(path_output+"Test_NJORD-Price_model_results.xlsx")





