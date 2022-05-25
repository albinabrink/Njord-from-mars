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


def plot_figure_pearson(price, weight):  # Plots the correlation value between NJORD and ? for the two different models
    x_all_p = []
    y_all_p = []
    # print(price)
    # print(weight)
    for i in price:
        mylist = i.items()
        x, y = zip(*mylist)
        x = x[0]
        y = y[0]
        x_all_p.append(x)
        y_all_p.append(y)
    plt.plot(x_all_p, y_all_p, label="Price")
    x_all_w = []
    y_all_w = []
    for i in weight:
        mylist = i.items()
        x, y = zip(*mylist)
        x = x[0]
        y = y[0]
        x_all_w.append(x)
        y_all_w.append(y)
    plt.plot(x_all_w, y_all_w, label="Weight")
    plt.legend()
    plt.show()
    return


# plot_figure_pearson(corr_Njord_PVPS_ref_price, corr_Njord_PVPS_ref_weight)


def calc_acc_cap(input_data, data_sources):
    data = input_data.loc[:, [data_sources in i for i in input_data]]
    data_acc = pd.DataFrame(index=data.index, columns=data.columns)
    for row in data.index.values:
        N_acc = 0
        for col in data:
            N_acc += data.loc[row, col]
            data_acc.loc[row, col] = N_acc
    return data_acc


Njord_acc_price = calc_acc_cap(price_model_results, "NJORD")
Njord_acc_price.to_excel(path_output+"Njord-Price_acc_all.xlsx")
Njord_acc_weight = calc_acc_cap(weight_model_results, "NJORD")
Njord_acc_weight.to_excel(path_output+"NJORD-Weight_acc_all.xlsx")

def plot_acc_cap(input, reference_countries):  # Not done in the smoothest way, look into making it less complicated
    ref_PVPS = pd.DataFrame()
    ref_Njord = pd.DataFrame()
    Njord = input.loc[:, ["NJORD" in i for i in input.columns]]
    PVPS = input.loc[:, ["PVPS" in i for i in input.columns]]
    Irena = input.loc[:, ["IRENA" in i for i in input.columns]]
    for country in reference_countries:
        ref_Njord = ref_Njord.append(Njord.loc[country])
        ref_PVPS = ref_PVPS.append(PVPS.loc[country])
    njord_acc_price = calc_acc_cap(ref_Njord, "NJORD")
    njord_acc_price.to_excel(path_output+"test_accumulated1.xlsx")
    ref_PVPS_sum = []
    year_columns = []
    test = 0
    for col in ref_PVPS:
        test = sum(ref_PVPS[col])
        ref_PVPS_sum.append(test)
        year_columns.append(col.split(" ")[1])
    ref_PVPS_sum = pd.DataFrame(ref_PVPS_sum, index=year_columns, columns=["Sum PVPS"])
    # print(ref_PVPS_sum)
    plt.plot(ref_PVPS_sum, label="PVPS")
    ref_Njord_sum = []
    year_columns = []
    for col in ref_Njord:
        test = sum(njord_acc_price[col])
        ref_Njord_sum.append(test)
        year_columns.append(col.split(" ")[1])
    ref_Njord_sum = pd.DataFrame(ref_Njord_sum, index=year_columns, columns=["Sum Njord"])
    plt.plot(ref_Njord_sum, label="NJORD")
    plt.legend()
    plt.show()
    return


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


def calc_tot_dev(input):
    Njord = input.loc[:, ["NJORD" in i for i in input.columns]]
    PVPS = input.loc[:, ["PVPS" in i for i in input.columns]]
    Irena = input.loc[:, ["IRENA" in i for i in input.columns]]
    # print(Njord)
    # print(Irena)
    # print(PVPS)
    return

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

def check_missing_countries(data1, data2):
    downloaded_countries = data1["Reporting Country"]
    downloaded_countries = list(downloaded_countries)
    downloaded_countries = list(dict.fromkeys(downloaded_countries))
    country_list = data2[1]
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
    test_with_set = [x for x in name_not_in_partner if x in set(name_not_in_reporting)]
    return not_in_reporting_or_partner

# test1 = pd.read_csv("ITC_yearly_data_HS_6.csv")
# test2 = pd.read_excel("Country_code_list.xlsx")
# check_missing_countries(test1, test2)

def outlier_check(data):
    for name in data.index:
        return


def check_reference_countries(data, reference_countries):
    data = data.loc[data["Unnamed: 0"].isin(reference_countries)]
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
            ref_country_data["NJORD "+col[-6:-2]] = NJORD_placeholder.sum(axis=1)
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
    return ref_country_data


def outlier_check(raw_data):
    imports_country_month = pd.DataFrame()
    exports_country_month = pd.DataFrame()
    periods = list(dict.fromkeys(raw_data["period"]))
    # print(periods)
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = check_missing_countries(raw_data, all_countries)
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
            print(imports_country[country].loc[i])
            z_score = 0.6745*(imports_country[country].loc[i]-median)/MAD
            if z_score.item() > 3.5 or z_score.item() < -3.5:
                outliers_import.at[country, i] = z_score
    for country in exports_country:
        MAD = exports_country[country].mad()
        median = exports_country[country].median()
        for i in exports_country.index:
            z_score = 0.6745*(exports_country[country].loc[i]-median)/MAD
            if z_score.item() > 3.5 or z_score.item() < -3.5:
                outliers_export.at[country, i] = z_score

    outliers_import = outliers_import.transpose()
    outliers_import = outliers_import.sort_index()
    outliers_export = outliers_import.transpose()
    outliers_import = outliers_import.sort_index()
    return outliers_import, outliers_export

#test = pd.read_excel("Test2_NJORD_weight_models_result.xlsx")
#ref = check_reference_countries(test, reference_countries)
#ref.to_excel("reference_countries_weight.xlsx")

outlier_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
outlier_import, outlier_export = outlier_check(outlier_data)
outlier_import.to_excel("Z_outliers_import.xlsx")
