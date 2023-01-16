# Code for validation of data in NJORD.
import warnings
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
import NJORD_functions

warnings.simplefilter(action='ignore', category=FutureWarning)

# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok=True)
reference_countries = ["Australia", "Belgium", "Chile", "Denmark", "Finland", "France", "Israel", "Italy", "Japan",
                       "Spain", "Sweden", "Switzerland", "United States of America"]


def check_reference_countries(data, reference_countries):
    data = data.loc[data["Unnamed: 0"].isin(reference_countries)]
    # data = data.loc[data.index.isin(reference_countries)]
    ref_country_data = pd.DataFrame()
    ref_country_data.insert(0, "country", data["Unnamed: 0"], True)
    # ref_country_data.insert(0, "Country", data["Country"], True)
    for col in data.columns:
        cutoff = 2014
        if type(col) == int:
            print(col)
            continue
        if "NJORD" in col:
            NJORD_placeholder = data.loc[:, [col[-6:-2] in i for i in data.columns]]
            NJORD_placeholder = NJORD_placeholder.loc[:, ~NJORD_placeholder.columns.duplicated()]
            NJORD_placeholder = NJORD_placeholder.loc[:, ["NJORD" in i for i in NJORD_placeholder.columns]]
            ref_country_data["NJORD " + col[-6:-2]] = NJORD_placeholder.sum(axis=1)
        if "PVPS" in col:
            if int(col[-4:]) >= cutoff:
                ref_country_data[col] = data[col]
    i = 2014
    while i < 2022:
        diff = ref_country_data["NJORD "+str(i)] - ref_country_data["PVPS " + str(i)]
        ref_country_data["DIFF "+str(i)] = diff
        ref_country_data["Percent Diff "+str(i)] = (diff/ref_country_data["PVPS "+str(i)])
        i += 1
    # ref_country_data = ref_country_data.set_index(ref_country_data.iloc[:]["country"])
    # ref_country_data = ref_country_data.drop(columns="country")
    i = 2014
    while i < 2022:
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
    country_not_in_data = NJORD_functions.check_missing_countries(raw_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    outliers_import = pd.DataFrame()
    outliers_export = pd.DataFrame()
    for nation in nation_list:
        for period in periods:
            monthly_data = raw_data.loc[raw_data["period"] == period]
            imports_period = NJORD_functions.imports_or_export_in_period(monthly_data, nation, int(period), "import",
                                                                             "Value")
            exports_period = NJORD_functions.imports_or_export_in_period(monthly_data, nation, int(period), "export",
                                                                             "Value")
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror = NJORD_functions.create_mirror_data(monthly_data, nation, int(period), "import",
                                                                           "Value")
            imports_period_mirror = NJORD_functions.create_mirror_data(monthly_data, nation, int(period), "export",
                                                                           "Value")
            imports_period = NJORD_functions.combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = NJORD_functions.combine_reported_and_mirror(exports_period, exports_period_mirror)

            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values

            percentage_imp, sum_imports = NJORD_functions.calc_percentage_import_or_export(nations_within_imp,
                                                                                               imports_period)
            # Add a check for export to large exporter, and remove them.
            percentage_exp, sum_exports = NJORD_functions.calc_percentage_import_or_export(nations_within_exp,
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

test = pd.read_excel("NJORD-Price_model_final_results.xlsx")
# print(test)
ref = check_reference_countries(test, reference_countries)
ref.to_excel("reference_countries_Price_final_results.xlsx")

# outlier_data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
# outlier_import, outlier_export = outlier_check(outlier_data)
# outlier_import.to_excel("Z_outliers_import.xlsx")
# outlier_export.to_excel("Z_outliers_export.xlsx")


def calc_PV_market_price(imp_or_exp_data, change, year, month, Europe):
    PV_market_price = 0
    nations_within = imp_or_exp_data.index.values
    change_list = change.index.values
    year_quarter = NJORD_functions.add_quarter(year, month)
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


#imp_summed, exp_summed, PV_marksum, net_trade = sort_out_data(pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str}))
##imp_summed.to_csv("Import_summed_NJORD.csv")
#exp_summed.to_csv("Export_summed_NJORD.csv")
#PV_marksum.to_csv("PV_market_price.csv")

def prel_market_size(net_trade, month, all_market_factors):
    change = pd.read_excel("PVxchange.xlsx", index_col=0)  # Read the cost of panels from big producers
    year_quarter = NJORD_functions.add_quarter(month[:4], month[4:])
    # Preliminary Market size:
    prel_MS = (net_trade / change[year_quarter]["RoW"]) / 10 ** 6
    # print(prel_MS,"prel")
    if prel_MS < 0:
        prel_MS = abs(prel_MS)
    if prel_MS == 0:
        market_factor = 1
    elif 0 < prel_MS <= 1:
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
    year, month = NJORD_functions.add_time_shift(3, int(year), int(month))
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

def visualise_the_results(data):
    # print(test)
    ref = check_reference_countries(data, reference_countries)
    # ref = ref.set_index("country")
    ref_njord = ref.filter(like="NJORD")
    ref_pvps = ref.filter(like="PVPS")
    ref_njord_summed = ref_njord.iloc[-1, :]
    ref_pvps_summed = ref_pvps.iloc[-1, :]
    print(ref_pvps_summed)
    print(ref_njord_summed)
    ref_pvps_summed.index = range(2014, 2023) #ref_pvps_summed.reindex(years)
    ref_njord_summed.index = range(2010, 2023)
    plt.plot(ref_njord_summed, label="NJORD")
    plt.plot(ref_pvps_summed, label="PVPS")
    plt.ylabel("Installed capacity [MW]")
    plt.grid(axis="y")
    # ax1 = ref_njord.A.plot(color='blue', grid=True, label='NJORD')
    # ax2 = ref_pvps.B.plot(color='red', grid=True, secondary_y=True, label='PVPS')
    plt.show()
    # ref.to_excel("reference_countries_Weight_10codes_test_only_kilos.xlsx")
    return


def market_factor_training(imp_summed, exp_summed, PV_marksum, ref):  # Used to calculate the new market factors
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
    market_factor_count = pd.DataFrame(np.zeros((12, 8)),
                                       columns=["<0", "0-1", "1-5", "5-10", "10-100", "100-500", "500-1000", ">1000"],
                                       index=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018",
                                              "2019", "2020", "2021"])
    for nation in imp_summed_ref.index.values:
        for month in imp_summed_ref.columns.values:
            net_trade = (imp_summed_ref.loc[nation][month]-exp_summed_ref.loc[nation][month]) * 1000
            net_trade_df.at[nation, month] = net_trade
            market_factor, prel_ms = prel_market_size(net_trade_df.loc[nation][month], month, mf)
            prel_ms_cat.at[nation, month] = prel_ms
            market_factor_count = market_factor_test_calculation(prel_ms_cat.loc[nation][month], market_factor_count,
                                                                 month[:-2])
    net_trade_test = (imp_summed_ref-exp_summed_ref)*1000
    print(net_trade_df)
    for i in range(0, 100):
        print(i)
        for nation in net_trade_df.index.values:
            for month in net_trade_df.columns.values:
                manufacturing_value = NJORD_functions.manufacturing(nation, str(month[:4]), manufacturing_df)
                # Minimize the abs deviation changing the market factors
                market_factor, prel_ms = prel_market_size(net_trade_df.loc[nation][month], month, mf)
                installed_capacity = ((net_trade_df.loc[nation][month]/(PV_marksum.loc[nation][month]*market_factor))/(10**6)) + (manufacturing_value/12)
                name = NJORD_functions.name_cleanup(nation, month[:4])
                if name in reference.index.values:
                    output_P_each_year, output_P_MF_each_year = create_output_price(reference, str(month[:4]), month[4:], name,
                                                                                installed_capacity,
                                                                                installed_capacity,
                                                                                output_P_each_year,
                                                                                output_P_MF_each_year)
        output_P_MF_each_year.to_excel("testest.xlsx")
        mf_test = pd.read_excel("testest.xlsx")
        visualise_the_results(mf_test)
        ref = check_reference_countries(mf_test, reference_countries)
        mf_test = mf_test.set_index("Unnamed: 0")
        ref = ref.set_index("country")
        ref_absdiff = ref.filter(like="AbsDiff")
        ref_diff = ref.filter(like="DIFF")
        print(ref_absdiff_best)
        market_factor_count = pd.DataFrame(np.zeros((2, 8)),
                                           columns=["<0MW", "0-1MW", "1-5MW", "5-10MW", "10-100MW", "100-500MW", "500-1000MW", "> 1000MW"],
                                           index=["higher", "lower"])
        if ref_absdiff.iloc[-1].sum() < ref_absdiff_best:
            ref_absdiff_best = ref_absdiff.iloc[-1].sum()
            print(ref_absdiff_best)
            mf_best = mf
            print(mf_best.to_string())
            # print("End of loop " + str(i))
        for country in net_trade_df.index.values:
            for month in net_trade_df.columns.values:
                if month[:-2] == "2010" or month[:-2] == "2011" or month[:-2] == "2012" or month[:-2] == "2013":
                    continue
                market_size_month = market_size(abs(mf_test.loc[country]["NJORD " + month]))
                if ref_diff.loc[country]["DIFF "+month[:-2]] <= 0:
                    market_factor_count.at["lower", market_size_month] += 1
                else:
                    market_factor_count.at["higher", market_size_month] += 1
        print(market_factor_count)
        for column in market_factor_count:
            if market_factor_count.loc["higher"][column] > market_factor_count.loc["lower"][column]:
                mf[column] *= 1.1
            else:
                mf[column] *= .9

    print(mf_best)
    return


def market_factor_test_calculation(prel_ms, market_factor_count, year):
    if prel_ms <= 0:
        market_factor_count.loc[str(year)]["<0"] += 1
    elif 0 < prel_ms <= 1:
        market_factor_count.loc[str(year)]["0-1"] += 1
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
    if 0 < Njord_calc <= 1:
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
        market_size_a = "<0MW"
    return market_size_a


imp_summed = pd.read_csv("Imports_summed_Price_last_test.csv", index_col=0)
exp_summed = pd.read_csv("Exports_summed_Price_last_test.csv", index_col=0)
PV_marksum = pd.read_csv("PVxchange_summed_Price_last_test.csv", index_col=0)


market_factor_training(imp_summed, exp_summed, PV_marksum, reference_countries)

# test = pd.read_excel("NJORD-Combined_model_results_cells.xlsx")
#test = pd.read_excel("testest.xlsx")
# visualise_the_results(test)


