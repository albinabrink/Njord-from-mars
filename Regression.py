import scipy
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns
import Validation_functions
import NJORD_function_test

import os

path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Regressiontest\\"
os.makedirs(path_input, exist_ok=True)


def percent_trade_PV(ten_code_data, six_code_data):
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    periods = list(dict.fromkeys(ten_code_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = NJORD_function_test.check_missing_countries(ten_code_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    trade_not_relevant = pd.DataFrame()
    unit_itc = "Quantity"

    for name in nation_list:
        print(name)
        i = 0
        for period in periods:
            monthly_data_ten = ten_code_data.loc[ten_code_data["period"] == period]
            monthly_data_ten = monthly_data_ten.astype({"productCd": str})
            monthly_data_six = six_code_data.loc[six_code_data["period"] == period]
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
            # print(relevant_codes)
            # Only keep the codes of the month that will be relevant here.
            monthly_data_ten = monthly_data_ten[monthly_data_ten["productCd"].isin(relevant_codes)]
            # Imports and exports a specific period for each specific country. Put in own function and save the results in a CSV-file?
            imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data_ten, name, int(period), "import",
                                                                             unit_itc)
            imports_period = imports_period.groupby(["Partner Country"]).sum()
            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data_ten, name, int(period), "export",
                                                                             unit_itc)
            exports_period = exports_period.groupby(["Partner Country"]).sum()
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            monthly_data_ten = ten_code_data.loc[ten_code_data["period"] == period]
            monthly_data_ten = monthly_data_ten.loc[monthly_data_ten["Partner Country"] == name]
            NTL_codes_rel = pd.DataFrame()
            for country in monthly_data_ten["Reporting Country"]:
                NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
                NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "Yes"]
                NTL_codes_rel = NTL_codes_rel.append(NTL_codes_country)
                # print(NTL_codes_rel)
            relevant_codes = NTL_codes_rel.index.values
            relevant_codes = relevant_codes.tolist()
            # Only keep the codes of the month that will be relevant here.
            monthly_data_ten = monthly_data_ten[monthly_data_ten["productCd"].isin(relevant_codes)]

            exports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data_ten, name, int(period), "import",
                                                                           unit_itc)
            exports_period_mirror = exports_period_mirror.groupby(["Reporting Country"]).sum()
            imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data_ten, name, int(period), "export",
                                                                           unit_itc)
            imports_period_mirror = imports_period_mirror.groupby(["Reporting Country"]).sum()
            imports_period = NJORD_function_test.combine_reported_and_mirror(imports_period, imports_period_mirror)
            exports_period = NJORD_function_test.combine_reported_and_mirror(exports_period, exports_period_mirror)
            if "World" in imports_period:
                imports_period = imports_period.drop(labels="World")
            if "World" in exports_period:
                exports_period = exports_period.drop(labels="World")
            # exports_period_quarter = pd.DataFrame()
            # imports_period_quarter = pd.DataFrame()
            # print(imports_period_quarter)

            # exports_period = NJORD_function_test.remove_large_exporters(exports_period)

            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values

            percentage_imp, sum_imports = NJORD_function_test.calc_percentage_import_or_export(nations_within_imp,
                                                                                               imports_period)
            percentage_exp, sum_exports = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp,
                                                                                               exports_period)

            # 6-digits level
            imports_period_six = NJORD_function_test.imports_or_export_in_period(monthly_data_six, name, int(period),
                                                                                 "import", unit_itc)
            exports_period_six = NJORD_function_test.imports_or_export_in_period(monthly_data_six, name, int(period),
                                                                                 "export", unit_itc)
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror_six = NJORD_function_test.create_mirror_data(monthly_data_six, name, int(period),
                                                                               "import", unit_itc)
            imports_period_mirror_six = NJORD_function_test.create_mirror_data(monthly_data_six, name, int(period),
                                                                               "export", unit_itc)
            imports_period_six = NJORD_function_test.combine_reported_and_mirror(imports_period_six, imports_period_mirror_six)
            exports_period_six = NJORD_function_test.combine_reported_and_mirror(exports_period_six, exports_period_mirror_six)

            # exports_period_six = NJORD_function_test.remove_large_exporters(exports_period_six)
            nations_within_imp = imports_period_six.index.values
            nations_within_exp = exports_period_six.index.values

            percentage_imp, sum_imports_six = NJORD_function_test.calc_percentage_import_or_export(nations_within_imp,
                                                                                               imports_period_six)
            # Add a check for export to large exporter, and remove them.
            percentage_exp, sum_exports_six = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp,
                                                                                               exports_period_six)

            if name in reference.index.values:
                trade_not_relevant.at[name + " 10-code import", period] = sum_imports
                trade_not_relevant.at[name + " 10-code export", period] = sum_exports
                trade_not_relevant.at[name + " 6-code import", period] = sum_imports_six
                trade_not_relevant.at[name + " 6-code export", period] = sum_exports_six
    return trade_not_relevant


