import pandas as pd
import os
import NJORD_function_test
import Validation_functions


# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok=True)

unit = "Weight"
ten_code = pd.read_csv("ITC_Monthly_data_HS_10.csv", dtype={"productCd": str})
six_code = pd.read_csv("ITC_Monthly_data_HS_6.csv", dtype={"productCd": str})
pv_xchange = pd.read_excel("PVxchange.xlsx", index_col=0)  # Not needed or used in Weight, but same sort data function
NTL_codes = pd.read_csv("NTL_codes - Marked.csv", index_col=0)
pv_share = pd.read_excel("Share_in_PV_Weight.xlsx", index_col=0)

#imp_summed, exp_summed, PV_mark_summed = NJORD_function_test.sort_out_data(ten_code, six_code, pv_xchange, pv_share, NTL_codes, unit)

#imp_summed.to_csv("Imports_summed_Weight.csv")
#exp_summed.to_csv("Exports_summed_Weight.csv")
# PV_mark_summed.to_csv("PVxchange_summed_Price.csv") # Doesn't exist in the weight model, therefore just let it be.
imp_summed = pd.read_csv("Imports_summed_Weight.csv", index_col=0)
exp_summed = pd.read_csv("Exports_summed_Weight.csv", index_col=0)

def weight(imp_sum, exp_sum):
    module_weight = pd.read_excel("Module_weight.xlsx", index_col=0)
    ref_data = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    output_W_each_year = pd.DataFrame()
    # Calc the net trade. *1000 to make it MW/kg
    net_trade_df = (imp_sum - exp_sum)
    net_trade_df.to_csv("Net_trade_Weight.csv")
    print(net_trade_df)
    for name in net_trade_df.index.values:
        print(name)
        for period in net_trade_df.columns.values:
            month = str(period)[4:]
            year = str(period[:4])
            manufacturing_value = NJORD_function_test.manufacturing(name, str(year), manufacturing_df)
            # Calculate the installed capacity.
            if module_weight[year]["Value"] == 0:
                installed_capacity = 0
            else:
                installed_capacity = (((net_trade_df.loc[name][period])/module_weight[year]["Value"])/10**6)+(manufacturing_value/12)
            # Clean up the names of the countries in the data, so they are shorter and lie closer to the everyday use
            name1 = NJORD_function_test.name_cleanup(name, year)
            # Only keep the data for relevant countries, the original data contains regions and misc areas.
            if name1 in ref_data.index.values:
                output_W_each_year = create_output_weight(ref_data, year, month, name1, installed_capacity, output_W_each_year)
    return output_W_each_year.sort_index()


def create_output_weight(reference, year, month, name, installed_capacity, output_W_each_year):
    # Creates the output for calculations of weight.
    PVPS = "".join([year, " - PVPS - annual"])
    other = "".join([year, " - Other - annual"])
    Irena = "".join([year, " - IRENA - annual"])
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
    year, month = NJORD_function_test.add_time_shift(3, int(year), int(month))
    year_output = str(year+month)
    output_W_each_year.at[name, "NJORD " + year_output] = installed_capacity
    # output_W_each_year.at[name, "Ref " + year] = ref_value
    # output_W_each_year.at[name, "Source " + year] = source
    output_W_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    # output_W_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][name]
    output_W_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_W_each_year.at[name, "Other " + year] = reference[other][name]
    return output_W_each_year


def weight_capacity_output(module_weight, year, manufacturing_value, net_trade):
    if module_weight[year]["Value"] == 0:
        installed_capacity = 0
    else:
        installed_capacity = (((net_trade/1000)/module_weight[year]["Value"])/10**6)+(manufacturing_value/12)
    return installed_capacity


