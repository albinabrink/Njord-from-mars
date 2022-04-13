# Code for validation of data in the NJORD data using Pearsons coefficient, Central limit theorem and t-distribution
# and mean absolute deviation (|u|) and total deviation.

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

# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok=True)
price_model_results = pd.read_excel("NJORD-Price_model_results_year.xlsx", index_col=0, na_values=['NA'])
weight_model_results = pd.read_excel("NJORD-Weight_model_results_year.xlsx", index_col=0, na_values=['NA'])
# reference_data = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])
reference_countries = ["Australia", "Belgium", "Chile", "Denmark", "Finland", "France", "Israel", "Italy", "Japan",
                       "Spain", "Sweden", "Switzerland", "United States of America"]

def Pearson_coef(input, reference_countries, unit):
    # Calculates the Pearson Coefficient between NJORDs data and reference data (IRENA and PVPS)
    # Only for reference countries from thesis and PVPS now, will add check for emerging markets later
    Njord = pd.DataFrame()
    Irena = pd.DataFrame()
    PVPS = pd.DataFrame()
    for data_source in input:
        if "NJORD" in data_source:
            Njord[data_source] = input[data_source]
        if "IRENA" in data_source:
            Irena[data_source] = input[data_source]
        if "PVPS" in data_source:
            PVPS[data_source] = input[data_source]
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
    print(ref_Njord)
    print(ref_PVPS)
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


corr_Njord_Irena_price, corr_Njord_PVPS_price, corr_Njord_PVPS_ref_price = Pearson_coef(price_model_results, reference_countries, "Price")
corr_Njord_Irena_weight, corr_Njord_PVPS_weight, corr_Njord_PVPS_ref_weight = Pearson_coef(weight_model_results, reference_countries, "Weight")


def plot_figure_pearson(price, weight):  # Plots the correlation value between NJORD and ? for the two different models
    x_all_p = []
    y_all_p = []
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


def calc_acc_cap(input, data_sources):
    data = pd.DataFrame()
    for data_source in input:
        if data_sources in data_source:
            data[data_source] = input[data_source]
    data_acc = pd.DataFrame(index=data.index, columns=data.columns)
    for row in data.index.values:
        N_acc = 0
        for col in data:
            N_acc += data.loc[row, col]
            data_acc.loc[row, col] = N_acc
    return data_acc


# Njord_acc_price = calc_acc_cap(price_model_results, "NJORD")


def plot_acc_cap(input, reference_countries):
    PVPS = pd.DataFrame()
    Njord = pd.DataFrame()
    ref_PVPS = pd.DataFrame()
    ref_Njord = pd.DataFrame()
    for data_source in input:
        if "PVPS" in data_source:
            PVPS[data_source] = input[data_source]
        if "NJORD" in data_source:
            Njord[data_source] = input[data_source]
    for country in reference_countries:
        ref_Njord = ref_Njord.append(Njord.loc[country])
        ref_PVPS = ref_PVPS.append(PVPS.loc[country])
    njord_acc_price = calc_acc_cap(ref_Njord, "NJORD")
    njord_acc_price.to_excel(path_output+"test_accumulated1.xlsx")
    ref_Njord_sum = []
    for col in ref_Njord:
        test = sum(njord_acc_price[col])
        ref_Njord_sum.append(test)
    print(ref_Njord_sum)
    plt.plot(ref_Njord_sum, label="NJORD")
    ref_PVPS_sum = []
    test = 0
    for col in ref_PVPS:
        test = sum(ref_PVPS[col])
        ref_PVPS_sum.append(test)
    print(ref_PVPS_sum)
    plt.plot(ref_PVPS_sum, label="PVPS")
    plt.legend()
    plt.show()
    return


plot_acc_cap(price_model_results, reference_countries)


def calc_mean_abs_dev(input, reference_countries):
    Njord = pd.DataFrame()
    Irena = pd.DataFrame()
    PVPS = pd.DataFrame()
    for data_source in input:
        if "NJORD" in data_source:
            Njord[data_source] = input[data_source]
        if "IRENA" in data_source:
            Irena[data_source] = input[data_source]
        if "PVPS" in data_source:
            PVPS[data_source] = input[data_source]
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
    Njord = pd.DataFrame()
    Irena = pd.DataFrame()
    PVPS = pd.DataFrame()
    for data_source in input:
        if "NJORD" in data_source:
            Njord[data_source] = input[data_source]
        if "IRENA" in data_source:
            Irena[data_source] = input[data_source]
        if "PVPS" in data_source:
            PVPS[data_source] = input[data_source]
    # print(Njord)
    # print(Irena)
    # print(PVPS)
    return

def histogram(input):
    Njord = pd.DataFrame()
    Irena = pd.DataFrame()
    PVPS = pd.DataFrame()
    for data_source in input:
        if "NJORD" in data_source:
            Njord[data_source] = input[data_source]
        if "IRENA" in data_source:
            Irena[data_source] = input[data_source]
        if "PVPS" in data_source:
            PVPS[data_source] = input[data_source]
    # sns.set_style('white')
    # sns.set_context("paper", font_scale=2)
    # sns.displot(Njord, x="NJORD 2019", kind="hist", bins=100)

    # (Njord.apply(stats.zscore))
    plt.hist(Njord["NJORD 2019"], bins=100)
    plt.show()


def calculate_standard_deviation(data):
    standard_deviation = statistics.stdev(data)
    return standard_deviation

def standard_deviation_all_countries(data):
    stdev_year = []
    stdev_countries = []
    for country in data.index:
        stdev_country = []
        for col in data:
            if "NJORD" in col:
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

standard_deviation_all_countries(price_model_results)

calc_mean_abs_dev(price_model_results, reference_countries)
# histogram(price_model_results)

