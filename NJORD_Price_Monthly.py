import numpy as np
import pandas as pd
import os
import NJORD_function_test
import Validation_functions

# This script calculates the installed capacity for the NJORD price model

path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data

os.makedirs(path_output, exist_ok=True)


# nation_list = os.listdir(path_input + "\\Export\\")
# periods = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
#             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
#             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
#             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
#             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]


# Functions only used in Price calculations
def price(raw_data):  # Main function calculating the price model.
    unit = "Price"
    reference = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    pv_share_unit = pd.read_excel("Share_in_PV_" + unit + ".xlsx", index_col=0)  # Read the PV_share from excel
    PVxchange_cost = pd.read_excel("PVxchange.xlsx", index_col=0)  # Read the cost of panels from big producers
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    output_P_each_year = pd.DataFrame()
    output_P_MF_each_year = pd.DataFrame()
    Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
              "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
              "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
              "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands", "Norway", "Poland", "Portugal",
              "Romania", "Russian_Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
              "Ukraine", "United_Kingdom"]
    # Extract the available periods in the data, and the countries that are in the data.
    periods = list(dict.fromkeys(raw_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = Validation_functions.check_missing_countries(raw_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    # Main loop, goes through each month and then each country in that month. Takes a couple of minutes to run.
    for period in periods:
        monthly_data = raw_data.loc[raw_data["period"] == period]
        print(period)
        month = str(period)[4:]
        year = str(period)[:4]
        if year == "2009":
            continue
        for name in nation_list:
            # Add months to quarters/years before you do the calculations.
            manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
            # Imports and exports a specific period for each specific country.
            imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period), "import",
                                                                             "Value")
            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period), "export",
                                                                             "Value")
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period), "import",
                                                                           "Value")
            imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period), "export",
                                                                           "Value")
            imports_period = NJORD_function_test.combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = NJORD_function_test.combine_reported_and_mirror(exports_period, exports_period_mirror)
            # Get a list of all the nations in imports and exports for the specific country and year.
            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values
            # Calculate each partner country's part if trade and sum the reporting country's trade.
            percentage_imp, sum_imports = NJORD_function_test.calc_percentage_import_or_export(nations_within_imp,
                                                                                               imports_period)
            percentage_exp, sum_exports = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp,
                                                                                               exports_period)
            # Calc PV_factor, used to determine the price of PV-modules.
            PV_factor_imp, PV_share_unit = NJORD_function_test.calc_PV_factor(str(year), pv_share_unit,
                                                                              nations_within_imp, percentage_imp,
                                                                              "Import")
            PV_factor_exp, PV_share_unit = NJORD_function_test.calc_PV_factor(str(year), pv_share_unit,
                                                                              nations_within_exp, percentage_exp,
                                                                              "Export")

            if sum(percentage_imp) < 1:
                waste = 1 - sum(percentage_imp)  # calc the wasted PV per year
                lack_PV = waste * PV_share_unit[str(year)]["RoW"]  # The lacking PV that comes from the waste
                PV_factor_imp += lack_PV  # Update PV_factor_imp
            # Insert subtraction of export to large producers
            net_trade = ((sum_imports * PV_factor_imp) - (sum_exports * PV_factor_exp)) * 1000
            PV_market_price = calc_PV_market_price(nations_within_imp, PVxchange_cost, percentage_imp, str(year), month,
                                                   Europe)
            market_factor = prel_market_size(net_trade, PVxchange_cost, str(year), month)

            if PV_market_price == 0:
                installed_capacity = 0
                installed_capacity_MF = 0
            else:
                installed_capacity = ((net_trade / PV_market_price) / 10 ** 6) + manufacturing_value  # /4 on manufacturing value, check if it should be removed?
                installed_capacity_MF = ((net_trade / (PV_market_price * market_factor)) / 10 ** 6) + manufacturing_value
            name = NJORD_function_test.name_cleanup(name, year)
            if name in reference.index.values:
                output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(year), month, name,
                                                                                installed_capacity,
                                                                                installed_capacity_MF,
                                                                                output_P_each_year,
                                                                                output_P_MF_each_year)
    output_P_each_year = NJORD_function_test.create_quarterly_data(output_P_each_year)
    output_P_MF_each_year = NJORD_function_test.create_quarterly_data(output_P_MF_each_year)
    output_P_each_year = NJORD_function_test.acc_year(output_P_each_year)
    output_P_MF_each_year = NJORD_function_test.acc_year(output_P_MF_each_year)
    return output_P_each_year.sort_index(), output_P_MF_each_year.sort_index()


def calc_PV_market_price(nations_within, change, percentage, year, month, Europe):
    cont = 0
    PV_market_price = 0
    change_list = change.index.values
    year_quarter = NJORD_function_test.add_quarter(year, month)
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
        cont = cont + 1
    return PV_market_price


def prel_market_size(net_trade, change, year, month):
    year_quarter = NJORD_function_test.add_quarter(year, month)
    # Preliminary Market size:
    prel_MS = (net_trade / change[year_quarter]["RoW"]) / 10 ** 6
    # print(prel_MS)
    all_market_factors = pd.read_excel("Market_size_factor.xlsx", index_col=0)
    market_factor = 0
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


def create_output_price(reference, year, month, name, installed_capacity, installed_capacity_MF, output_P_each_year,
                        output_P_MF_each_year):
    PVPS = year + " - PVPS"
    other = year + " - Other"
    Irena = year + " - IRENA"
    # year_quarter = add_quarter(year, month)
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
    # Add a timeshift in the month when it should be expected to be installed.
    ref_year = year
    year, month = NJORD_function_test.add_time_shift(3, int(year), int(month))
    year_output = str(year + month)
    output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
    output_P_each_year.at[name, "Ref " + ref_year] = ref_value
    output_P_each_year.at[name, "Source " + ref_year] = source
    output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
    output_P_MF_each_year.at[name, "Ref " + ref_year] = ref_value
    output_P_MF_each_year.at[name, "Source " + ref_year] = source
    output_P_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    output_P_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    output_P_each_year.at[name, "Other " + ref_year] = reference[other][name]
    output_P_MF_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    output_P_MF_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_MF_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    output_P_MF_each_year.at[name, "Other " + ref_year] = reference[other][name]
    return output_P_each_year, output_P_MF_each_year


raw_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
output_P_each_year, output_P_MF_each_year = price(raw_data)
output_P_each_year.to_excel(path_output + "Test_month_Price_max_model_results.xlsx")
# output_P_MF_each_year.to_excel(path_output+"Test_NJORD-Price_model_results.xlsx")


def create_nations_within(dataset, country, year, export_import):  # Doesn't use this now
    nations_within = dataset.loc[country]
    partner_countries = []
    for row in range(len(nations_within)):
        if nations_within.iloc[row]["period"] == year:
            if nations_within.iloc[row][export_import + "Value"] != np.nan:
                partner_countries.append(nations_within.iloc[row]["Partner Country"])
    nations_within = list(dict.fromkeys(partner_countries))
    return nations_within
