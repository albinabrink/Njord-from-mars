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

# IRENA_data = pd.read_excel(path_input + "Off-grid_Renewable_Energy_Statistics_2021.xlsx", index_col=0)
# electrification_rate_africa = pd.read_csv(path_input + "Access to electricity Africa.csv", index_col=0)
# trade_data = pd.read_excel(path_input + "Test_NJORD-Price_model_results.xlsx", index_col=0)
# Africa = ["Algeria", "Angola", "Benin", "Botswana", "Burkina_Faso", "Burundi", "Cameroon", "Cabo_Verde",
#          "Central_African_Republic", "Comoros", "Congo", "Congo__Democratic_Republic_of_the", "Djibouti", "Egypt",
#          "Equatorial_Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea_Bissau",
#          "Côte_d'Ivoire", "Kenya", "Lesotho", "Liberia", "Libya__State_of", "Mayotte", "Madagascar", "Malawi", "Mali",
#          "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Saint_Helena",
#          "Sao_Tome_and_Principe", "Senegal", "Seychelles", "Sierra_Leone", "Somalia", "South_Africa", "South_Sudan",
#          "Sudan", "Tanzania__United_Republic_of", "Togo", "Tunisia", "Uganda", "Western_Sahara", "Zambia", "Zimbabwe"]
# print(IRENA_data)
# print(electrification_rate_africa)
# print(trade_data)


def test_correlation(IRENA_data, electrification_rate_africa, trade_data):
    df = pd.DataFrame()
    for country in electrification_rate_africa.index:
        if country not in IRENA_data.index:
            continue
        if country not in trade_data.index:
            continue
        country_IRENA = IRENA_data.loc[country]
        country_IRENA = country_IRENA.rename(country+"_IRENA")
        country_elec_rate = electrification_rate_africa.loc[country]
        country_elec_rate = country_elec_rate.rename(country+"_elec")
        country_Njord = trade_data.loc[:, ["NJORD" in x for x in trade_data.columns]]
        country_Njord = country_Njord.loc[country]
        country_Njord_year = pd.Series(name=country+"_NJORD")
        i = 0
        while i < 132:
            sum_NJORD_year = country_Njord.iloc[i:i+12].sum()
            year = 2010+(i/12)
            country_Njord_year[str(int(year))] = sum_NJORD_year
            i += 12
        country_Njord_year = country_Njord_year.dropna()
        country_IRENA = country_IRENA.dropna()
        country_elec_rate = country_elec_rate.iloc[:][-12:]
        country_elec_rate = country_elec_rate.dropna()
        # country_elec_rate.settype("float64")
        # country_elec_rate,, IRENA_data)
        df[country+'_elec'] = country_elec_rate
        df[country+"_NJORD"] = country_Njord_year
        df[country+"_IRENA"] = country_IRENA
        print(df)
        print(country_IRENA)
        print(country_elec_rate)
        print(country_Njord_year)
        # corr_I_N = country_Njord_year.corr(country_IRENA)
        # corr_E_N = country_Njord_year.corr(country_elec_rate)
        # corr_E_I = country_IRENA.corr(country_elec_rate)
        # corr = df.corr()
        # print(corr)
        # model = LinearRegression()
        # model.fit(country_elec_rate, country_IRENA)
        # R_E_I = model.score(country_elec_rate, country_IRENA)
        # print(country, f"coefficient of determination: {R_E_I}")

        #print(country, f"Correlation Irena_SHS and NJORD {corr_I_N}", f"Correlation electrification rate and NJORD {corr_E_N}", f"Correlation IRENA_SHS and electrification rate {corr_E_I}")

    return df

# test = test_correlation(IRENA_data, electrification_rate_africa, trade_data)
# print(test)
# test.to_excel(path_input+"datatest123.xlsx")


def percent_trade_PV(ten_code_data, six_code_data):
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    periods = list(dict.fromkeys(ten_code_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = Validation_functions.check_missing_countries(ten_code_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    trade_not_relevant = pd.DataFrame()

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
            # manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
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
                                                                             "Value")
            imports_period = imports_period.groupby(["Partner Country"]).sum()
            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data_ten, name, int(period), "export",
                                                                             "Value")
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
                                                                           "Value")
            exports_period_mirror = exports_period_mirror.groupby(["Reporting Country"]).sum()
            imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data_ten, name, int(period), "export",
                                                                           "Value")
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
            # Add a check for export to large exporter, and remove them.
            percentage_exp, sum_exports = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp,
                                                                                               exports_period)
            net_trade = sum_imports - sum_exports
            # 6-digits level
            imports_period_six = NJORD_function_test.imports_or_export_in_period(monthly_data_six, name, int(period),
                                                                                 "import", "Value")
            exports_period_six = NJORD_function_test.imports_or_export_in_period(monthly_data_six, name, int(period),
                                                                                 "export", "Value")
            # Handle missing data/mirror data, and combine the direct data with the mirror data.
            exports_period_mirror_six = NJORD_function_test.create_mirror_data(monthly_data_six, name, int(period),
                                                                               "import", "Value")
            imports_period_mirror_six = NJORD_function_test.create_mirror_data(monthly_data_six, name, int(period),
                                                                               "export", "Value")
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
ten = pd.read_csv("ITC_Monthly_data_HS_10.csv")
#check_amount = percent_trade_PV(ten, six)
#check_amount.to_excel("To_calculate_percentage_of_PV.xlsx")

