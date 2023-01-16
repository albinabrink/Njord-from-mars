import warnings
import pandas as pd
import os
import NJORD_functions

warnings.simplefilter(action='ignore', category=FutureWarning)

# This script calculates the installed capacity for the NJORD price model with monthly data and 10-codes and 6-codes

path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"

os.makedirs(path_output, exist_ok=True)
unit = "Price"
ten_code = pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str})  # Set dtype due to confused python.
six_code = pd.read_csv("ITC_Monthly_data_HS_6.csv", dtype={"productCd": str})
pv_xchange = pd.read_excel("PVxchange.xlsx", index_col=0)
NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)

# If all code has already been run once, should be able to comment out rows 21-31 as it is not needed for the last
# values. If any input data is changed, this would need to be rerun.

to_calculate_share_price = NJORD_functions.percent_trade_PV(ten_code, six_code, "Value")
pv_share = NJORD_functions.calculate_percentage_of_PV(to_calculate_share_price)
pv_share.to_excel("Share_in_PV_Price.xlsx")

pv_share = pd.read_excel("Share_in_PV_Price.xlsx", index_col=0)  # Comment out if the previous three lines are not
# commented out

imp_summed, exp_summed, PV_mark_summed = NJORD_functions.sort_out_data(ten_code, six_code, pv_xchange, pv_share, NTL_codes, unit)

imp_summed.to_csv("Imports_summed_Price.csv")
exp_summed.to_csv("Exports_summed_Price.csv")
PV_mark_summed.to_csv("PVxchange_summed_Price.csv")
# Functions only used in Price calculations in this file, should be rewritten into own files/libraries
imp_summed = pd.read_csv("Imports_summed_Price.csv", index_col=0)
exp_summed = pd.read_csv("Exports_summed_Price.csv", index_col=0)
PV_mark_summed = pd.read_csv("PVxchange_summed_Price.csv", index_col=0)

def NJORD_price_function(imp_summed, exp_summed, PV_mark_summed):  # Main function calculating the price model.
    reference = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])  # Read reference data
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    mf = pd.read_excel("Market_size_factor.xlsx", index_col=0)
    output_P = pd.DataFrame()
    output_P_MF = pd.DataFrame()

    net_trade_df = (imp_summed-exp_summed) * 1000
    net_trade_df.to_csv("Net_trade_price_last_test.csv")
    print(net_trade_df)
    for name in net_trade_df.index.values:
        print(name)
        for period in net_trade_df.columns.values:
            # monthly_data = raw_data.loc[raw_data["period"] == period]
            month = str(period)[4:]
            year = str(period[:4])
            # if year == "2022" or year == "2009":
            #     continue
            manufacturing_value = NJORD_functions.manufacturing(name, str(year), manufacturing_df)
            if PV_mark_summed.loc[name][period] == 0:
                installed_capacity = 0
                installed_capacity_MF = 0
            else:
                installed_capacity = ((net_trade_df.loc[name][period]/PV_mark_summed.loc[name][period])/10**6) + manufacturing_value/12  # on manufacturing value, check if it should be removed?
                market_factor, prel_ms = prel_market_size(net_trade_df.loc[name][period], period, mf)
                installed_capacity_MF = ((net_trade_df.loc[name][period]/(PV_mark_summed.loc[name][period]*(market_factor)))/(10**6)) + (manufacturing_value/12)
            name1 = NJORD_functions.name_cleanup(name, year)  # Name1 due to weird bug where the name stayed same
            if name1 in reference.index.values:
                output_P, output_P_MF = create_output_price(reference, str(year), month, name1,
                                                                                installed_capacity,
                                                                                installed_capacity_MF,
                                                                                output_P,
                                                                                output_P_MF)
    # output_P_each_year = NJORD_function_test.acc_year(output_P)
    # output_P_MF_each_year = NJORD_function_test.acc_year(output_P_MF)
    return output_P.sort_index(), output_P_MF.sort_index()


def prel_market_size(net_trade, month, all_market_factors):
    change = pd.read_excel("PVxchange.xlsx", index_col=0)  # Read the cost of panels from big producers
    year_quarter = NJORD_functions.add_quarter(month[:4], month[4:])
    # Preliminary Market size:
    prel_MS = (net_trade / change[year_quarter]["RoW"]) / 10 ** 6
    # print(prel_MS,"prel")
    if prel_MS <= 0:
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
    output_P_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    # output_P_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    # output_P_each_year.at[name, "Other " + ref_year] = reference[other][name]
    output_P_MF_each_year.at[name, "IRENA " + ref_year] = reference[Irena][name]
    # output_P_MF_each_year.at[name, "IRENA s " + ref_year] = reference[str(ref_year) + " - IRENA s"][name]
    output_P_MF_each_year.at[name, "PVPS " + ref_year] = reference[PVPS][name]
    # output_P_MF_each_year.at[name, "Other " + ref_year] = reference[other][name]
    return output_P_each_year, output_P_MF_each_year


output_P_each_year, output_P_MF_each_year = NJORD_price_function(imp_summed, exp_summed, PV_mark_summed)
# output_P_each_year.to_excel(path_output + "NJORD_Price_model_10Codes.xlsx")
output_P_MF_each_year.to_excel(path_output+"NJORD-Price_model_final_results.xlsx")
