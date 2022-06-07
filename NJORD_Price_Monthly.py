import numpy as np
import pandas as pd
import os
import NJORD_function_test
import Validation_functions

# This script calculates the installed capacity for the NJORD price model

path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data

os.makedirs(path_output, exist_ok=True)


# Functions only used in Price calculations
def price(raw_data):  # Main function calculating the price model.
    unit = "Price"
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
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
    exports_period_quarter = pd.Series()
    imports_period_quarter = pd.Series()

    # Main loop, might be able to be more effective. Takes a couple of minutes to run.
    for name in nation_list:
        print(name)
        i = 0
        for period in periods:
            monthly_data = raw_data.loc[raw_data["period"] == period]
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2009":
                continue
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
            # if i < 3:
            #    if i == 0:
            #        exports_period_quarter = exports_period
            #        # print(exports_period_quarter)
            #        imports_period_quarter = imports_period
            #    else:
            #        exports_period_quarter = exports_period_quarter.add(exports_period, fill_value=0)
            #        # print(exports_period_quarter)
            #        imports_period_quarter = imports_period_quarter.add(imports_period, fill_value=0)
            #    i += 1
            #    if i <= 2:
            #        continue
            # i = 0
            # exports_period = exports_period_quarter
            # imports_period = imports_period_quarter
            if "World" in imports_period:
                imports_period = imports_period.drop(labels="World")
            if "World" in exports_period:
                exports_period = exports_period.drop(labels="World")
            # exports_period_quarter = pd.DataFrame()
            # imports_period_quarter = pd.DataFrame()
            # print(imports_period_quarter)
            exports_period = NJORD_function_test.remove_large_exporters(exports_period)

            # Get a list of all the nations in imports and exports for the specific country and year.
            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values
            # Calculate each partner country's part of trade and sum the reporting country's trade.
            percentage_imp, sum_imports = NJORD_function_test.calc_percentage_import_or_export(nations_within_imp,
                                                                                               imports_period)
            # Add a check for export to large exporter, and remove them.
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
                installed_capacity = ((net_trade / PV_market_price) / 10 ** 6) + manufacturing_value  # /4 # on manufacturing value, check if it should be removed?
                installed_capacity_MF = ((net_trade / (PV_market_price * market_factor)) / 10 ** 6)# + manufacturing_value
            name = NJORD_function_test.name_cleanup(name, year)
            if name in reference.index.values:
                output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(year), month, name,
                                                                                installed_capacity,
                                                                                installed_capacity_MF,
                                                                                output_P_each_year,
                                                                                output_P_MF_each_year)
    # output_P_each_year = NJORD_function_test.create_quarterly_data(output_P_each_year)
    # output_P_MF_each_year = NJORD_function_test.create_quarterly_data(output_P_MF_each_year)
    # output_P_each_year = NJORD_function_test.acc_year(output_P_each_year)
    # output_P_MF_each_year = NJORD_function_test.acc_year(output_P_MF_each_year)
    return output_P_MF_each_year.sort_index(), output_P_each_year.sort_index()


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
    if 10 < prel_MS <= 100:
        market_factor = all_market_factors["10-100MW"]["Factor"]
    if prel_MS > 100:
        market_factor = all_market_factors[">100 MW"]["Factor"]
    return market_factor


def create_output_price(reference, year, month, name, installed_capacity, installed_capacity_MF, output_P_each_year,
                        output_P_MF_each_year):
    PVPS = year + " - PVPS - annual"
    other = year + " - Other - annual"
    Irena = year + " - IRENA - annual"
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
    year, month = NJORD_function_test.add_time_shift(3, int(year), int(month))
    ref_year = year
    year_output = str(year + month)
    # Creation of the excel sheet that will be returned.
    output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
    output_P_each_year.at[name, "Ref " + ref_year] = ref_value
    output_P_each_year.at[name, "Source " + ref_year] = source
    output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
    output_P_MF_each_year.at[name, "Ref " + ref_year] = ref_value
    output_P_MF_each_year.at[name, "Source " + ref_year] = source
    output_P_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    # output_P_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    output_P_each_year.at[name, "Other " + ref_year] = reference[other][name]
    output_P_MF_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    # output_P_MF_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_MF_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    output_P_MF_each_year.at[name, "Other " + ref_year] = reference[other][name]
    return output_P_each_year, output_P_MF_each_year


# raw_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
# output_P_each_year, output_P_MF_each_year = price(raw_data)
# output_P_each_year.to_excel(path_output + "Test2_month_Price_max_model_results.xlsx")
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
