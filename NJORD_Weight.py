import os
import pandas as pd
import NJORD_functions
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"  # this will be the folder to where the program will write the data
os.makedirs(path_output, exist_ok=True)

unit = "Weight"
ten_code = pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str})
six_code = pd.read_csv("ITC_Monthly_data_HS_6.csv", dtype={"productCd": str})
pv_xchange = pd.read_excel("PVxchange.xlsx", index_col=0)  # Not needed or used in Weight, but same sort data function
NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)

# If all code has already been run once, should be able to comment out rows 21-31 as it is not needed for the last
# values. If any input data is changed, this would need to be rerun.

#to_calculate_share_price = NJORD_functions.percent_trade_PV(ten_code, six_code, "Quantity")
#pv_share = NJORD_functions.calculate_percentage_of_PV(to_calculate_share_price)
#pv_share.to_excel("Share_in_PV_Weight.xlsx")

pv_share = pd.read_excel("Share_in_PV_Weight.xlsx", index_col=0)  # Comment out if the previous three lines are not
# commented out

# imp_summed, exp_summed, PV_mark_summed = NJORD_functions.sort_out_data(ten_code, six_code, pv_xchange, pv_share, NTL_codes, unit)

#imp_summed.to_csv("Imports_summed_Weight.csv")
#exp_summed.to_csv("Exports_summed_Weight.csv")
imp_summed = pd.read_csv("Imports_summed_Weight.csv", index_col=0)
exp_summed = pd.read_csv("Exports_summed_Weight.csv", index_col=0)


def weight(imp_sum, exp_sum):
    module_weight = pd.read_excel("Module_weight.xlsx", index_col=0)
    ref_data = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    output_W = pd.DataFrame()
    # Calc the net trade by subtracting the export from the import.
    net_trade_df = (imp_sum - exp_sum)
    net_trade_df.to_csv("Net_trade_Weight.csv")
    for name in net_trade_df.index.values:
        print(name)
        for period in net_trade_df.columns.values:
            month = str(period)[4:]
            year = str(period[:4])
            manufacturing_value = NJORD_functions.manufacturing(name, str(year), manufacturing_df)
            # Calculate the installed capacity.
            if module_weight[year]["Value"] == 0:
                installed_capacity = 0
            else:
                installed_capacity = (((net_trade_df.loc[name][period])/module_weight[year]["Value"])/10**6)+(manufacturing_value/12)
            # Clean up the names of the countries in the data, so they are shorter and lie closer to the everyday use
            name1 = NJORD_functions.name_cleanup(name, year)
            # Only keep the data for relevant countries, the original data contains regions and misc areas.
            if name1 in ref_data.index.values:
                output_W = create_output_weight(ref_data, year, month, name1, installed_capacity, output_W)
    return output_W.sort_index()


def create_output_weight(reference, year, month, name, installed_capacity, output_W_each_year):
    # Creates the output for calculations of weight.
    PVPS = "".join([year, " - PVPS - annual"])
    other = "".join([year, " - Other - annual"])
    Irena = "".join([year, " - IRENA - annual"])
    year, month = NJORD_functions.add_time_shift(3, int(year), int(month))
    year_output = str(year+month)
    output_W_each_year.at[name, "NJORD " + year_output] = installed_capacity
    output_W_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    output_W_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_W_each_year.at[name, "Other " + year] = reference[other][name]
    return output_W_each_year


weight_output_each_year = weight(imp_summed, exp_summed)
weight_output_each_year.to_excel(path_output+"NJORD-Weight_model_results.xlsx")