def calculate_percentage_of_PV(trade_data):
    PV_share_in_ten_code = pd.DataFrame()
    n = 0
    while n < len(trade_data.index):
        x = 0
        while x < len(trade_data.columns):
            import_data = trade_data.iloc[n:n + 4:2, x:x + 12]
            export_data = trade_data.iloc[n+1:n + 5:2, x:x + 12]
            import_data_six = import_data.iloc[1].sum()
            import_data_ten = import_data.iloc[0].sum()
            export_data_six = export_data.iloc[1].sum()
            export_data_ten = export_data.iloc[0].sum()
            percent_import = import_data_ten/import_data_six
            percent_export = export_data_ten/export_data_six
            x += 12
            junkwords = ["10-code", "6-code"]
            print()
            country_imp = [word for word in import_data.index[0].split() if word not in junkwords]
            country_exp = [word for word in export_data.index[0].split() if word not in junkwords]
            country_imp = " ".join(country_imp)
            country_exp = " ".join(country_exp)
            PV_share_in_ten_code.at[country_imp, str(int(2009 + x/12))] = percent_import
            PV_share_in_ten_code.at[country_exp, str(int(2009 + x/12))] = percent_export
        n += 4
    return PV_share_in_ten_code


# trade_data = pd.read_excel("To_calculate_percentage_of_PV.xlsx", index_col=0)
# trade_data = calculate_percentage_of_PV(trade_data)
# trade_data.to_excel("share_in_PV_price.xlsx")

def test(ten_code_data):
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    periods = list(dict.fromkeys(ten_code_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = Validation_functions.check_missing_countries(ten_code_data, all_countries)
    for period in periods:
        monthly_data_ten = ten_code_data.loc[ten_code_data["period"] == period]
        month = str(period)[4:]
        year = str(period)[:4]
        if year == "2009":
            continue
        # Add months to quarters/years before you do the calculations.
        # manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
        # Picks out the relevant codes
        NTL_codes_rel = NTL_codes.loc[NTL_codes["countryCd"] == "United Kingdom"]
        print(NTL_codes_rel)
        NTL_codes_rel = NTL_codes_rel.loc[NTL_codes_rel["PV?"] == "Yes"]
        print(NTL_codes_rel)
        relevant_codes = NTL_codes_rel.index.values
        relevant_codes = relevant_codes.tolist()
        # print(relevant_codes)
        # Only keep the codes of the month that will be relevant here.
        monthly_data_ten = monthly_data_ten[monthly_data_ten["productCd"].isin(relevant_codes)]
        # Imports and exports a specific period for each specific country. Put in own function and save the results in a CSV-file?
        imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data_ten, "United Kingdom", int(period), "import",
                                                                             "Value")
        imports_period = imports_period.groupby(["Partner Country"]).sum()
        exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data_ten, "United Kingdom", int(period), "export",
                                                                             "Value")
        exports_period = exports_period.groupby(["Partner Country"]).sum()
        # Handle missing data/mirror data, and combine the direct data with the mirror data.
        monthly_data_ten = ten_code_data.loc[ten_code_data["period"] == period]
        monthly_data_ten = monthly_data_ten.loc[monthly_data_ten["Partner Country"] == "United Kingdom"]
        NTL_codes_rel = pd.DataFrame()
        for country in monthly_data_ten["Reporting Country"]:
            NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
            NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "No"]
            NTL_codes_rel = NTL_codes_rel.append(NTL_codes_country)
            # print(NTL_codes_rel)
        relevant_codes = NTL_codes_rel.index.values
        relevant_codes = relevant_codes.tolist()
        # Only keep the codes of the month that will be relevant here.
        monthly_data_ten = monthly_data_ten[monthly_data_ten["productCd"].isin(relevant_codes)]

        exports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data_ten, "United Kingdom", int(period), "import",
                                                                           "Value")
        exports_period_mirror = exports_period_mirror.groupby(["Reporting Country"]).sum()
        imports_period_mirror = NJORD_function_test.create_mirror_data(monthly_data_ten, "United Kingdom", int(period), "export",
                                                                           "Value")
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
        # Add a check for export to large exporter, and remove them.
        percentage_exp, sum_exports = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp,
                                                                                               exports_period)
        net_trade = sum_imports - sum_exports
    return


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
    north_of_sahara = ["Algeria", "Egypt, Arab Rep.", "Libya", "Morocco", "Tunisia"]
    west_africa = ["Benin", "Burkina Faso", "Cabo Verde", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Liberia",
                   "Mali", "Mauritania", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"]  # Côte d'Ivoire
    central_africa = ["Angola", "Cameroon", "Central African Republic", "Chad", "Congo, Dem. Rep.",
                      "Congo, Rep.", "Equatorial Guinea", "Gabon", "Sao Tome and Principe"]
    east_africa = ["Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Malawi",
                   "Mauritius", "Mozambique", "Rwanda", "Seychelles", "Somalia", "Uganda", "Tanzania", "Zambia",
                   "Zimbabwe", "Sudan", "South Sudan"]
    south_africa = ["South Africa", "Eswatini", "Lesotho", "Namibia", "Botswana"]
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
                              "Electrification_rate_Urban", "Access_to_clean_fuels", "Education_rate", "USOilprice",
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
    correlation_Njord_acc.to_excel(path_output + "Njord_acc_corr.xlsx")
    correlation_Njord_yearly.to_excel(path_output + "Njord_yearly_corr.xlsx")
    return


correlation_statistics_africa(pd.read_excel("Test_NJORD-Price_model_results_10codes_pvshareremoved.xlsx", index_col=0))

