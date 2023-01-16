from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from scipy.stats.stats import kendalltau
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns

import os

# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Regressiontest\\"
# os.makedirs(path_input, exist_ok=True)


def europe_trade_US(ten_codes):  # Used to sort out the trade between the EU countries and USA.
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


def sort_out_Europe_trade(ten_code, six_code):
    Europe_countries = ["Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium",
                        "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark",
                        "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
                        "Italy", "Kosovo", "Latvia",
                        "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro",
                        "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia",
                        "San Marino", "Serbia", "Slovakia",
                        "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom",
                        "Vatican City"]
    years = ["2018", "2019", "2020", "2021"]
    NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
    # NTL_codes_Europe = NTL_codes[NTL_codes["countryCd"].isin(Europe_countries)]
    europe_trade_ten_code = ten_code.loc[ten_code["Reporting Country"].isin(Europe_countries)]
    europe_trade_six_code = six_code.loc[six_code["Reporting Country"].isin(Europe_countries)]
    for year in years:
        print(year)
        if year == "2018":
            europe_ten_code = europe_trade_ten_code[europe_trade_ten_code["period"].str.contains(year)]
            europe_six_code = europe_trade_six_code[europe_trade_six_code["period"].str.contains(year)]
        else:
            europe_ten_code = europe_ten_code.append(
                europe_trade_ten_code[europe_trade_ten_code["period"].str.contains(year)])
            europe_six_code = europe_six_code.append(
                europe_trade_six_code[europe_trade_six_code["period"].str.contains(year)])
    europe_six_code.to_excel("Europe_PV_trade_6_codes_2018-2021.xlsx")
    europe_ten_code.to_excel("Europe_PV_trade_10_codes_2018-2021.xlsx")
    NTL_codes_rel = pd.DataFrame()
    for country in europe_trade_ten_code["Reporting Country"].unique():
        print(country)
        NTL_codes_country = NTL_codes.loc[NTL_codes["countryCd"] == country]
        NTL_codes_country = NTL_codes_country.loc[NTL_codes_country["PV?"] == "Yes"]
        NTL_codes_rel = NTL_codes_rel.append(NTL_codes_country)
        # print(NTL_codes_rel)
    relevant_codes = NTL_codes_rel.index.values
    relevant_codes = relevant_codes.tolist()
    Europe_trade = europe_ten_code[europe_ten_code["productCd"].isin(relevant_codes)]
    print(Europe_trade)
    Europe_trade.to_excel("Europe_PV_trade_10_codes_relevant_2018-2021.xlsx")
    return

# ten_code = pd.read_csv("ITC_yearly_data_HS_10.csv", dtype={"productCd": str, "period": str})
# six_code = pd.read_csv("ITC_yearly_data_HS_6.csv", dtype={"productCd": str, "period": str})
# sort_out_Europe_trade(ten_code, six_code)

# From this point on, the code is used to check the african countries and the correlation with SDGs ###


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