six = pd.read_csv("ITC_Monthly_data_HS_6.csv")
ten = pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str})
check_amount = percent_trade_PV(ten, six)
check_amount.to_excel("To_calculate_percentage_of_PV_weight.xlsx")

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
            export_data = one_year.iloc[n+1:n + 5:2, ]
            # print(import_data)
            percent_import = import_data.iloc[0]/import_data.iloc[1]
            percent_export = export_data.iloc[0]/export_data.iloc[1]
            junkwords = ["10-code", "6-code"]
            country_imp = [word for word in import_data.index[0].split() if word not in junkwords]
            country_exp = [word for word in export_data.index[0].split() if word not in junkwords]
            country_imp = " ".join(country_imp)
            country_exp = " ".join(country_exp)
            PV_share_in_ten_code.at[country_imp, str(i)] = percent_import
            PV_share_in_ten_code.at[country_exp, str(i)] = percent_export
            n += 4
        # print(PV_share_in_ten_code)
        i = i + 1
        print(i)
    print(PV_share_in_ten_code)
    PV_share_in_ten_code = PV_share_in_ten_code.fillna(0)
    PV_share_in_ten_code = PV_share_in_ten_code.replace([np.inf, -np.inf], 0)
    print(PV_share_in_ten_code)
    return PV_share_in_ten_code


trade_data = pd.read_excel("To_calculate_percentage_of_PV_weight.xlsx", index_col=0)
trade_data = calculate_percentage_of_PV(trade_data)
trade_data.to_excel("share_in_PV_weight.xlsx")


def europe_trade_US(ten_codes):
    EU_countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark",
                    "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia",
                    "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
                    "Slovenia", "Spain", "Sweden"]
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    NTL_codes_EU_US = NTL_codes[NTL_codes["countryCd"].isin(EU_countries)]
    NTL_codes_EU_US = NTL_codes_EU_US.append(NTL_codes[NTL_codes["countryCd"] == "United States of America"])
    # NTL_codes_EU_US.to_excel("NTL_codes_US_EU.xlsx")
    EU_trade_US = ten_codes.loc[ten_codes["Reporting Country"].isin(EU_countries)]
    EU_trade_US = EU_trade_US.loc[EU_trade_US["Partner Country"] == "United States of America"]
    EU_trade_US = EU_trade_US.astype({"productCd": str})
    US_reported_trade = ten_codes.loc[ten_codes["Reporting Country"] == "United States of America"]
    US_reported_trade = US_reported_trade.loc[US_reported_trade["Partner Country"].isin(EU_countries)]
    US_reported_trade = US_reported_trade.astype({"productCd": str})
    US_reported_trade.to_excel("US_reported_trade_EU_10code.xlsx")
    EU_trade_US.to_excel("EU_reported_trade_US_10code.xlsx")

    NTL_codes_rel = pd.DataFrame()
    for country in EU_trade_US["Reporting Country"]:
        NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
        NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "Yes"]
        NTL_codes_rel = NTL_codes_rel.append(NTL_codes_country)
        # print(NTL_codes_rel)
    relevant_codes = NTL_codes_rel.index.values
    relevant_codes = relevant_codes.tolist()
    EU_trade_US = EU_trade_US[EU_trade_US["productCd"].isin(relevant_codes)]
    NTL_codes_US = NTL_codes[NTL_codes["countryCd"] == "United States of America"]
    NTL_codes_US = NTL_codes_US.loc[NTL_codes_US["PV?"] == "Yes"]
    # print(US_reported_trade[US_reported_trade["productCd"] == 8541406020])
    US_reported_trade = US_reported_trade[US_reported_trade["productCd"].isin(NTL_codes_US.index)]
    print(US_reported_trade)
    EU_trade_US.to_excel("EU_10code_trade_US_cert_codes.xlsx")
    US_reported_trade.to_excel("US_10code_EU_cert_codes.xlsx")
    return

