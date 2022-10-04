# Code for validation of data in NJORD.

import numpy as np
import pandas as pd
import scipy
from scipy import stats
import seaborn as sns
# from fitter import Fitter, get_common_distributions, get_distributions
from matplotlib import pyplot as plt
import statistics
import itertools
import os
import NJORD_function_test

# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok=True)
price_model_results = pd.read_excel("NJORD_Price_year_with_ref.xlsx", index_col=0, na_values=['NA'])
weight_model_results = pd.read_excel("Weight_results_yearly.xlsx", index_col=0, na_values=['NA'])
# reference_data = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])
reference_countries = ["Australia", "Belgium", "Chile", "Denmark", "Finland", "France", "Israel", "Italy", "Japan",
                       "Spain", "Sweden", "Switzerland", "United States of America"]


def Pearson_coef(input, reference_countries, unit):
    # Calculates the Pearson Coefficient between NJORDs data and reference data (IRENA and PVPS)
    # Only for reference countries from thesis and PVPS now, will add check for emerging markets later
    Njord = input.loc[:, ["NJORD" in i for i in input.columns]]
    PVPS = input.loc[:, ["PVPS" in i for i in input.columns]]
    Irena = input.loc[:, ["IRENA" in i for i in input.columns]]
    # print(Njord)
    # print(Irena)
    # print(PVPS)

    corr_Njord_Irena = []
    corr_Njord_PVPS = []
    corr_Njord_PVPS_ref = []
    ref_Njord = pd.DataFrame()
    ref_PVPS = pd.DataFrame()
    for country in reference_countries:
        if unit == "Weight":
            if country != "Australia" and country != "Japan" and country != "United States of America" and country != "Israel":
                ref_Njord = ref_Njord.append(Njord.loc[country])
                ref_PVPS = ref_PVPS.append(PVPS.loc[country])
        else:
            ref_Njord = ref_Njord.append(Njord.loc[country])
            ref_PVPS = ref_PVPS.append(PVPS.loc[country])
    # print(ref_Njord)
    # print(ref_PVPS)
    for year in range(2010, 2021):
        corr_Njord_Irena.append({str(year): Njord["NJORD "+str(year)].corr(Irena["IRENA "+str(year)])})
        corr_Njord_PVPS.append({str(year): Njord["NJORD "+str(year)].corr(PVPS["PVPS "+str(year)])})  # For all countries P-cor
        corr_Njord_PVPS_ref.append({str(year): ref_Njord["NJORD "+str(year)].corr(ref_PVPS["PVPS "+str(year)])})
        # print(corr_Njord_PVPS_ref)
    # printing out graphs for easier overview
    # ref_PVPS.swapaxes(axis1="Index", axis2="Columns")
    # ref_Njord.plot(y=ref_Njord.loc("NJORD 2019"))
    # plt.show()

    return corr_Njord_Irena, corr_Njord_PVPS, corr_Njord_PVPS_ref  # at the moment for all countries and reference
    # countries, should find emerging markets from report and compare there as well.


# corr_Njord_Irena_price, corr_Njord_PVPS_price, corr_Njord_PVPS_ref_price = Pearson_coef(price_model_results, reference_countries, "Price")
# corr_Njord_Irena_weight, corr_Njord_PVPS_weight, corr_Njord_PVPS_ref_weight = Pearson_coef(weight_model_results, reference_countries, "Weight")


def calc_acc_cap(input_data, data_sources):
    data = input_data.loc[:, [data_sources in i for i in input_data]]
    data_acc = pd.DataFrame(index=data.index, columns=data.columns)
    for row in data.index.values:
        N_acc = 0
        for col in data:
            N_acc += data.loc[row, col]
            data_acc.loc[row, col] = N_acc
    return data_acc


#Njord_acc_price = calc_acc_cap(price_model_results, "NJORD")
#Njord_acc_price.to_excel(path_output+"Njord-Price_acc_all.xlsx")
#Njord_acc_weight = calc_acc_cap(weight_model_results, "NJORD")
#Njord_acc_weight.to_excel(path_output+"NJORD-Weight_acc_all.xlsx")

# plot_acc_cap(price_model_results, reference_countries)


