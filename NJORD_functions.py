import os
import warnings
import numpy as np
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)

path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok=True)

# Generic functions for both weight and price calculations, name_cleanup, a poorly written library for the NJORD models.


def name_clean_up(nation_list):
    # Clean up the names of nations from the raw database and return a list of countries
    # print(nation_list)
    nation_list = [sub.replace("Bolivia, Plurinational State of", "Bolivia") for sub in nation_list]
    nation_list = [sub.replace("Congo, Democratic Republic of the", "Democratic Republic of the Congo") for sub in
                   nation_list]
    nation_list = [sub.replace("Côte d'Ivoire", "Côte dIvoire") for sub in nation_list]
    nation_list = [sub.replace("Falkland Islands (Malvinas)", "Falkland Islands") for sub in nation_list]
    nation_list = [sub.replace("Hong Kong, China", "Hong Kong") for sub in nation_list]
    nation_list = [sub.replace("Iran, Islamic Republic of", "Iran") for sub in nation_list]
    nation_list = [sub.replace("Korea, Democratic People's Republic of", "North_Korea") for sub in nation_list]
    nation_list = [sub.replace("Korea, Republic of", "South Korea") for sub in nation_list]
    nation_list = [sub.replace("Lao People's Democratic Republic", "Laos") for sub in nation_list]
    nation_list = [sub.replace("Libya, State of", "Libya") for sub in nation_list]
    nation_list = [sub.replace("Macedonia, North", "Macedonia") for sub in nation_list]
    nation_list = [sub.replace("Micronesia, Federated States of", "Micronesia") for sub in nation_list]
    nation_list = [sub.replace("Moldova, Republic of", "Moldova") for sub in nation_list]
    nation_list = [sub.replace("Palestine, State of", "Palestine") for sub in nation_list]
    nation_list = [sub.replace("Russian Federation", "Russia") for sub in nation_list]
    nation_list = [sub.replace("Syrian Arab Republic", "Syria") for sub in nation_list]
    nation_list = [sub.replace("Taipei, Chinese", "Taiwan") for sub in nation_list]
    nation_list = [sub.replace("Tanzania, United Republic of", "Tanzania") for sub in nation_list]
    nation_list = [sub.replace("Venezuela, Bolivarian Republic of", "Venezuela") for sub in nation_list]
    nation_list = [sub.replace("Viet Nam", "Vietnam") for sub in nation_list]
    # Add a way to handle Sudan

    nation_list = [name.split(".") for name in nation_list]
    nation_list = [name[0] for name in nation_list]
    # for name in nation_list:
    #    if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
    #        nation_list.remove(name)
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
    if nation in manufacturing_df.index.values:
        manufacturing_value = manufacturing_df[year][nation]
    else:  # if no reported manufacturing, set to 0
        manufacturing_value = 0
    return manufacturing_value


def imports_or_export_in_period(dataset, country, year, export_import, value_or_quantity):
    data = dataset.loc[dataset["Reporting Country"] == country]
    data = data.loc[data["period"] == year]
    # Only viable for the weight model.
    if value_or_quantity == "Quantity":
        # Sort out all trade reported in kilos or tonnes
        data = data[data[export_import + "QuantityUnitCd"].str.contains("W", na=False)]
        # Change the trade reported in tonnes to kilos
        data.loc[data[export_import + "QuantityUnitCd"] == "WC0", export_import + value_or_quantity] = data[
                                                                                                           export_import + value_or_quantity] * 1000
        trade_data = data[export_import + value_or_quantity]
        trade_data = trade_data.set_axis(data["Partner Country"])
    else:
        trade_data = data[export_import + value_or_quantity]
        trade_data = trade_data.set_axis(data["Partner Country"])
    return trade_data


def create_mirror_data(data, country, year, export_import, value_or_quantity):
    data = data.loc[data["Partner Country"] == country]
    data = data.loc[data["period"] == year]
    # If statement to only select trade in tonnes in the weight model
    if value_or_quantity == "Quantity":
        # Sort out all trade reported in kilos or tonnes
        data = data[data[export_import + "QuantityUnitCd"].str.contains("W", na=False)]
        # Change the trade reported in tonnes to kilos
        data.loc[data[export_import + "QuantityUnitCd"] == "WC0", export_import + value_or_quantity] = data[
                                                                                                           export_import + value_or_quantity] * 1000
        mirror_data = data[export_import + value_or_quantity]
        mirror_data = mirror_data.set_axis(data["Reporting Country"])
    else:
        mirror_data = data[export_import + value_or_quantity]
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
    for item in imp_or_exp.index:  # Should be able to speed up with apply or vectorization
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