# europe_trade_US(pd.read_csv("ITC_Monthly_data_HS_10.csv"))

def sort_into_area_Africa(file):
    north_of_sahara = ["Algeria", "Egypt", "Libya", "Morocco", "Tunisia"]
    west_africa = ["Benin", "Burkina Faso", "Cabo Verde", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Liberia",
                   "Mali", "Mauritania", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo", "Côte dIvoire"]
    central_africa = ["Angola", "Cameroon", "Central African Republic", "Chad", "Democratic Republic of the Congo",
                      "Congo", "Equatorial Guinea", "Gabon", "Sao Tome and Principe"]
    east_africa = ["Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Malawi",
                   "Mauritius", "Mozambique", "Rwanda", "Seychelles", "Somalia", "Uganda", "Tanzania", "Zambia",
                   "Zimbabwe", "Sudan", "South Sudan"]
    south_africa = ["South Africa", "Eswatini", "Lesotho", "Namibia", "Botswana"]
    for country in file.index.values:
        if country in north_of_sahara:
            area = "North of Sahara"
        elif country in central_africa:
            area = "Central Africa"
        elif country in east_africa:
            area = "East Africa"
        elif country in west_africa:
            area = "West Africa"
        elif country in south_africa:
            area = "Southern Africa"
        else:
            print(country)
        file.at[country, "Area"] = area
    print(file)
    return file

def correlation_statistics_africa(Njord):
    path_output = "Regressiontest\\Correlation files\\"
    # os.makedirs(path_output, exist_ok=True)

    african_countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
                        "Central African Republic", "Chad", "Comoros", "Congo, Dem. Rep.", "Congo, Rep.",
                        "Djibouti", "Egypt, Arab Rep.", "Equatorial Guinea", "Eritrea", "Eswatini",
                        "Ethiopia", "Gabon", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                        "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
                        "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
                        "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania",
                        "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"] # "Côte d'Ivoire"

    GDP = pd.read_csv(path_input + "GDP_World.csv", index_col=0)
    GDPperC = pd.read_csv(path_input + "GDP per capita.csv", index_col=0)
    Oilprices = pd.read_excel(path_input + "Oil_prices.xlsx", index_col=0)
    education_rate = pd.read_csv(path_input + "percent_graduating_primary_school.csv", index_col=0)
    education_rate.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    education_rate = education_rate.replace("..", np.nan)
    education_rate = education_rate.astype(float)
    electrification_rate = pd.read_csv(path_input + "Access to electricity Africa.csv", index_col=0)
    electrification_rate.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    electrification_rate = electrification_rate.replace("..", np.nan)
    electrification_rate = electrification_rate.astype(float)
    electrification_rate_rural = pd.read_csv(path_input + "Access to electricity Rural.csv", index_col=0)
    electrification_rate_rural.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    electrification_rate_rural = electrification_rate_rural.replace("..", np.nan)
    electrification_rate_rural = electrification_rate_rural.astype(float)
    electrification_rate_urban = pd.read_csv(path_input + "Access to electricity Urban.csv", index_col=0)
    electrification_rate_urban.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    electrification_rate_urban = electrification_rate_urban.replace("..", np.nan)
    electrification_rate_urban = electrification_rate_urban.astype(float)
    clean_fuels = pd.read_csv(path_input + "Access_to_clean_fuels.csv", index_col=0)
    clean_fuels.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
    clean_fuels = clean_fuels.replace("..", np.nan)
    clean_fuels = clean_fuels.astype(float)
    correlation_Njord_acc = pd.DataFrame()
    correlation_Njord_yearly = pd.DataFrame()
    Oilprices = Oilprices[2:-5]
    n = 2010
    oil_price_yearavg = pd.DataFrame()
    for x in range(0, len(Oilprices.index), 12):
        oilprice = Oilprices[x:x+12]
        oilprice_mean = oilprice.mean()
        oilprice_mean.name = str(n)
        oil_price_yearavg = oil_price_yearavg.append(oilprice_mean)
        n += 1

    Njord = Njord.loc[:, [col for col in Njord.columns if "NJORD" in col]]

    for country in african_countries:
        country_data = pd.DataFrame()
        country_data = country_data.append(GDP.loc[country, :])
        country_data = country_data.append(GDPperC.loc[country, :])
        country_data = country_data.append(electrification_rate.loc[country, :])
        country_data = country_data.append(electrification_rate_rural.loc[country, :])
        country_data = country_data.append(electrification_rate_urban.loc[country, :])
        country_data = country_data.append(clean_fuels.loc[country, :])
        country_data = country_data.append(education_rate.loc[country, :])
        country_data = country_data.append(oil_price_yearavg.transpose())
        if country == "Congo, Dem. Rep.":
            country = "Democratic Republic of the Congo"
        if country == "Congo, Rep.":
            country = "Congo"
        if country == "Egypt, Arab Rep.":
            country = "Egypt"
        if country == "Eswatini" or country == "Guinea-Bissau":
            continue
        if country == "Gambia, The":
            country = "Gambia"
        n = 2010
        Njord_yearly = pd.DataFrame()
        while n < 2022:
            Njord_year_sum = Njord.loc[country, [col for col in Njord.columns if str(n) in col]]
            Njord_year_sum = Njord_year_sum.sum()
            Njord_yearly.at["Njord", str(n)] = Njord_year_sum
            n += 1
        Njord_year = 0
        Njord_acc = pd.DataFrame()
        n = 0
        while n < len(Njord_yearly.columns):
            Njord_year += Njord_yearly.iloc[0][n]
            Njord_acc.at["Njord_acc", str(2010+n)] = Njord_year
            n += 1
        country_data = country_data.append(Njord_yearly)
        country_data = country_data.append(Njord_acc)
        country_data.index = ["GDP", "GDP_per_capita", "Electrification_rate", "Electrification_rate_Rural",
                              "Electrification_rate_Urban", "Access_to_clean_cooking_fuels", "Education_rate", "USOilprice",
                              "Njord_yearly", "Njord_acc"]
        country_data = country_data.transpose()
        country_data.drop(["2010", "2011", "2021"], axis=0, inplace=True)
        # sns.pairplot(country_data, kind="scatter")
        # plt.show()
        matrix = country_data.corr()
        matrix.to_excel(path_output + country + "_corr_matrix.xlsx")
        matrix["Njord_acc"].name = country
        matrix["Njord_yearly"].name = country
        correlation_Njord_acc = correlation_Njord_acc.append(matrix["Njord_acc"])
        correlation_Njord_yearly = correlation_Njord_yearly.append(matrix["Njord_yearly"])
        country_data.to_excel(path_output + country + ".xlsx")
    correlation_Njord_acc = sort_into_area_Africa(correlation_Njord_acc)
    correlation_Njord_yearly = sort_into_area_Africa(correlation_Njord_yearly)
    correlation_Njord_acc.to_excel(path_output + "Njord_acc_corr.xlsx")
    correlation_Njord_yearly.to_excel(path_output + "Njord_yearly_corr.xlsx")
    return