def calc_mean_abs_dev(input, reference_countries):
    Njord = input.loc[:, ["NJORD" in i for i in input.columns]]
    PVPS = input.loc[:, ["PVPS" in i for i in input.columns]]
    Irena = input.loc[:, ["IRENA" in i for i in input.columns]]
    ref_Njord = pd.DataFrame()
    ref_PVPS = pd.DataFrame()
    sum = 0
    for country in reference_countries:
        ref_Njord = ref_Njord.append(Njord.loc[country])
        ref_PVPS = ref_PVPS.append(PVPS.loc[country])
        # print(ref_Njord["NJORD 2010"])
        # print(ref_Njord.loc[country, "NJORD 2010"])
    for year in range(2010, 2021):
        mean_PVPS = statistics.mean(ref_PVPS["PVPS "+str(year)])
        mean_Njord = statistics.mean(ref_Njord["NJORD "+str(year)])
        for country in reference_countries:
            mad = (mean_PVPS-ref_Njord.loc[country, "NJORD "+str(year)])
            sum += mad/len(ref_PVPS["PVPS "+str(year)])
        mad = mad
    mad_Njord = ref_Njord.mad()
    mad_PVPS = ref_PVPS.mad()
    # print(mean_PVPS)
    return mad_PVPS, mad_Njord

def calculate_standard_deviation(data):
    standard_deviation = statistics.stdev(data)
    return standard_deviation

def standard_deviation_all_countries(data, data_sources=""):  # send in more specific data, so only Njord, or only the data you want to look at.
    stdev_year = []
    stdev_countries = []
    for country in data.index:
        stdev_country = []
        for col in data:
            if data_sources != "":
                if data_sources in col:
                    stdev_country.append(data.loc[country][col])
                    stdev_year.append([str(col), statistics.stdev(data[col])])
            else:
                stdev_country.append(data.loc[country][col])
                stdev_year.append([str(col), statistics.stdev(data[col])])
        stdev_country = statistics.stdev(stdev_country)
        stdev_countries.append([country, stdev_country])
    new_stdev_year = []
    for i in stdev_year:
        if i not in new_stdev_year:
            new_stdev_year.append(i)
    stdev_year = new_stdev_year
    # print(stdev_year)
    return stdev_countries, stdev_year


# stdev_test_countries, stdev_test_year = standard_deviation_all_countries(price_model_results, "NJORD")

# calc_mean_abs_dev(price_model_results, reference_countries)


def mean_difference_from_ref_data(input):
    Njord = input.loc[:, ["NJORD" in i for i in input.columns]]
    PVPS = input.loc[:, ["PVPS" in i for i in input.columns]]
    Irena = input.loc[:, ["IRENA" in i for i in input.columns]]
    diff_Njord_Irena = pd.DataFrame()
    percentual_diff_Njord_Irena = pd.DataFrame()
    for country in Njord.index:
        Njord_value = 0
        for year in Njord:
            Njord_value += Njord.loc[country, year]
            year = year.split(" ")[1]
            PVPS_value = PVPS.loc[country, "PVPS "+year]  # Should only be used in comparison with reference countries
            Irena_value = Irena.loc[country, "IRENA "+year]
            diff_Njord_Irena.loc[country, year] = Njord_value-Irena_value
            if Irena_value != 0:
                percentual_diff_Njord_Irena.loc[country, year] = (Njord_value-Irena_value)/Irena_value
    percentual_diff_Njord_Irena.replace([np.inf, -np.inf], np.nan, inplace=True)
    mean_difference_Njord_Irena = pd.DataFrame()
    for country in diff_Njord_Irena.index:
        mean_difference_Njord_Irena.loc[country, "Mean"] = diff_Njord_Irena.loc[country].mean()
    return mean_difference_Njord_Irena, diff_Njord_Irena, percentual_diff_Njord_Irena


# mean_diff, diff, perc_diff = mean_difference_from_ref_data(price_model_results)
# std_diff_countries, std_diff_year = standard_deviation_all_countries(diff)
# perc_std_diff_countries, perc_std_diff_year = standard_deviation_all_countries(perc_diff)
# perc_std_diff_countries_df = pd.DataFrame(perc_std_diff_countries).set_index(0)
# std_diff_countries_df = pd.DataFrame(std_diff_countries).set_index(0)
# perc_diff.to_excel(path_output+"Njord_percentual_diff_Irena.xlsx")
# diff.to_excel(path_output+"Njord_diff_Irena.xlsx")
# diff_1 = perc_diff# .transpose()
# print(diff_1)
# diff_1.plot()#hist(bins=50)
# plt.show()

