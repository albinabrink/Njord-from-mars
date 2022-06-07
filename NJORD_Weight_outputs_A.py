import pandas as pd
import os
import NJORD_function_test
import Validation_functions


# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

########

os.makedirs(path_output, exist_ok=True)
# nations_list = os.listdir(path_input + "\\Export\\")
#period = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
#          "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
#          "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
#          "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
#          "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]


# Functions only used in weight calculations
def weight(raw_data):
    unit = "Weight"
    module_weight = pd.read_excel("Module_weight.xlsx", index_col=0)
    ref_data = pd.read_excel("Reference_annual_2022.xlsx", index_col=0, na_values=['NA'])
    pv_share_unit = pd.read_excel("Share_in_PV_" + unit + ".xlsx", index_col=0)  # Read the PV_share from excel
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Read manufacturing data
    manufacturing_df = manufacturing_df.fillna(0)
    previous_capacity_W = 0
    output_W_each_year = pd.DataFrame()
    periods = list(dict.fromkeys(raw_data["period"]))
    all_countries = pd.read_excel("Country_code_list.xlsx")
    country_not_in_data = Validation_functions.check_missing_countries(raw_data, all_countries)
    nation_list = set(all_countries[1]) - set(country_not_in_data)
    # print(nation_list)
    for name in nation_list:
        if name not in ref_data.index.values:
            continue
        print(name)
        i = 0
        for period in periods:
            monthly_data = raw_data.loc[raw_data["period"] == period]
            month = str(period)[4:]
            year = str(period)[:4]
            if year == "2021":
                continue

            manufacturing_value = NJORD_function_test.manufacturing(name, year, manufacturing_df)

            imports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period), "import", "Quantity")
            exports_period = NJORD_function_test.imports_or_export_in_period(monthly_data, name, int(period), "export", "Quantity")
            imports_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period), "export", "Quantity")
            exports_mirror = NJORD_function_test.create_mirror_data(monthly_data, name, int(period), "import", "Quantity")
            imports_period = NJORD_function_test.combine_reported_and_mirror(imports_period, imports_mirror)
            exports_period = NJORD_function_test.combine_reported_and_mirror(exports_period, exports_mirror)
            # Add month shift here
            # year, month = NJORD_function_test.add_time_shift(2, int(year), int(month))
            # if i < 3:
            #     if i == 0:
            #        exports_period_quarter = exports_period
            #        imports_period_quarter = imports_period
            #    else:
            #        exports_period_quarter = exports_period_quarter.add(exports_period, fill_value=0)
            #        imports_period_quarter = imports_period_quarter.add(imports_period, fill_value=0)
            #    i += 1
            #   if i <= 2:
            #        continue
            # i = 0
            # exports_period = exports_period_quarter
            # imports_period = imports_period_quarter
            if "World" in imports_period:
                imports_period = imports_period.drop(labels="World")
            if "World" in exports_period:
                exports_period = exports_period.drop(labels="World")

            # exports_period_quarter = pd.DataFrame()
            # imports_period_quarter = pd.DataFrame()
            # print(imports_period_quarter)
            exports_period = NJORD_function_test.remove_large_exporters(exports_period)

            nations_within_imp = imports_period.index.values
            nations_within_exp = exports_period.index.values

            percentage_imp, sum_imports = NJORD_function_test.calc_percentage_import_or_export(nations_within_imp, imports_period)
            percentage_exp, sum_exports = NJORD_function_test.calc_percentage_import_or_export(nations_within_exp, exports_period)
            PV_factor_imp, PV_share_unit = NJORD_function_test.calc_PV_factor(str(year), pv_share_unit, nations_within_imp, percentage_imp, "Import")
            PV_factor_exp, PV_share_unit = NJORD_function_test.calc_PV_factor(str(year), pv_share_unit, nations_within_exp, percentage_exp, "Export")

            if sum(percentage_imp) < 1:
                waste = 1-sum(percentage_imp)  # calc the wasted PV per year
                lack_PV = waste*PV_share_unit[year]["RoW"]  # The lacking PV that comes from the waste
                PV_factor_imp += lack_PV  # Update PV_factor_imp

            net_trade = ((sum_imports * PV_factor_imp) - (sum_exports * PV_factor_exp)) * 1000
            previous_capacity_W, installed_capacity = weight_capacity_output(module_weight, year, manufacturing_value, net_trade, previous_capacity_W)

            name = NJORD_function_test.name_cleanup(name, year)
            output_W_each_year = create_output_weight(ref_data, year, month, name, installed_capacity, output_W_each_year)
    output_W_each_year = NJORD_function_test.create_quarterly_data(output_W_each_year)
    # output_W_each_year = NJORD_function_test.acc_year(output_W_each_year)
    return output_W_each_year.sort_index()


def create_output_weight(reference, year, month, name, installed_capacity, output_W_each_year):
    # Creates the output for calculations of weight.
    PVPS = year + " - PVPS - annual"
    other = year + " - Other - annual"
    Irena = year + " - IRENA - annual"
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
    output_W_each_year.at[name, "Ref " + year] = ref_value
    output_W_each_year.at[name, "Source " + year] = source
    output_W_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    # output_W_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][name]
    output_W_each_year.at[name, "PVPS " + year] = reference[PVPS][name]
    output_W_each_year.at[name, "Other " + year] = reference[other][name]
    return output_W_each_year


def weight_capacity_output(module_weight, year, manufacturing_value, net_trade, previous_capacity_W):
    if module_weight[year]["Value"] == 0:
        installed_capacity = 0
    else:
        installed_capacity = (((net_trade/1000)/module_weight[year]["Value"])/10**6)+(manufacturing_value/4)
    previous_capacity_W = previous_capacity_W+installed_capacity
    return previous_capacity_W, installed_capacity


def create_weight_models_result_region():
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


data = pd.read_csv("ITC_Monthly_data_HS_6.csv")
weight_output_each_year = weight(data)
weight_output_each_year.to_excel(path_output+"Worldrem_NJORD_weight_models_result.xlsx")
