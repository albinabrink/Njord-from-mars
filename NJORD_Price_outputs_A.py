import numpy as np
import pandas as pd
import os
import NJORD_function_test
import API_download

#### This script calculates the installed capacity
unit = "Price"

### change path also in lines  453 -454####
path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Price\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

######

os.makedirs(path_output, exist_ok=True)
# nation_list = os.listdir(path_input + "\\Export\\")
period = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]


# Functions only used in Price calculations
def price(inputs, periods):  # Main function calculating the price model.
    unit = "Price"
    # nations_list = os.listdir(input + "\\Export\\")
    reference = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
    output_P_each_year = pd.DataFrame()
    output_P_MF_each_year = pd.DataFrame()
    Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
              "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
              "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
              "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands", "Norway", "Poland", "Portugal",
              "Romania", "Russian_Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
              "Ukraine", "United_Kingdom"]
    nations_list = API_download.get_countries()
    country_codes = []
    nation_list = []
    for x in nations_list:
        country_codes.append(x[0])
        nation_list.append(x[1])
    access_token = API_download.import_access_token()
    for year_quarter in periods:
        year = year_quarter.split("-")
        year = year[0]
        test = API_download.access_yearly_data(access_token, str(2018), '6')
        print(test)
        for name in nation_list:
            name = name.split(".")
            name = name[0]
            if name == "American Samoa" or name == "British Indian Ocean Territory" or name == "Eswatini" or name == "World":
                continue
            if int(year) > 2016 and "before" in name:
                # print("\n\nit is Sudan before so I stop\n\n", name)
                continue
            if int(year) <= 2016 and name == "Sudan":
                # print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
                continue
            manufacturing_value = NJORD_function_test.manufacturing(name, year)
            change1 = pd.read_excel("PVxchange.xlsx", index_col=0)
            # change_list = change.index.values
            import_source, imports_period, time_window_import, nations_within_imp = NJORD_function_test.direct_or_mirror(inputs, unit, "Import", year_quarter, name)
            export_source, exports_period, time_window_export, nations_within_exp = NJORD_function_test.direct_or_mirror(inputs, unit, "Export", year_quarter, name)
            percentage_imp, percentage_exp, sum_imports, sum_exports = NJORD_function_test.calc_percentage_import_export(imports_period,
                                                                                                     exports_period,
                                                                                                     time_window_import,
                                                                                                     time_window_export)
            PV_factor_imp, PV_share_unit = NJORD_function_test.calc_PV_factor(year, unit, nations_within_imp, percentage_imp, "Import")
            PV_factor_exp, PV_share_unit = NJORD_function_test.calc_PV_factor(year, unit, nations_within_exp, percentage_exp, "Export")

            if sum(percentage_imp) < 1:
                waste = 1-sum(percentage_imp)  # calc the wasted PV per year
                lack_PV = waste*PV_share_unit[year]["RoW"]  # The lacking PV that comes from the waste
                PV_factor_imp += lack_PV  # Update PV_factor_imp

            net_trade = (sum_imports*PV_factor_imp)-(sum_exports*PV_factor_exp)*1000
            PV_market_price = calc_PV_market_price(nations_within_imp, change1, percentage_imp, year_quarter, Europe)
            market_factor = prel_market_size(net_trade, change1, year_quarter)

            if PV_market_price == 0:
                installed_capacity = 0
                installed_capacity_MF = 0
            else:
                installed_capacity = ((net_trade/PV_market_price)/10**6)+manufacturing_value  # /4 on manufacturing value, check if should be removed?
                installed_capacity_MF = ((net_trade/(PV_market_price*market_factor))/10**6)+manufacturing_value

            name = NJORD_function_test.name_cleanup(name, year)

            output_P_each_year, output_P_MF_each_year = create_output_price(reference, year_quarter, year, name, installed_capacity, installed_capacity_MF, output_P_each_year, output_P_MF_each_year)

    return output_P_each_year, output_P_MF_each_year