def calc_median(data_input, datasources=""):  # Takes a DataFrame as input and returns the median for all rows and columns in the DataFrame. Returns it as Series.
    median_rows = data_input.median(axis="columns")
    median_columns = data_input.median()
    return median_rows, median_columns

# calc_median(price_model_results)

def check_reference_countries(data, reference_countries):
    data = data.loc[data["Unnamed: 0"].isin(reference_countries)]
    # data = data.loc[data.index.isin(reference_countries)]
    # print(data)
    # ref_country_data = data.iloc[:, -9:]
    ref_country_data = pd.DataFrame()
    ref_country_data.insert(0, "country", data["Unnamed: 0"], True)
    # print(ref_country_data)
    for col in data.columns:
        cutoff = 2014
        if "NJORD" in col:
            NJORD_placeholder = data.loc[:, [col[-6:-2] in i for i in data.columns]]
            NJORD_placeholder = NJORD_placeholder.loc[:, ~NJORD_placeholder.columns.duplicated()]
            NJORD_placeholder = NJORD_placeholder.loc[:, ["NJORD" in i for i in NJORD_placeholder.columns]]
            ref_country_data["NJORD " + col[-6:-2]] = NJORD_placeholder.sum(axis=1)
            # print(ref_country_data)
        if "PVPS" in col:
            if int(col[-4:]) >= cutoff:
                ref_country_data[col] = data[col]
    i = 2014
    while i < 2021:
        diff = ref_country_data["NJORD "+str(i)] - ref_country_data["PVPS " + str(i)]
        ref_country_data["DIFF "+str(i)] = diff
        ref_country_data["Percent Diff "+str(i)] = (diff/ref_country_data["PVPS "+str(i)])
        i += 1
    ref_country_data = ref_country_data.set_index(ref_country_data.iloc[:]["country"])
    ref_country_data = ref_country_data.drop(columns="country")
    i = 2014
    while i < 2021:
        summed = ref_country_data["NJORD "+str(i)].sum()
        ref_country_data.at["Summed", "NJORD "+str(i)] = summed
        summed = ref_country_data["PVPS "+str(i)].sum()
        ref_country_data.at["Summed", "PVPS "+str(i)] = summed
        summed = ref_country_data["DIFF "+str(i)].sum()
        ref_country_data.at["Summed", "DIFF "+str(i)] = summed
        abs_diff = abs(ref_country_data["DIFF "+str(i)])
        ref_country_data["AbsDiff "+str(i)] = abs_diff
        summed = ref_country_data["AbsDiff "+str(i)].sum()
        ref_country_data.at["Summed", "AbsDiff "+str(i)] = summed
        i += 1
    return ref_country_data


def outlier_check(raw_data):
    imports_country_month = pd.DataFrame()
    exports_country_month = pd.DataFrame()
    periods = list(dict.fromkeys(raw_data["period"]))
    # print(periods)
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = NJORD_function_test.check_missing_countries(raw_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    outliers_import = pd.DataFrame()
    outliers_export = pd.DataFrame()
    # Should make a function that does this (330-352)
    for nation in nation_list:
        for period in periods:
            monthly_data = raw_data.loc[raw_data["period"] == period]
            imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, nation, int(period), "import",
                                                                             "Value")
            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, nation, int(period), "export",
                                                                             "Value")
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, nation, int(period), "import",
                                                                           "Value")
            imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data, nation, int(period), "export",
                                                                           "Value")
            imports_period = NJORD_function_test.combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = NJORD_function_test.combine_reported_and_mirror(exports_period, exports_period_mirror)

            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values

            percentage_imp, sum_imports = NJORD_function_test.calc_percentage_import_or_export(nations_within_imp,
                                                                                               imports_period)
            # Add a check for export to large exporter, and remove them.
            percentage_exp, sum_exports = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp,
                                                                                               exports_period)
            imports_country_month.at[nation, period] = sum_imports
            exports_country_month.at[nation, period] = sum_exports
            imports_country_month = imports_country_month.sort_index()
            exports_country_month = exports_country_month.sort_index()
    imports_country = imports_country_month.transpose()
    exports_country = exports_country_month.transpose()
    for country in imports_country:
        # print(imports_country[country])
        MAD = imports_country[country].mad()
        median = imports_country[country].median()
        for i in imports_country.index:
            print(imports_country[country].loc[i], imports_country[country])
            z_score = 0.6745*(imports_country[country].loc[i]-median)/MAD
            if z_score.item() > 3.5 or z_score.item() < -3.5:
                outliers_import.at[country, i] = z_score
    for country in exports_country:
        MAD = exports_country[country].mad()
        median = exports_country[country].median()
        for i in exports_country.index:
            print(exports_country[country].loc[i], exports_country[country])
            z_score = 0.6745*(exports_country[country].loc[i]-median)/MAD
            if z_score.item() > 3.5 or z_score.item() < -3.5:
                outliers_export.at[country, i] = z_score

    outliers_import = outliers_import.transpose()
    outliers_import = outliers_import.sort_index()
    outliers_export = outliers_export.transpose()
    outliers_export = outliers_export.sort_index()
    return outliers_import, outliers_export

