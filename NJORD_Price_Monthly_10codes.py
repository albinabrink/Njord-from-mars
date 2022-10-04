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
    six_code_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
    unit = "Price"
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    # Needs to be changed?
    pv_share_unit = pd.read_excel("Share_in_PV_" + unit + ".xlsx", index_col=0)  # Read the PV_share from excel
    PVxchange_cost = pd.read_excel("PVxchange.xlsx", index_col=0)  # Read the cost of panels from big producers
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
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
    # Select all the countries in the data, could probably be made more effective.
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = NJORD_function_test.check_missing_countries(raw_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    # Main loop, might be able to be more effective. Takes a couple of minutes to run.
    # Should only have to be run once a year, when not in development.
    for name in nation_list:
        print(name)
        for period in periods:
            monthly_data = raw_data.loc[raw_data["period"] == period]
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2022" or year == "2009":
                continue
            manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
            # Picks out the relevant codes
            NTL_codes_rel = NTL_codes.loc[NTL_codes["countryCd"] == name]
            NTL_codes_rel = NTL_codes_rel.loc[NTL_codes_rel["PV?"] == "Yes"]
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # print(relevant_codes)
            # Only keep the codes of the month that will be relevant here.
            monthly_data = monthly_data[monthly_data["productCd"].isin(relevant_codes)]
            # Imports and exports a specific period for each specific country.
            imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period), "import",
                                                                             "Value")
            imports_period = imports_period.groupby(["Partner Country"]).sum()
            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period), "export",
                                                                             "Value")
            exports_period = exports_period.groupby(["Partner Country"]).sum()
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            monthly_data = raw_data.loc[raw_data["period"] == period]
            monthly_data = monthly_data.loc[monthly_data["Partner Country"] == name]
            NTL_codes_rel = pd.DataFrame()
            for country in monthly_data["Reporting Country"]:
                NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
                NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "Yes"]
                NTL_codes_rel = NTL_codes_rel.append(NTL_codes_country)
                # print(NTL_codes_rel)
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            monthly_data = monthly_data[monthly_data["productCd"].isin(relevant_codes)]

            exports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period), "import",
                                                                           "Value")
            exports_period_mirror = exports_period_mirror.groupby(["Reporting Country"]).sum()
            exports_period_mirror = exports_period_mirror[exports_period_mirror != 0]
            imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period), "export",
                                                                           "Value")
            imports_period_mirror = imports_period_mirror.groupby(["Reporting Country"]).sum()
            imports_period_mirror = imports_period_mirror[imports_period_mirror != 0]
            imports_period_ten = NJORD_function_test.combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period_ten = NJORD_function_test.combine_reported_and_mirror(exports_period, exports_period_mirror)

            # Calc PV_factor, used to determine the price of PV-modules.
            monthly_data = six_code_data[six_code_data["period"] == period]
            imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period),
                                                                                 "import",
                                                                                 "Value")
            imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period),
                                                                               "export",
                                                                               "Value")
            imports_period = NJORD_function_test.combine_reported_and_mirror(imports_period, imports_period_mirror)
            nations_within_imp = imports_period.index.values

            imports_period_six = NJORD_function_test.share_in_PV(str(year), name, imports_period, pv_share_unit, nations_within_imp, "Import", "six")

            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period),
                                                                                 "export", "Value")
            exports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period),
                                                                               "import", "Value")
            exports_period = NJORD_function_test.combine_reported_and_mirror(exports_period, exports_period_mirror)
            nations_within_exp = exports_period.index.values
            exports_period_six = NJORD_function_test.share_in_PV(str(year), name, exports_period, pv_share_unit,
                                                              nations_within_exp, "Export", "six")
            imports_period = NJORD_function_test.combine_reported_and_mirror(imports_period_ten, imports_period_six)
            exports_period = NJORD_function_test.combine_reported_and_mirror(exports_period_ten, exports_period_six)

            sum_imports = imports_period.sum()
            sum_exports = exports_period.sum()
            net_trade = (sum_imports - sum_exports) * 1000
            # net_trade = ((sum_imports * PV_factor_imp) - (sum_exports * PV_factor_exp)) * 1000

            # market_factor = prel_market_size(net_trade, PVxchange_cost, str(year), month)
            # year, month = NJORD_function_test.add_time_shift(0, int(year), int(month))  # Doesn't do anything right now
            PV_market_price = calc_PV_market_price(imports_period, PVxchange_cost, str(year), month,
                                                   Europe)
            if PV_market_price == 0:
                installed_capacity = 0
                installed_capacity_MF = 0
            else:
                installed_capacity = ((net_trade / PV_market_price)/10**6) + manufacturing_value/12 # on manufacturing value, check if it should be removed?
                market_factor = prel_market_size(net_trade, PVxchange_cost, str(year), month)
                installed_capacity_MF = ((net_trade / (PV_market_price * market_factor))/10**6) + manufacturing_value/12
            name = NJORD_function_test.name_cleanup(name, year)
            if name in reference.index.values:
                output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(year), month, name,
                                                                                installed_capacity,
                                                                                installed_capacity_MF,
                                                                                output_P_each_year,
                                                                                output_P_MF_each_year)
    # output_P_each_year = NJORD_function_test.acc_year(output_P_each_year)
    # output_P_MF_each_year = NJORD_function_test.acc_year(output_P_MF_each_year)
    return output_P_each_year.sort_index(), output_P_MF_each_year.sort_index()


