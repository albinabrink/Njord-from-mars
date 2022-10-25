import os
import pandas as pd
import numpy as np
import NJORD_function_test
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"

os.makedirs(path_output, exist_ok=True)

imp_sum_price = pd.read_csv("Imports_summed_Price.csv", index_col=0)
exp_sum_price = pd.read_csv("Exports_summed_Price.csv", index_col=0)
imp_sum_weight = pd.read_csv("Imports_summed_Weight.csv", index_col=0)
exp_sum_weight = pd.read_csv("Exports_summed_Weight.csv", index_col=0)

njord_price = pd.read_excel("NJORD-Price_model_results_2022.xlsx", index_col=0)
njord_weight = pd.read_excel("NJORD-Weight_model_results_2022.xlsx", index_col=0)


def combined(NJORD_Price, NJORD_Weight, imp_sum_price, imp_sum_weight, exp_sum_price, exp_sum_weight):
    net_trade_price = (imp_sum_price-exp_sum_price)*1000
    test = NJORD_function_test.name_clean_up(net_trade_price.index.values)
    net_trade_price.index = test
    net_trade_weight = (imp_sum_weight-exp_sum_weight)*1000
    test = NJORD_function_test.name_clean_up(net_trade_weight.index.values)
    net_trade_weight.index = test
    combined_df = pd.DataFrame()
    PVPS_reference_data = NJORD_Price.filter(like="PVPS")
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    NJORD_Price = NJORD_Price.filter(like="NJORD")
    NJORD_Weight = NJORD_Weight.filter(like="NJORD")
    units_or_weight = pd.read_csv("units_or_weight_six.csv", index_col=0)
    for period in NJORD_Price.columns.values:
        year = str(period[-6:-2])
        print(year)
        if 2015 == int(period[-6:-2]) or int(period[-6:-2]) == 2020:
            # Use weight instrument
            for name in NJORD_Weight.index.values:
                manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
                # if units: use price.
                if name not in units_or_weight.index.values:
                    # print(name, " NOT IN UNITS OR WEIGHT")
                    combined_df.at[name, period] = NJORD_Price.loc[name][period]
                    continue
                if units_or_weight.loc[name][period[-6:]] == "Unit" or units_or_weight.loc[name][period[-6:]] == np.nan:
                    print(name)
                    combined_df.at[name, period] = NJORD_Price.loc[name][period]
                    continue
                # if non-producing, negative net trade: price
                if manufacturing_value == 0 and net_trade_weight.loc[name][period[-6:]] < 0:
                    combined_df.at[name, period] = NJORD_Price.loc[name][period]
                    continue
                # if negative results: price
                if NJORD_Weight.loc[name][period] < 0:
                    combined_df.at[name, period] = NJORD_Price.loc[name][period]
                    continue
                combined_df.at[name, period] = NJORD_Weight.loc[name][period]
        if int(period[-6:-2]) == 2014 or 2016 <= int(period[-6:-2]) <= 2019 or int(period[-6:-2]) == 2021:
            # Use Price instrument
            for name in NJORD_Price.index.values:
                manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
                # if non-producing, negative net trade: weight
                if manufacturing_value == 0 and net_trade_price.loc[name][period[-6:]] < 0:
                    combined_df.at[name, period] = NJORD_Weight.loc[name][period]
                    continue
                # if negative results: weight
                if NJORD_Price.loc[name][period] < 0:
                    combined_df.at[name, period] = NJORD_Weight.loc[name][period]
                    continue
                combined_df.at[name, period] = NJORD_Price.loc[name][period]
    for column in PVPS_reference_data.columns.values:
        for name in PVPS_reference_data.index.values:
            combined_df.at[name, column] = PVPS_reference_data.loc[name][column]
    print(combined_df)
    return combined_df


combined_data = combined(njord_price, njord_weight, imp_sum_price, imp_sum_weight, exp_sum_price, exp_sum_weight)
combined_data.to_excel("NJORD-Combined_model_results2_2022.xlsx")