test = pd.read_excel("Test_NJORD-Price_model_results_10codes_pvshareremoved.xlsx")
# print(test)
ref = check_reference_countries(test, reference_countries)
ref.to_excel("reference_countries_Price_10codes_shareadded4.xlsx")

# outlier_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
# outlier_import, outlier_export = outlier_check(outlier_data)
# outlier_import.to_excel("Z_outliers_import.xlsx")
# outlier_export.to_excel("Z_outliers_export.xlsx")


def sort_out_data(data):
    six_code_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
    unit = "Price"
    pv_share_unit = pd.read_excel("Share_in_PV_" + unit + ".xlsx", index_col=0)  # Read the PV_share from excel
    PVxchange_cost = pd.read_excel("PVxchange.xlsx", index_col=0)  # Read the cost of panels from big producers
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    # Extract the available periods in the data, and the countries that are in the data.
    periods = list(dict.fromkeys(data["period"]))
    # Select all the countries in the data, could probably be made more effective.
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = NJORD_function_test.check_missing_countries(data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    exports_period_summed = pd.DataFrame()
    imports_period_summed = pd.DataFrame()
    PV_market_price_summed = pd.DataFrame()
    for name in nation_list:
        print(name)
        for period in periods:
            monthly_data = data.loc[data["period"] == period]
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2022" or year == "2009":
                continue
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
            monthly_data = data.loc[data["period"] == period]
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

            imports_period_six = NJORD_function_test.share_in_PV(str(year), name, imports_period, pv_share_unit,
                                                                 nations_within_imp, "Import", "six")

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
            net_trade_summed = imports_period-exports_period
            net_trade_summed = net_trade_summed.sum()
            print(net_trade_summed)
            imports_period = imports_period.sum()
            exports_period = exports_period.sum()
            exports_period_summed.at[name, period] = exports_period
            imports_period_summed.at[name, period] = imports_period
    return imports_period_summed, exports_period_summed, PV_market_price_summed, net_trade_summed


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


# imp_summed, exp_summed, PV_marksum, net_trade = sort_out_data(pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str}))
# imp_summed.to_csv("Import_summed_NJORD.csv")
# exp_summed.to_csv("Export_summed_NJORD.csv")
# PV_marksum.to_csv("PV_market_price.csv")

def market_factor_testing(imp_sum, exp_sum, PV_market_sum):
    market_factors = pd.read_excel("Market_size_factor_test.xlsx", index_col=0)
    print(market_factors)
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    output_P_each_year = pd.DataFrame()
    output_P_MF_each_year = pd.DataFrame()
    prel_ms_save = pd.DataFrame()
    for nation in imp_sum.index.values:
        print(nation)
        for month in imp_sum.columns.values:
            manufacturing_value = NJORD_function_test.manufacturing(nation, str(month[:4]), manufacturing_df)
            net_trade = (imp_sum.loc[nation][month] - exp_sum.loc[nation][month]) * 1000
            if PV_market_sum.loc[nation][month] == 0:
                installed_capacity = 0
                installed_capacity_MF = 0
            else:
                installed_capacity = ((net_trade/PV_market_sum.loc[nation][month])/10**6) + manufacturing_value/12  # on manufacturing value, check if it should be removed?
                market_factor, prel_ms = prel_market_size(net_trade, month, market_factors)
                prel_ms_save.at[name, month] = prel_ms
                installed_capacity_MF = ((net_trade/(PV_market_sum.loc[nation][month]*market_factor))/10**6) + manufacturing_value/12
            name = NJORD_function_test.name_cleanup(nation, month[:4])
            if name in reference.index.values:
                output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(month[:4]), month[4:], name,
                                                                                installed_capacity,
                                                                                installed_capacity_MF,
                                                                                output_P_each_year,
                                                                                output_P_MF_each_year)
    prel_ms_save.to_excel("prel_ms_save.xlsx")
    return output_P_MF_each_year


