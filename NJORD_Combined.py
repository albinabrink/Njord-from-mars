import os
import pandas as pd
import numpy as np
import NJORD_functions
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"

os.makedirs(path_output, exist_ok=True)

imp_sum_price = pd.read_csv("Imports_summed_Price.csv", index_col=0)
exp_sum_price = pd.read_csv("Exports_summed_Price.csv", index_col=0)
imp_sum_weight = pd.read_csv("Imports_summed_Weight.csv", index_col=0)
exp_sum_weight = pd.read_csv("Exports_summed_Weight.csv", index_col=0)

njord_price = pd.read_excel("NJORD-Price_model_results.xlsx", index_col=0)
njord_weight = pd.read_excel("NJORD-Weight_model_results.xlsx", index_col=0)


def combined(NJORD_Price, NJORD_Weight, imp_sum_price, imp_sum_weight, exp_sum_price, exp_sum_weight):
    # Calculate the net trade for Price and Weight and clean names of countries to make it comparable with the reference
    # countries.
    net_trade_price = (imp_sum_price-exp_sum_price)*1000
    price = NJORD_functions.name_clean_up(net_trade_price.index.values)
    net_trade_price.index = price
    net_trade_weight = (imp_sum_weight-exp_sum_weight)*1000
    weight = NJORD_functions.name_clean_up(net_trade_weight.index.values)
    net_trade_weight.index = weight
    # Read in required data, filter so only NJORD data is looped over and choose countries that uses weight and not
    # units for quantity
    combined_df = pd.DataFrame()
    PVPS_reference_data = NJORD_Price.filter(like="PVPS")
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    NJORD_Price = NJORD_Price.filter(like="NJORD")
    NJORD_Weight = NJORD_Weight.filter(like="NJORD")
    units_or_weight = pd.read_csv("units_or_weight_six.csv", index_col=0)
    # Loop over all years and select the weight model or the price model, price is used all years but 2015.
    for period in NJORD_Price.columns.values:
        year = str(period[-6:-2])
        print(year)
        if 2015 == int(period[-6:-2]):  # or int(period[-6:-2]) == 2020:
            # Use weight instrument
            for name in NJORD_Weight.index.values:
                manufacturing_value = NJORD_functions.manufacturing(name, str(year), manufacturing_df)
                # if units: use price.
                if name not in units_or_weight.index.values:
                    combined_df.at[name, period] = NJORD_Price.loc[name][period]
                    continue
                if name == "Burkina Faso":  # Added specially as it was missing in the weight data.
                    #print(NJORD_Price.loc[name][period])
                    combined_df.at[name, period] = NJORD_Price.loc[name][period]
                    continue
                if units_or_weight.loc[name][period[-6:]] == "Unit" or units_or_weight.loc[name][period[-6:]] == np.nan:
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
        # Change this and the first if statement above to choose which model to draw from.
        if 2010 <= int(period[-6:-2]) <= 2014 or 2016 <= int(period[-6:-2]) <= 2021:  # or int(period[-6:-2]) == 2020 or int(period[-6:-2]) == 2021:
            # Use Price instrument
            for name in NJORD_Price.index.values:
                manufacturing_value = NJORD_functions.manufacturing(name, str(year), manufacturing_df)
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
    combined_df = combined_df.clip(lower=0)  # Sets all values to at lowest 0.
    return combined_df


combined_data = combined(njord_price, njord_weight, imp_sum_price, imp_sum_weight, exp_sum_price, exp_sum_weight)
combined_data.to_excel("NJORD-Combined_model_results.xlsx")