def calc_PV_market_price(nations_within, change, percentage, year_quarter, Europe):
    cont = 0
    PV_market_price = 0
    change_list = change.index.values
    for item in nations_within:
        if item == "DataType":
            continue
        if item in change_list:
            single_value = change[year_quarter][item] * percentage[cont]  # value for each single nation
        else:
            if item in Europe:
                single_value = change[year_quarter]["EU"] * percentage[cont]  # value for each single nation
            else:
                single_value = change[year_quarter]["RoW"] * percentage[cont]

            # print(item, change[year_quarter]["RoW"], percentage[cont], year_quarter)

        PV_market_price = PV_market_price + single_value
        # print(PV_market_price,year,single_value,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        cont = cont + 1

    return PV_market_price


def prel_market_size(net_trade, change, year):
    # Preliminary Market size:
    prel_MS = (net_trade/change[year]["RoW"])/10**6
    all_market_factors = pd.read_excel("Market_size_factor.xlsx", index_col=0)

    # print(prel_MS,"prel")
    if prel_MS <= 1:
        market_factor = all_market_factors["0-1MW"]["Factor"]
    if 1 < prel_MS <= 5:
        market_factor = all_market_factors["1-5MW"]["Factor"]
    if 5 < prel_MS <= 10:
        market_factor = all_market_factors["5-10MW"]["Factor"]
    if 10 < prel_MS <= 100:
        market_factor = all_market_factors["10-100MW"]["Factor"]
    if prel_MS > 100:
        market_factor = all_market_factors[">100 MW"]["Factor"]
    return market_factor


def create_output_price(reference, year_quarter, year, name, installed_capacity, installed_capacity_MF, output_P_each_year, output_P_MF_each_year):
    PVPS = year + " - PVPS"
    other = year + " - Other"
    Irena = year + " - IRENA"
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

    if "Q4" in year_quarter:
        year_output = str(int(year) + 1) + "-Q1"
    if "Q1" in year_quarter:
        year_output = str(year) + "-Q2"
    if "Q2" in year_quarter:
        year_output = str(year) + "-Q3"
    if "Q3" in year_quarter:
        year_output = str(year) + "-Q4"

    output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
    output_P_each_year.at[name, "Ref " + year] = ref_value
    output_P_each_year.at[name, "Source " + year] = source
    output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
    output_P_MF_each_year.at[name, "Ref " + year] = ref_value
    output_P_MF_each_year.at[name, "Source " + year] = source
    output_P_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    output_P_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][
        name]
    output_P_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_P_each_year.at[name, "Other " + year] = reference[other][name]
    output_P_MF_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    output_P_MF_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][
        name]
    output_P_MF_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_P_MF_each_year.at[name, "Other " + year] = reference[other][name]
    return output_P_each_year, output_P_MF_each_year


def create_nations_within(dataset, name, export_import):
    nations_within = dataset.loc[name]
    partner_countries = []
    for row in range(len(nations_within)):
        if nations_within.iloc[row][export_import+"Value"] != np.nan:
            partner_countries.append(nations_within.iloc[row]["Partner Country"])
    nations_within = list(dict.fromkeys(partner_countries))
    return nations_within

    #test.to_csv("jagvetinte.csv")
    #print(test)
periods = ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
test = pd.read_csv("ITC_yearly_data_HS_6.csv")
test = test.set_index("Reporting Country")
# test.sort_values(by=["period", "Reporting Country"])
# test = test.drop(columns=["Unnamed: 0", "productCd"])
# test.to_csv("jagvetinte.csv")
# print(test)
create_nations_within(test, "Algeria", "import")
# output_P_each_year, output_P_MF_each_year = price(path_input, period)
# output_P_each_year.to_excel(path_output+"Test_Price_max_model_results.xlsx")
# output_P_MF_each_year.to_excel(path_output+"Test_NJORD-Price_model_results.xlsx")