def open_SDG_data():
    african_countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde", "Cameroon",
                         "Central African Republic", "Chad", "Comoros", "Democratic Republic of Congo", "Congo",
                         "Cote d'Ivoire",
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
        SDG_data = pd.read_csv(path_input + single_file)  # , index_col=0)
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
                         "Central African Republic", "Chad", "Comoros", "Democratic Republic of Congo", "Congo",
                         "Cote d'Ivoire",
                         "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini",
                         "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                         "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
                         "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
                         "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania",
                         "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]
    SDG_data = pd.read_excel("SDG_test.xlsx", index_col=[0, 1])
    print(SDG_data)
    # Read in IRENA data to use as reference for the African countries. This could and should probably be done in its own function, but too lazy for that now.
    IRENA_acc = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0).filter(like="IRENA")
    IRENA_acc.drop(list(IRENA_acc.filter(regex='s')), axis=1, inplace=True)
    IRENA_year = pd.read_excel("Reference_annual_2022.xlsx", index_col=0).filter(like="IRENA")
    IRENA_year.drop(list(IRENA_year.filter(regex='s')), axis=1, inplace=True)
    correlation_Njord_acc = pd.DataFrame()
    correlation_Njord_yearly = pd.DataFrame()
    Njord_accumulated = pd.DataFrame()
    Njord_yearly_installed = pd.DataFrame()
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
        while n < 2022:
            Njord_year_sum = Njord.loc[country, [col for col in Njord.columns if str(n) in col]]
            for col in Njord_year_sum.index.values:
                if str(n) != col[-6:-2]:
                    Njord_year_sum = Njord_year_sum.drop(col)
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
        SDG_data_country.insert(0, "Njord_acc", Njord_acc, True)
        SDG_data_country.insert(0, "Njord_yearly", Njord_yearly, True)
        Njord_acc = Njord_acc.rename(columns={"Njord_acc": country})
        Njord_accumulated[country] = Njord_acc[country]

        Njord_yearly = Njord_yearly.rename(columns={"Njord": country})
        Njord_yearly_installed[country] = Njord_yearly[country]
        SDG_data_country_corr = SDG_data_country.corr()
        SDG_data_country_corr_spear = SDG_data_country.corr(method="spearman")
        SDG_data_country_corr_spear["Njord_acc"].name = country
        SDG_data_country_corr_spearman = SDG_data_country_corr_spearman.append(SDG_data_country_corr_spear["Njord_acc"])
        SDG_data_country_corr_spearman.to_excel("Spearman_analysis_test.xlsx")
        # for column in SDG_data_country:
        #    print(column)
        #    print(SDG_data_country[column])
        #    not_nan = SDG_data_country[column].dropna()
        #    SDG_data_country_corr = pearsonr(SDG_data_country["Njord_yearly"], not_nan)
        #    SDG_data_country_corr_spear = SDG_data_country.corr(method="spearman")
        #    print(SDG_data_country_corr)
        #    print(SDG_data_country_corr_spear)
        SDG_data_country_corr["Njord_acc"].name = country
        SDG_data_country_corr["Njord_yearly"].name = country
        correlation_Njord_acc = correlation_Njord_acc.append(SDG_data_country_corr["Njord_acc"])
        correlation_Njord_yearly = correlation_Njord_yearly.append(SDG_data_country_corr["Njord_yearly"])
    correlation_Njord_acc = sort_into_area_Africa(correlation_Njord_acc)
    correlation_Njord_yearly = sort_into_area_Africa(correlation_Njord_yearly)
    correlation_Njord_acc.to_excel("Njord_acc_corr.xlsx")
    correlation_Njord_yearly.to_excel("Njord_yearly_corr.xlsx")
    Njord_accumulated_with_ref = Njord_accumulated.transpose()
    Njord_yearly_installed_with_ref = Njord_yearly_installed.transpose()
    for country in african_countries:
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
        for column in IRENA_acc.columns.values:
            if int(column[:4]) < 2010:
                continue
            Njord_accumulated_with_ref.at[country, column] = IRENA_acc.loc[country][column]
        for column in IRENA_year.columns.values:
            if int(column[:4]) < 2010:
                continue
            Njord_yearly_installed_with_ref.at[country, column] = IRENA_year.loc[country][column]
    Njord_accumulated_with_ref.to_excel("Africa_accumulated.xlsx")
    Njord_yearly_installed_with_ref.to_excel("Africa_yearly.xlsx")
    return