def open_SDG_data():
    african_countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde", "Cameroon",
                         "Central African Republic", "Chad", "Comoros", "Democratic Republic of Congo", "Congo", "Cote d'Ivoire",
                         "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini",
                         "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                         "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
                         "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
                         "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania",
                         "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]
    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    idx = pd.IndexSlice
    # The path to where the SDG data files are stored, needs to be changed if running on another computer.
    path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Regressiontest\\SDG\\"
    os.makedirs(path_input, exist_ok=True)
    country_data = pd.DataFrame()
    # Loops through the files in the folder, opens and reads them, copies them to a new file if they are in the right
    # timeperiod and in the list of nations, here african_countries.
    for single_file in os.listdir(path_input):
        SDG_data = pd.read_csv(path_input + single_file)#, index_col=0)
        SDG_data = SDG_data.set_index(["Entity", "Year"])
        # SDG_data = SDG_data.loc[idx[:, african_countries], :]
        SDG_data = SDG_data.loc[idx[african_countries, years], :]
        for column in SDG_data.columns.values:
            if column == "Code":
                continue
            elif column in country_data.columns.values:
                continue
            country_data[str(column)] = SDG_data[column]
    country_data.to_excel("SDG_test.xlsx")
            # print(pd.read_csv(path_input + single_file, index_col=0).columns)