def calc_PV_market_price(imp_or_exp_data, change, year, month, Europe):
    PV_market_price = 0
    nations_within = imp_or_exp_data.index.values
    change_list = change.index.values
    year_quarter = NJORD_function_test.add_quarter(year, month)
    for item in nations_within:
        if item in change_list:
            if imp_or_exp_data[item] == 0:
                continue
            single_value = change[year_quarter][item] * (imp_or_exp_data[item]/imp_or_exp_data.sum())  # value for each single nation
        else:
            if imp_or_exp_data[item] == 0:
                continue
            if item in Europe:
                single_value = change[year_quarter]["EU"] * (imp_or_exp_data[item]/imp_or_exp_data.sum())  # value for each single nation
            else:
                single_value = change[year_quarter]["RoW"] * (imp_or_exp_data[item]/imp_or_exp_data.sum())
        PV_market_price = PV_market_price + single_value
    return PV_market_price


def prel_market_size(net_trade, change, year, month):
    year_quarter = NJORD_function_test.add_quarter(year, month)
    # Preliminary Market size:
    prel_MS = (net_trade / change[year_quarter]["RoW"]) / 10 ** 6
    # print(prel_MS)
    all_market_factors = pd.read_excel("Market_size_factor_test2.xlsx", index_col=0)
    market_factor = 0
    # print(prel_MS,"prel")
    if prel_MS*3 <= 1:
        market_factor = all_market_factors["0-1MW"]["Factor"]
    elif 1 < prel_MS*3 <= 5:
        market_factor = all_market_factors["1-5MW"]["Factor"]
    elif 5 < prel_MS*3 <= 10:
        market_factor = all_market_factors["5-10MW"]["Factor"]
    elif 10 < prel_MS*3 <= 100:
        market_factor = all_market_factors["10-100MW"]["Factor"]
    elif 100 < prel_MS*3:  # <= 500:
        market_factor = all_market_factors["100-500MW"]["Factor"]
    elif 500 < prel_MS <= 1000:
        market_factor = all_market_factors["500-1000MW"]["Factor"]
    elif prel_MS > 1000:
        market_factor = all_market_factors["> 1000MW"]["Factor"]
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
    # Creation of the Excel sheet that will be returned.
    output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
    # output_P_each_year.at[name, "Ref " + ref_year] = ref_value
    # output_P_each_year.at[name, "Source " + ref_year] = source
    output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
    # output_P_MF_each_year.at[name, "Ref " + ref_year] = ref_value
    # output_P_MF_each_year.at[name, "Source " + ref_year] = source
    # output_P_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    # output_P_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    # output_P_each_year.at[name, "Other " + ref_year] = reference[other][name]
    # output_P_MF_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    # output_P_MF_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_MF_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    # output_P_MF_each_year.at[name, "Other " + ref_year] = reference[other][name]
    return output_P_each_year, output_P_MF_each_year


raw_data = pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str})
output_P_each_year, output_P_MF_each_year = price(raw_data)
output_P_each_year.to_excel(path_output + "NJORD_Price_model_10Codes_raw.xlsx")
output_P_MF_each_year.to_excel(path_output+"Test_NJORD-Price_model_results_10codes_pvshareremoved.xlsx")