def share_in_PV(year, country, imp_or_exp_data, pv_share_unit, nations_within, import_or_export, six_or_ten):
    pv_share_unit_list1 = pv_share_unit.index.values
    pv_share_unit_list = []
    for nation in pv_share_unit_list1:
        pv_share_unit_list.append(nation.rsplit(' ', 1)[0])

    pv_share_unit_list = list(dict.fromkeys(pv_share_unit_list))
    if six_or_ten == "six":
        if import_or_export == "Import":
            for nation in nations_within:
                if nation in ["China", "Italy", "Japan", "United States of America", "Germany",
                              "France"]:  # "Taipei, Chinese"
                    imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year][nation + " export"]
                elif country in pv_share_unit_list:
                    if pv_share_unit[year][country + " import"] >= 0.3 and pv_share_unit[year][
                        country + " import"] <= 1:
                        imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year][country + " import"]
                    else:
                        imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year]["China export"]
                else:
                    imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year]["China export"]
        if import_or_export == "Export":
            for nation in nations_within:
                if country in pv_share_unit_list:
                    if pv_share_unit[year][country + " export"] == 0:
                        imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year]["China import"]
                    else:
                        imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year][country + " export"]
                else:
                    imp_or_exp_data[nation] = imp_or_exp_data[nation] * pv_share_unit[year]["China import"]
    return imp_or_exp_data


def add_quarter(year, month):  # No longer used as quarterly data is not reported
    if int(month) <= 3:
        quarter = "-Q1"
    elif int(month) <= 6:
        quarter = "-Q2"
    elif int(month) <= 9:
        quarter = "-Q3"
    else:
        quarter = "-Q4"
    return "".join([year, quarter])


def add_time_shift(months_shift, year, month):
    if month + months_shift > 12:
        month = months_shift - (12 - month)
        year = year + 1
    else:
        month = month + months_shift
    if month < 10:
        month = f"0{str(month)}"
    return str(year), str(month)


def create_quarterly_data(data):
    for name in data.columns:
        if "NJORD" in name:
            if int(name[-2:]) <= 3:
                temp_name = name[:-2] + "-Q1"
            elif 3 < int(name[-2:]) <= 6:
                temp_name = name[:-2] + "-Q2"
            elif 6 < int(name[-2:]) <= 9:
                temp_name = name[:-2] + "-Q3"
            else:
                temp_name = name[:-2] + "-Q4"
            if temp_name in data.columns:
                data[temp_name] += data[name]
            else:
                data[temp_name] = data[name]
    return data


# Functions for combined model

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
    large_exporters = ["China", "Korea, Republic of", "Taipei, Chinese", "Malaysia", "India", "Indonesia",
                       "United States of America", "Japan", "France", "Italy", "Germany"]
    for country in large_exporters:
        if country in exports.index:
            # print(exports.index)
            exports = exports.drop(country)
            # print(exports)
    return exports


