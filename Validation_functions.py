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
import os

# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok=True)
price_model_results = pd.read_excel("NJORD-Price_model_results_year.xlsx", index_col=0, na_values=['NA'])
weight_model_results = pd.read_excel("NJORD-Weight_model_results_year.xlsx", index_col=0, na_values=['NA'])
# reference_data = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])
reference_countries = ["Australia", "Belgium", "Chile", "Denmark", "Finland", "France", "Israel", "Italy", "Japan",
                       "Spain", "Sweden", "Switzerland", "United States of America"]
# print(price_model_results.columns)

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
            if country != "Australia" and country != "Japan" and country != "United States of America":
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


corr_Njord_Irena_price, corr_Njord_PVPS_price, corr_Njord_PVPS_ref_price = Pearson_coef(price_model_results, reference_countries, "Price")
corr_Njord_Irena_weight, corr_Njord_PVPS_weight, corr_Njord_PVPS_ref_weight = Pearson_coef(weight_model_results, reference_countries, "Weight")


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
    print(mad_PVPS)

    return


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
    pyplot.hist(Njord["NJORD 2019"], bins=100)
    pyplot.show()

# calc_mean_abs_dev(price_model_results, reference_countries)
# histogram(price_model_results)