def test_correlation_per_year():
    SDG_data = pd.read_excel("SDG_test.xlsx", index_col=[0, 1])
    NJORD = pd.read_excel("NJORD-Combined_model_results_last_test.xlsx", index_col=0)
    Njord = NJORD.loc[:, [col for col in NJORD.columns if "NJORD" in col]]
    african_countries = ["Algeria",
                         "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde", "Cameroon",
                         "Central African Republic", "Chad", "Comoros", "Democratic Republic of Congo", "Congo",
                         "Cote d'Ivoire",
                         "Djibouti", "Egypt",
                         "Equatorial Guinea", "Eritrea", "Eswatini",
                         "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                         "Liberia", "Libya",
                         "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
                         "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
                         "Seychelles", "Sierra Leone", "Somalia", "South Africa",
                         "South Sudan", "Sudan", "Tanzania",
                         "Togo", "Tunisia",
                         "Uganda", "Zambia", "Zimbabwe"]
    correlation = pd.DataFrame()
    for column in SDG_data.columns.values:
        print(column)
        for year in range(2010, 2021):
            yearly_data = pd.DataFrame()
            Njord_yearly = pd.DataFrame()
            print(year)
            for country in african_countries:
                if country == "Eswatini" or country == "Guinea-Bissau":
                    continue
                if SDG_data.loc[country, year].loc[column] != SDG_data.loc[country, year].loc[
                    column]:  # To remove NaN values :)
                    continue
                yearly_data.at[country, column] = SDG_data.loc[country, year].loc[column]
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
                Njord_year_sum = Njord.loc[country, [col for col in Njord.columns if str(year) in col]]
                Njord_year_sum = Njord_year_sum.sum()
                Njord_yearly.at[country, year] = Njord_year_sum
            if yearly_data.empty:
                continue
            if len(yearly_data) < 3:
                continue
            # print(Njord_yearly)
            Njord_yearly = Njord_yearly.astype("float")
            # print(yearly_data)
            yearly_data = yearly_data.astype("float")
            corr = pearsonr(yearly_data[column], Njord_yearly[year])
            print(corr)
            correlation.at[year, column] = corr[0]  # f'{corr[0]} ({corr[1]})'
            correlation.at[year, column + " p-value"] = corr[1]
            # outpath = "path/of/your/folder/"

            # fig, ax = plt.subplots()  # generate figure with axes
            # ax.scatter(yearly_data, Njord_yearly)  # initialize plot
            # ax.xlabel(f'{column}')
            # ax.ylabel(f'Installed capacity {year}')
            # plt.draw()
            # plt.show()
            # fig.savefig(path.join(outpath, "dataname_0.png")
            # for i in range(1, len(data)):
            #    image.set_data(x, data[i])
            #   plt.draw()
            #   fig.savefig(path.join(outpath, "dataname_{0}.png".format(i))
            # plt.scatter(yearly_data, Njord_yearly, label=yearly_data.index.values)
            # ax.xlabel(f'{column}')
            # ax.ylabel(f'Installed capacity {year}')
        # for i, txt in enumerate(yearly_data.index.values):
        #    ax.annotate(txt, (yearly_data.iloc[i], Njord_yearly.iloc[i]))
        # plt.show(block=True)
    print(correlation)
    correlation.to_excel("correlation_Africa.xlsx")
    return


test_correlation_per_year()


# corr_stats_africa(pd.read_excel("NJORD-Combined_model_results_last_test.xlsx", index_col=0))


def correlation_statistics_africa(Njord):  # Not used currently
    path_output = "Regressiontest\\Correlation files\\"
    path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Regressiontest\\"
    os.makedirs(path_input, exist_ok=True)
    # os.makedirs(path_output, exist_ok=True)

    african_countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
                         "Central African Republic", "Chad", "Comoros", "Congo, Dem. Rep.", "Congo, Rep.",
                         "Djibouti", "Egypt, Arab Rep.", "Equatorial Guinea", "Eritrea", "Eswatini",
                         "Ethiopia", "Gabon", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                         "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
                         "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
                         "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania",
                         "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]  # "Côte d'Ivoire"

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
    electrification_rate_rural.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
                                          "2021"]
    electrification_rate_rural = electrification_rate_rural.replace("..", np.nan)
    electrification_rate_rural = electrification_rate_rural.astype(float)
    electrification_rate_urban = pd.read_csv(path_input + "Access to electricity Urban.csv", index_col=0)
    electrification_rate_urban.columns = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
                                          "2021"]
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
        oilprice = Oilprices[x:x + 12]
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
            Njord_acc.at["Njord_acc", str(2010 + n)] = Njord_year
            n += 1
        country_data = country_data.append(Njord_yearly)
        country_data = country_data.append(Njord_acc)
        country_data.index = ["GDP", "GDP_per_capita", "Electrification_rate", "Electrification_rate_Rural",
                              "Electrification_rate_Urban", "Access_to_clean_cooking_fuels", "Education_rate",
                              "USOilprice",
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