def create_weight_models_result_region(): # Not currently in use, needs to be made more effective
    Combined = pd.read_excel("NJORD-Weight_model_results_year.xlsx", index_col=0, na_values=['NA'])  # Must change
    reference_data_year = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
    index = ["Ref_country", "Asia", "Europe", "Africa", "North_America", "Central_America", "South_America", "Eurasia",
             "Oceania", "Middle_East"]
    period_col = ["NJORD 2010", "Ref 2010", "Source 2010", "Diff 2010", "NJORD 2011", "Ref 2011", "Source 2011",
                  "Diff 2011", "NJORD 2012", "Ref 2012", "Source 2012", "Diff 2012", "NJORD 2013", "Ref 2013",
                  "Source 2013", "Diff 2013", "NJORD 2014", "Ref 2014", "Source 2014", "Diff 2014", "NJORD 2015",
                  "Ref 2015", "Source 2015", "Diff 2015", "NJORD 2016", "Ref 2016", "Source 2016", "Diff 2016",
                  "NJORD 2017", "Ref 2017", "Source 2017", "Diff 2017", "NJORD 2018", "Ref 2018", "Source 2018",
                  "Diff 2018", "NJORD 2019", "Ref 2019", "Source 2019", "Diff 2019", "NJORD 2020", "Ref 2020",
                  "Source 2020", "Diff 2020"]
    output_col = ["Absolute Country Average [%]", "Total deviation for Data set [%]", "Median [%]", "Median [MW]",
                     "Standard deviation [MW]", "Average deviation [MW]", "T distribution [MW]"]
    Combined_region_results = pd.DataFrame()

    for year in period_col:
        if "Ref" in year or "Source" in year or "Diff" in year:
            continue
        for region in index:
            difference_sum = 0
            NJORD_value_sum = 0
            ref_value_sum = 0
            ref_tot_irena = 0
            ref_tot_pvps = 0
            ref_tot_other = 0
            for country in eval(region):
                # print(country)
                # country=country.replace(" ","_")
                if country == "British_Indian_Ocean_Territory" or country == "Eswatini":
                    continue
                only_year = year.split(" ")
                only_year = only_year[1]
                PVPS = only_year + " - PVPS"
                other = only_year + " - Other"
                Irena = only_year + " - IRENA"
                country = country.replace("_", " ")
                country = NJORD_function_test.name_cleanup(country, year)
                NJORD_value = Combined[year][country]
                ref_value = 0
                if reference_data_year[PVPS][country] == 0:
                    ref_value = reference_data_year[other][country]
                    source = "Other"
                    # print("PVPS zero used",reference_data_year[other][country])
                    if reference_data_year[other][country] == 0:
                        ref_value = reference_data_year[Irena][country]
                        source = "Irena"
                        if reference_data_year[Irena][country] == 0:
                            ref_value = 0
                            source = "No ref data"
                    # print("PVPS e Other zero, while Irena=",reference_data_year[Irena][country])
                else:
                    ref_value = reference_data_year[PVPS][country]
                    source = "PVPS"
                    # print("PVPS not zero")
                if NJORD_value < 0:
                    NJORD_value = 0
                    NJORD_value_sum = NJORD_value_sum + NJORD_value
                else:
                    NJORD_value_sum = NJORD_value_sum + NJORD_value
                # print(ref_value,source,country,year,"Referenza")
                ref_value_sum = ref_value_sum + ref_value
                # print(ref_value_sum,"totale",region,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                ref_tot_irena = ref_tot_irena + reference_data_year[Irena][country]
                ref_tot_pvps = ref_tot_pvps + reference_data_year[PVPS][country]
                ref_tot_other = ref_tot_other + reference_data_year[other][country]
                # print(NJORD_value_sum,"SOMMA!!!!!!!",region)
        region = region.replace("_", " ")

        Combined_region_results.at[region, "NJORD " + only_year] = NJORD_value_sum
        Combined_region_results.at[region, "Ref " + only_year] = ref_value_sum
        Combined_region_results.at[region, "IRENA " + only_year] = ref_tot_irena
        Combined_region_results.at[region, "PVPS " + only_year] = ref_tot_pvps
        Combined_region_results.at[region, "Other " + only_year] = ref_tot_other
    return Combined_region_results


weight_output_each_year = weight(imp_summed, exp_summed)
weight_output_each_year.to_excel(path_output+"NJORD-Weight_model_results_2022.xlsx")