# open_SDG_data()
# correlation_statistics_africa(pd.read_excel("Test_NJORD-Price_model_results_10codes_pvshareremoved.xlsx", index_col=0))
def corr_stats_africa(Njord):
    african_countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde", "Cameroon",
                         "Central African Republic", "Chad", "Comoros", "Democratic Republic of Congo", "Congo", "Cote d'Ivoire",
                         "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini",
                         "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                         "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
                         "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
                         "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania",
                         "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]
    SDG_data = pd.read_excel("SDG_test.xlsx", index_col=[0, 1])
    print(SDG_data)
    correlation_Njord_acc = pd.DataFrame()
    correlation_Njord_yearly = pd.DataFrame()
    SDG_data_country_corr_spearman = pd.DataFrame()
    Njord = Njord.loc[:, [col for col in Njord.columns if "NJORD" in col]]
    for country in african_countries:
        # print(SDG_data.loc[country, :])#.loc["Access to electricity (% of population)"])
        SDG_data_country = SDG_data.loc[country, :]
        # print(SDG_data_country.corr())
        if country == "Eswatini" or country == "Guinea-Bissau":
            continue
        if country == "Cape Verde":
            country = "Cabo Verde"
        if country == "Democratic Republic of Congo":
            country = "Democratic Republic of the Congo"
        # if country == "Congo, Rep.":
        #    country = "Congo"
        if country == "Egypt, Arab Rep.":
            country = "Egypt"
        if country == "Gambia, The":
            country = "Gambia"
        if country == "Cote d'Ivoire":
            country = "Côte dIvoire"
        n = 2010
        Njord_yearly = pd.DataFrame()
        while n < 2021:
            Njord_year_sum = Njord.loc[country, [col for col in Njord.columns if str(n) in col]]
            Njord_year_sum = Njord_year_sum.sum()
            Njord_yearly.at["Njord", n] = Njord_year_sum
            n += 1
        Njord_year = 0
        Njord_acc = pd.DataFrame()
        n = 0
        y = 2010
        while n < len(Njord_yearly.columns):
            Njord_year += Njord_yearly.loc["Njord"][y]
            Njord_acc.at["Njord_acc", 2010 + n] = Njord_year
            n += 1
            y += 1
        Njord_acc = Njord_acc.transpose()
        Njord_yearly = Njord_yearly.transpose()
        # Creates a warning, I don't get how to solve the warning and still have a working solution
        SDG_data_country["Njord_acc"] = Njord_acc
        SDG_data_country["Njord_yearly"] = Njord_yearly
        SDG_data_country_corr = SDG_data_country.corr()
        SDG_data_country_corr_spear = SDG_data_country.corr(method="spearman")
        SDG_data_country_corr_spear["Njord_acc"].name = country
        SDG_data_country_corr_spearman = SDG_data_country_corr_spearman.append(SDG_data_country_corr_spear["Njord_acc"])
        SDG_data_country_corr_spearman.to_excel("Spearman_analysis_test.xlsx")
        SDG_data_country_corr["Njord_acc"].name = country
        SDG_data_country_corr["Njord_yearly"].name = country
        correlation_Njord_acc = correlation_Njord_acc.append(SDG_data_country_corr["Njord_acc"])
        correlation_Njord_yearly = correlation_Njord_yearly.append(SDG_data_country_corr["Njord_yearly"])
    correlation_Njord_acc = sort_into_area_Africa(correlation_Njord_acc)
    correlation_Njord_yearly = sort_into_area_Africa(correlation_Njord_yearly)
    correlation_Njord_acc.to_excel("Njord_acc_corr.xlsx")
    correlation_Njord_yearly.to_excel("Njord_yearly_corr.xlsx")

corr_stats_africa(pd.read_excel("Test_NJORD-Price_model_results_10codes_pvshareremoved.xlsx", index_col=0))