def create_imports_exports_data(data):
    periods = list(dict.fromkeys(data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = check_missing_countries(data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    for name in nation_list:
        print(name)
        for period in periods:
            monthly_data = data.loc[data["period"] == period]
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2009":
                continue
            # Imports and exports a specific period for each specific country. Put in own function and save the results in a CSV-file?
            imports_period = imports_or_export_in_period(monthly_data, name, int(period), "import",
                                                         "Value")
            exports_period = imports_or_export_in_period(monthly_data, name, int(period), "export",
                                                         "Value")
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror = create_mirror_data(monthly_data, name, int(period), "import",
                                                       "Value")
            imports_period_mirror = create_mirror_data(monthly_data, name, int(period), "export",
                                                       "Value")
            imports_period = combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = combine_reported_and_mirror(exports_period, exports_period_mirror)

            exports_period = remove_large_exporters(exports_period)
    return imports_period, exports_period


def check_missing_countries(data1, all_countries_list):
    downloaded_countries = data1["Reporting Country"]
    downloaded_countries = list(downloaded_countries)
    downloaded_countries = list(dict.fromkeys(downloaded_countries))
    country_list = all_countries_list[1]
    name_not_in_reporting = list()
    for name in country_list:
        if name not in downloaded_countries:
            name_not_in_reporting.append(name)

    downloaded_countries = data1["Partner Country"]
    downloaded_countries = list(downloaded_countries)
    downloaded_countries = list(dict.fromkeys(downloaded_countries))
    name_not_in_partner = []
    for name in country_list:
        if name not in downloaded_countries:
            name_not_in_partner.append(name)
    not_in_reporting_or_partner = [x for x in name_not_in_reporting if x in set(name_not_in_partner)]
    # test_with_set = [x for x in name_not_in_partner if x in set(name_not_in_reporting)]
    return not_in_reporting_or_partner


# This function is way too big and does too much, should be split in multiples.
def sort_out_data(ten_code_data, six_code_data, PVxchange_cost, pv_share_unit, NTL_codes, unit):
    if unit == "Price":
        value_or_quantity = "Value"
    else:
        value_or_quantity = "Quantity"
    # Extract the available periods in the data, and the countries that are in the data.
    periods = list(dict.fromkeys(ten_code_data["period"]))
    # Select all the countries in the data, could probably be made more effective.
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = check_missing_countries(ten_code_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    # Set up the frames that will be returned.
    exports_period_summed = pd.DataFrame()
    imports_period_summed = pd.DataFrame()
    PV_market_price_summed = pd.DataFrame()
    for name in nation_list:
        print(name)
        for period in periods:
            monthly_data = ten_code_data.loc[ten_code_data["period"] == period]
            monthly_data = monthly_data.astype({"productCd": str})
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2022" or year == "2009":
                continue
            # Picks out the relevant codes
            NTL_codes_rel = NTL_codes.loc[NTL_codes["countryCd"] == name]
            NTL_codes_rel = NTL_codes_rel.loc[NTL_codes_rel["PV?"] == "Yes"]
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            monthly_data = monthly_data[monthly_data["productCd"].isin(relevant_codes)]
            # Imports and exports a specific period for each specific country.
            imports_period = imports_or_export_in_period(monthly_data, name, int(period), "import", value_or_quantity)
            imports_period = imports_period.groupby(["Partner Country"]).sum()
            exports_period = imports_or_export_in_period(monthly_data, name, int(period), "export", value_or_quantity)
            exports_period = remove_large_exporters(exports_period)
            exports_period = exports_period.groupby(["Partner Country"]).sum()
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            monthly_data = ten_code_data.loc[ten_code_data["period"] == period]
            monthly_data = monthly_data.loc[monthly_data["Partner Country"] == name]
            NTL_codes_rel = pd.DataFrame()
            for country in monthly_data["Reporting Country"]:
                NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
                NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "Yes"]
                NTL_codes_rel = pd.concat([NTL_codes_rel, NTL_codes_country])
                # print(NTL_codes_rel)
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            monthly_data = monthly_data[monthly_data["productCd"].isin(relevant_codes)]

            exports_period_mirror = create_mirror_data(monthly_data, name, int(period), "import", value_or_quantity)
            exports_period_mirror = remove_large_exporters(exports_period_mirror)
            exports_period_mirror = exports_period_mirror.groupby(["Reporting Country"]).sum()
            exports_period_mirror = exports_period_mirror[exports_period_mirror != 0]
            imports_period_mirror = create_mirror_data(monthly_data, name, int(period), "export", value_or_quantity)
            imports_period_mirror = imports_period_mirror.groupby(["Reporting Country"]).sum()
            imports_period_mirror = imports_period_mirror[imports_period_mirror != 0]

            imports_period_ten = combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period_ten = combine_reported_and_mirror(exports_period, exports_period_mirror)

            # 6-digit calculations
            monthly_data = six_code_data[six_code_data["period"] == period]
            imports_period = imports_or_export_in_period(monthly_data, name, int(period), "import", value_or_quantity)
            imports_period_mirror = create_mirror_data(monthly_data, name, int(period), "export", value_or_quantity)
            imports_period = combine_reported_and_mirror(imports_period, imports_period_mirror)
            nations_within_imp = imports_period.index.values

            imports_period_six = share_in_PV(str(year), name, imports_period, pv_share_unit, nations_within_imp,
                                             "Import", "six")
            exports_period = imports_or_export_in_period(monthly_data, name, int(period), "export", value_or_quantity)
            exports_period = remove_large_exporters(exports_period)
            exports_period_mirror = create_mirror_data(monthly_data, name, int(period), "import", value_or_quantity)
            exports_period_mirror = remove_large_exporters(exports_period_mirror)
            exports_period = combine_reported_and_mirror(exports_period, exports_period_mirror)
            nations_within_exp = exports_period.index.values
            exports_period_six = share_in_PV(str(year), name, exports_period, pv_share_unit, nations_within_exp,
                                             "Export", "six")
            imports_period = combine_reported_and_mirror(imports_period_ten, imports_period_six)
            exports_period = combine_reported_and_mirror(exports_period_ten, exports_period_six)
            PV_market_price = calc_PV_market_price(imports_period, PVxchange_cost, str(year), month,
                                                   ["Albania", "Andorra", "Austria", "Belarus", "Belgium",
                                                    "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
                                                    "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland",
                                                    "France", "Georgia", "Germany", "Greece",
                                                    "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia",
                                                    "Lithuania", "Luxembourg",
                                                    "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands",
                                                    "Norway", "Poland", "Portugal",
                                                    "Romania", "Russian_Federation", "Serbia", "Slovakia", "Slovenia",
                                                    "Spain", "Sweden", "Switzerland",
                                                    "Ukraine", "United_Kingdom"])
            PV_market_price_summed.at[name, period] = PV_market_price
            imports_period = imports_period.sum()
            exports_period = exports_period.sum()
            exports_period_summed.at[name, period] = exports_period
            imports_period_summed.at[name, period] = imports_period
    return imports_period_summed, exports_period_summed, PV_market_price_summed


def calc_PV_market_price(imp_or_exp_data, pvinsights, year, month, Europe):
    PV_market_price = 0
    nations_within = imp_or_exp_data.index.values
    pvxchange_list = pvinsights.index.values
    year_quarter = add_quarter(year, month)
    for item in nations_within:
        if item in pvxchange_list:
            if imp_or_exp_data[item] == 0:
                continue
            single_value = pvinsights[year_quarter][item] * (
                    imp_or_exp_data[item] / imp_or_exp_data.sum())  # value for each single nation
        else:
            if imp_or_exp_data[item] == 0:
                continue
            if item in Europe:
                single_value = pvinsights[year_quarter]["EU"] * (
                        imp_or_exp_data[item] / imp_or_exp_data.sum())  # value for each single nation
            else:
                single_value = pvinsights[year_quarter]["RoW"] * (imp_or_exp_data[item] / imp_or_exp_data.sum())
        PV_market_price = PV_market_price + single_value
    return PV_market_price


def count_units_in_trade(ten_code_data, six_code_data):
    unit_or_weight = pd.DataFrame()
    unit_or_weight_six = pd.DataFrame()
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    periods = list(dict.fromkeys(ten_code_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = check_missing_countries(ten_code_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    for name in nation_list:
        print(name)
        for month in periods:
            country_data = ten_code_data.loc[ten_code_data["Reporting Country"] == name]
            country_data = country_data.loc[country_data["period"] == month]
            country_data_six = six_code_data.loc[six_code_data["Reporting Country"] == name]
            country_data_six = country_data_six.loc[country_data_six["period"] == month]
            NTL_codes_rel = NTL_codes.loc[NTL_codes["countryCd"] == name]
            NTL_codes_rel = NTL_codes_rel.loc[NTL_codes_rel["PV?"] == "Yes"]
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            country_data = country_data[country_data["productCd"].isin(relevant_codes)]
            # print(test["Reporting Country"])
            imports_period = imports_or_export_in_period(country_data_six, name, int(month), "import", "Quantity")
            trade_data = country_data_six["importQuantity"]
            trade_data = trade_data.set_axis(country_data_six["Partner Country"])
            trade_data = trade_data.replace(np.nan, 0)
            exports_period = imports_or_export_in_period(country_data, name, int(month), "export", "Quantity")
            trade_data_exp = country_data_six["importQuantity"]
            trade_data_exp = trade_data_exp.set_axis(country_data_six["Partner Country"])
            trade_data_exp = trade_data_exp.replace(np.nan, 0)
            if sum(trade_data) == 0:
                continue
            if sum(trade_data_exp) == 0:
                continue
            if sum(imports_period) - sum(trade_data) / sum(trade_data) < 0.9:
                unit_or_weight_six.at[name, month] = "Unit"
            elif sum(exports_period) - sum(trade_data_exp) / sum(trade_data_exp) < 0.9:
                unit_or_weight_six.at[name, month] = "Unit"
            else:
                unit_or_weight_six.at[name, month] = "Weight"

            # export_country_weight_data = country_data[country_data["export" + "QuantityUnitCd"].str.contains("W", na=False)]
            # import_country_weight_data = country_data[country_data["import" + "QuantityUnitCd"].str.contains("W", na=False)]

    print(unit_or_weight)
    print(unit_or_weight_six)
    return unit_or_weight, unit_or_weight_six


# units_or_weights, units_or_weights_six = count_units_in_trade(pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str}), pd.read_csv("ITC_Monthly_data_HS_6.csv", dtype={"productCd": str}))
# units_or_weights.to_csv("units_or_weights.csv")
# units_or_weights_six.to_csv("units_or_weight_six.csv")

def percent_trade_PV(ten_code_data, six_code_data, unit_itc):
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    periods = list(dict.fromkeys(ten_code_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = check_missing_countries(ten_code_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    trade_not_relevant = pd.DataFrame()

    for name in nation_list:
        print(name)
        for period in periods:
            monthly_data_ten = ten_code_data.loc[ten_code_data["period"] == period]
            monthly_data_ten = monthly_data_ten.astype({"productCd": str})
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2009":
                continue
            # Add months to quarters/years before you do the calculations.
            # Picks out the relevant codes
            NTL_codes_rel = NTL_codes.loc[NTL_codes["countryCd"] == name]
            NTL_codes_rel = NTL_codes_rel.loc[NTL_codes_rel["PV?"] == "Yes"]
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            monthly_data_ten = monthly_data_ten[monthly_data_ten["productCd"].isin(relevant_codes)]
            # Imports and exports a specific period for each specific country. Put in own function and save the
            # results in a CSV-file?
            imports_period = imports_or_export_in_period(monthly_data_ten, name, int(period), "import",
                                                         unit_itc)
            imports_period = imports_period.groupby(["Partner Country"]).sum()
            exports_period = imports_or_export_in_period(monthly_data_ten, name, int(period), "export",
                                                         unit_itc)
            exports_period = exports_period.groupby(["Partner Country"]).sum()
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            monthly_data_ten = ten_code_data.loc[ten_code_data["period"] == period]
            monthly_data_ten = monthly_data_ten.loc[monthly_data_ten["Partner Country"] == name]
            NTL_codes_rel = pd.DataFrame()
            for country in monthly_data_ten["Reporting Country"]:
                NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
                NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "Yes"]
                NTL_codes_rel = pd.concat([NTL_codes_rel, NTL_codes_country])
                # NTL_codes_rel = NTL_codes_rel.concat(NTL_codes_country)
                # print(NTL_codes_rel)
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            monthly_data_ten = monthly_data_ten[monthly_data_ten["productCd"].isin(relevant_codes)]

            exports_period_mirror = create_mirror_data(monthly_data_ten, name, int(period), "import",
                                                       unit_itc)
            exports_period_mirror = exports_period_mirror.groupby(["Reporting Country"]).sum()
            imports_period_mirror = create_mirror_data(monthly_data_ten, name, int(period), "export",
                                                       unit_itc)
            imports_period_mirror = imports_period_mirror.groupby(["Reporting Country"]).sum()

            imports_period = combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = combine_reported_and_mirror(exports_period, exports_period_mirror)

            # exports_period = NJORD_function_test.remove_large_exporters(exports_period)

            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values

            percentage_imp, sum_imports = calc_percentage_import_or_export(nations_within_imp,
                                                                           imports_period)
            percentage_exp, sum_exports = calc_percentage_import_or_export(nations_within_exp,
                                                                           exports_period)

            # 6-digits level
            monthly_data_six = six_code_data.loc[six_code_data["period"] == period]
            imports_period_six = imports_or_export_in_period(monthly_data_six, name, int(period),
                                                             "import", unit_itc)
            exports_period_six = imports_or_export_in_period(monthly_data_six, name, int(period),
                                                             "export", unit_itc)
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror_six = create_mirror_data(monthly_data_six, name, int(period),
                                                           "import", unit_itc)
            imports_period_mirror_six = create_mirror_data(monthly_data_six, name, int(period),
                                                           "export", unit_itc)
            imports_period_six = combine_reported_and_mirror(imports_period_six,
                                                             imports_period_mirror_six)
            exports_period_six = combine_reported_and_mirror(exports_period_six,
                                                             exports_period_mirror_six)

            # exports_period_six = NJORD_function_test.remove_large_exporters(exports_period_six)
            nations_within_imp = imports_period_six.index.values
            nations_within_exp = exports_period_six.index.values

            percentage_imp, sum_imports_six = calc_percentage_import_or_export(nations_within_imp,
                                                                               imports_period_six)
            # Add a check for export to large exporter, and remove them.
            percentage_exp, sum_exports_six = calc_percentage_import_or_export(nations_within_exp,
                                                                               exports_period_six)

            if name in reference.index.values:
                trade_not_relevant.at[name + " 10-code import", period] = sum_imports
                trade_not_relevant.at[name + " 10-code export", period] = sum_exports
                trade_not_relevant.at[name + " 6-code import", period] = sum_imports_six
                trade_not_relevant.at[name + " 6-code export", period] = sum_exports_six
    return trade_not_relevant


# six = pd.read_csv("ITC_Monthly_data_HS_6.csv", dtype={"productCd": str})
# ten = pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str})
# check_amount = percent_trade_PV(ten, six)
# check_amount.to_excel("To_calculate_percentage_of_PV_weight.xlsx")

def calculate_percentage_of_PV(trade_data):
    PV_share_in_ten_code = pd.DataFrame()
    trade_data.columns = trade_data.columns.astype(str)
    i = 2010
    while i < 2022:
        n = 0
        one_year = trade_data.loc[:, trade_data.columns.str.startswith(str(i))]
        one_year = one_year.sum(axis=1)
        while n < len(one_year.index):
            import_data = one_year.iloc[n:n + 4:2, ]
            export_data = one_year.iloc[n + 1:n + 5:2, ]
            # print(import_data)
            percent_import = import_data.iloc[0] / import_data.iloc[1]
            percent_export = export_data.iloc[0] / export_data.iloc[1]
            junkwords = ["10-code", "6-code"]
            country_imp = [word for word in import_data.index[0].split() if word not in junkwords]
            country_exp = [word for word in export_data.index[0].split() if word not in junkwords]
            country_imp = " ".join(country_imp)
            country_exp = " ".join(country_exp)
            PV_share_in_ten_code.at[country_imp, str(i)] = percent_import
            PV_share_in_ten_code.at[country_exp, str(i)] = percent_export
            n += 4
        i = i + 1
    PV_share_in_ten_code = PV_share_in_ten_code.fillna(0)
    PV_share_in_ten_code = PV_share_in_ten_code.replace([np.inf, -np.inf], 0)
    return PV_share_in_ten_code


# trade_data = pd.read_excel("To_calculate_percentage_of_PV_weight.xlsx", index_col=0)
# trade_data = calculate_percentage_of_PV(trade_data)
# trade_data.to_excel("share_in_PV_weight.xlsx")


#  Not used anymore!!!!
def calc_PV_factor(year, pv_share_unit, nations_within, percentage, import_export, six_or_ten):
    pv_share_unit_list = pv_share_unit.index.values
    cont = 0
    pv_factor = 0
    if import_export == "Import":
        for nation in nations_within:
            if nation == "DataType":
                continue
            if six_or_ten == "ten":
                single_value = percentage[cont]
            else:
                if nation in pv_share_unit_list:
                    single_value = pv_share_unit[year][nation + " export"] * percentage[cont]
                else:
                    single_value = pv_share_unit[year]["China" + " export"] * percentage[cont]
            pv_factor += single_value
            cont = cont + 1
    if import_export == "Export":  # Why is this different?
        for nation in nations_within:
            if nation == "DataType":
                continue
            if six_or_ten == "ten":
                single_value = percentage[cont]
            else:
                if nation in pv_share_unit_list:
                    single_value = pv_share_unit[year][nation + " import"] * percentage[cont]
                else:
                    single_value = pv_share_unit[year]["China import"] * percentage[cont]
            pv_factor += single_value
            cont = cont + 1
    return pv_factor


# Not used
def direct_or_mirror(data, unit, import_export, year,
                     name):  # Do not need to check direct or mirror data, rewritten in the specific programs
    data = pd.read_excel(data + import_export + "\\" + name + ".xlsx", index_col=0,
                         na_values=['NA'])  # Needs to be changed now.
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
        add1 = ""
        word1 = ""
        word2 = ""
    time_window = [word1 + add1 + str(year)]
    if import_export == "Export":
        time_window = [word2 + add1 + str(year)]
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


def extract_one_country(country):  # Never used
    data = pd.read_csv("ITC_yearly_data_HS_6.csv")
    country_data = data.loc[(data["Reporting Country"] == country)]
    country_data = country_data.loc[(country_data["period"] == 2012)]
    country_data_import = country_data["exportValue"]
    # print(country_data_import)
    return country_data

# country = "Sweden"
# extract_one_country(country)