def prel_market_size(net_trade, month, all_market_factors):
    change = pd.read_excel("PVxchange.xlsx", index_col=0)  # Read the cost of panels from big producers
    year_quarter = NJORD_function_test.add_quarter(month[:4], month[4:])
    # Preliminary Market size:
    prel_MS = (net_trade / change[year_quarter]["RoW"]) / 10 ** 6
    # print(prel_MS,"prel")
    if prel_MS < 0:
        market_factor = 1
    if 0 < prel_MS <= 1:
        market_factor = all_market_factors["0-1MW"]["Factor"]
    elif 1 < prel_MS <= 5:
        market_factor = all_market_factors["1-5MW"]["Factor"]
    elif 5 < prel_MS <= 10:
        market_factor = all_market_factors["5-10MW"]["Factor"]
    elif 10 < prel_MS <= 100:
        market_factor = all_market_factors["10-100MW"]["Factor"]
    elif 100 < prel_MS <= 500:
        market_factor = all_market_factors["100-500MW"]["Factor"]
    elif 500 < prel_MS <= 1000:
        market_factor = all_market_factors["500-1000MW"]["Factor"]
    elif prel_MS > 1000:
        market_factor = all_market_factors["> 1000MW"]["Factor"]
    return market_factor, prel_MS

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


def market_factor_training(imp_summed, exp_summed, PV_marksum, ref):
    mf = pd.read_excel("Market_size_factor_test2.xlsx", index_col=0)
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=[0])  # Read reference data
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=[0])  # Read manufacturing data
    manufacturing_df.fillna(0, inplace=True)
    imp_summed_ref = imp_summed.loc[[x for x in imp_summed.index.values if x in ref]]
    exp_summed_ref = exp_summed.loc[[x for x in exp_summed.index.values if x in ref]]
    ref_absdiff_best = np.inf
    output_P_each_year = pd.DataFrame()
    output_P_MF_each_year = pd.DataFrame()
    net_trade_df = pd.DataFrame()
    prel_ms_cat = pd.DataFrame()
    market_factor_count = pd.DataFrame(np.zeros((12, 7)),
                                       columns=["<1", "1-5", "5-10", "10-100", "100-500", "500-1000", ">1000"],
                                       index=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018",
                                              "2019", "2020", "2021"])
    for nation in imp_summed_ref.index.values:
        for month in imp_summed_ref.columns.values:
            net_trade = (imp_summed_ref.loc[nation][month]-exp_summed_ref.loc[nation][month]) * 1000
            # print(nation, month, net_trade)
            net_trade_df.at[nation, month] = net_trade
            market_factor, prel_ms = prel_market_size(net_trade_df.loc[nation][month], month, mf)
            prel_ms_cat.at[nation, month] = prel_ms
            market_factor_count = market_factor_test_calculation(prel_ms_cat.loc[nation][month], market_factor_count,
                                                                 month[:-2])
    for i in range(0, 100):
        print(i)
        for nation in net_trade_df.index.values:
            for month in net_trade_df.columns.values:
                manufacturing_value = NJORD_function_test.manufacturing(nation, str(month[:4]), manufacturing_df)
                # Minimize the abs deviation changing the market factors
                market_factor, prel_ms = prel_market_size(net_trade_df.loc[nation][month], month, mf)
                installed_capacity = ((net_trade_df.loc[nation][month]/(PV_marksum.loc[nation][month]*market_factor))/(10**6)) - (manufacturing_value/12)
                name = NJORD_function_test.name_cleanup(nation, month[:4])
                if name in reference.index.values:
                    output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(month[:4]), month[4:], name,
                                                                                installed_capacity,
                                                                                installed_capacity,
                                                                                output_P_each_year,
                                                                                output_P_MF_each_year)
        output_P_MF_each_year.to_excel("testest.xlsx")
        mf_test = pd.read_excel("testest.xlsx")
        ref = check_reference_countries(mf_test, reference_countries)
        mf_test = mf_test.set_index("Unnamed: 0")
        ref_absdiff = ref.filter(like="AbsDiff")
        ref_diff = ref.filter(like="DIFF")
        print(ref_absdiff.loc["Summed"].sum())
        print(ref_absdiff_best)
        market_factor_count = pd.DataFrame(np.zeros((2, 8)),
                                           columns=[">0", "0-1MW", "1-5MW", "5-10MW", "10-100MW", "100-500MW", "500-1000MW", "> 1000MW"],
                                           index=["higher", "lower"])
        if ref_absdiff.loc["Summed"].sum() < ref_absdiff_best:
            ref_absdiff_best = ref_absdiff.loc["Summed"].sum()
            print(ref_absdiff_best)
            mf_best = mf
            print(mf_best)
            print("End of loop " + str(i))
        for country in net_trade_df.index.values:
            for month in net_trade_df.columns.values:
                if month[:-2] == "2010" or month[:-2] == "2011" or month[:-2] == "2012" or month[:-2] == "2013" or month[:-2] == "2021":
                    continue
                market_size_month = market_size(mf_test.loc[country]["NJORD " + month])
                if market_size_month == "<0":
                    continue
                elif ref_diff.loc[country]["DIFF "+month[:-2]] <= 0:
                    market_factor_count.at["lower", market_size_month] += 1
                    # mf[market_size_month] = mf[market_size_month] - 0.01
                else:
                    market_factor_count.at["higher", market_size_month] += 1
                    # mf[market_size_month] = mf[market_size_month] + 0.01
        print(market_factor_count)
        for column in market_factor_count:
            if column == ">0":
                continue
            if market_factor_count.loc["higher"][column] > market_factor_count.loc["lower"][column]:
                mf[column] -= 0.001
            else:
                mf[column] += 0.001

    print(mf_best)
    return


def market_factor_test_calculation(prel_ms, market_factor_count, year):
    if 0 < prel_ms <= 1:
        market_factor_count.loc[str(year)]["<1"] += 1
    elif 1 < prel_ms <= 5:
        market_factor_count.loc[str(year)]["1-5"] += 1
    elif 5 < prel_ms <= 10:
        market_factor_count.loc[str(year)]["5-10"] += 1
    elif 10 < prel_ms <= 100:
        market_factor_count.loc[str(year)]["10-100"] += 1
    elif 100 < prel_ms <= 500:
        market_factor_count.loc[str(year)]["100-500"] += 1
    elif 500 < prel_ms <= 1000:
        market_factor_count.loc[str(year)]["500-1000"] += 1
    elif prel_ms > 1000:
        market_factor_count.loc[str(year)][">1000"] += 1
    return market_factor_count


def market_size(Njord_calc):
    if 0 <= Njord_calc <= 1:
        market_size_a = "0-1MW"
    elif 1 < Njord_calc <= 5:
        market_size_a = "1-5MW"
    elif 5 < Njord_calc <= 10:
        market_size_a = "5-10MW"
    elif 10 < Njord_calc <= 100:
        market_size_a = "10-100MW"
    elif 100 < Njord_calc <= 500:
        market_size_a = "100-500MW"
    elif 500 < Njord_calc <= 1000:
        market_size_a = "500-1000MW"
    elif Njord_calc > 1000:
        market_size_a = "> 1000MW"
    else:
        market_size_a = "<0"
    return market_size_a




imp_summed = pd.read_csv("Import_summed_NJORD.csv", index_col=0)
exp_summed = pd.read_csv("Export_summed_NJORD.csv", index_col=0)
PV_marksum = pd.read_csv("PV_market_price.csv", index_col=0)

# market_factor_training(imp_summed, exp_summed, PV_marksum, reference_countries)

# mf_test = market_factor_testing(imp_summed, exp_summed, PV_marksum)
# mf_test.to_excel("test.xlsx")
#mf_test = pd.read_excel("test.xlsx")  # , index_col=0)
#ref = check_reference_countries(mf_test, reference_countries)
#ref.to_excel("reference_countries_test.xlsx")

