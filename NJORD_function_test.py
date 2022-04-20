import os
import pandas as pd

# unit = "weight"
# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
# path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

# os.makedirs(path_output, exist_ok=True)
# nations_list = os.listdir(path_input + "\\Export\\")

# period = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
#             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
#             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
#             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
#             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]

# Generic functions for both weight and price calculations, name_cleanup,


def name_clean_up(nation_list):  # NOT USED!!!
    # Clean up the names of nations from the raw database and return a list of countries
    # print(nation_list)
    nation_list = [sub.replace("Bolivia__Plurinational_State_of", "Bolivia") for sub in nation_list]
    nation_list = [sub.replace("Congo__Democratic_Republic_of", "Democratic Republic of the Congo") for sub in nation_list]
    nation_list = [sub.replace("Côte_d'Ivoire", "Côte dIvoire") for sub in nation_list]
    nation_list = [sub.replace("Falkland_Islands_(Malvinas)", "Falkland Islands") for sub in nation_list]
    nation_list = [sub.replace("Hong_Kong__China", "Hong Kong") for sub in nation_list]
    nation_list = [sub.replace("Iran__Islamic_Republic_of", "Iran") for sub in nation_list]
    nation_list = [sub.replace("Korea__Democratic_People's_Republic_of", "North_Korea") for sub in nation_list]
    nation_list = [sub.replace("Korea__Republic_of", "South Korea") for sub in nation_list]
    nation_list = [sub.replace("Lao_People's_Democratic_Republic", "Laos") for sub in nation_list]
    nation_list = [sub.replace("Libya__State_of", "Libya") for sub in nation_list]
    nation_list = [sub.replace("Macedonia__North", "Macedonia") for sub in nation_list]
    nation_list = [sub.replace("Micronesia__Federated_States_of", "Micronesia") for sub in nation_list]
    nation_list = [sub.replace("Moldova__State_of", "Moldova") for sub in nation_list]
    nation_list = [sub.replace("Palestine__State_of", "Palestine") for sub in nation_list]
    nation_list = [sub.replace("Russian_Federation", "Russia") for sub in nation_list]
    nation_list = [sub.replace("Syrian_Arab_Republic", "Syria") for sub in nation_list]
    nation_list = [sub.replace("Taipei__Chinese", "Taiwan") for sub in nation_list]
    nation_list = [sub.replace("Tanzania__United_Republic_of", "Tanzania") for sub in nation_list]
    nation_list = [sub.replace("Venezuela__United_Republic_of", "Venezuela") for sub in nation_list]
    nation_list = [sub.replace("Viet_Nam", "Vietnam") for sub in nation_list]
    # Add a way to handle Sudan

    nation_list = [name.split(".") for name in nation_list]
    nation_list = [name[0] for name in nation_list]
    for name in nation_list:
        if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
            nation_list.remove(name)
    nation_list = [name.replace("_", " ") for name in nation_list]
    # print(nation_list)
    return nation_list


def name_cleanup(name, year):
    name = name.replace("_", " ")
    if name == "Bolivia  Plurinational State of":
        name = "Bolivia"
    if name == "Congo  Democratic Republic of the":
        name = "Democratic Republic of the Congo"
    if name == "Côte d'Ivoire":
        name = "Côte dIvoire"
    if name == "Falkland Islands Malvinas":
        name = "Falkland Islands"
    if name == "Hong Kong  China":
        name = "Hong Kong"
    if name == "Iran  Islamic Republic of":
        name = "Iran"
    if name == "Korea  Democratic People's Republic of":
        name = "North Korea"
    if name == "Korea  Republic of":
        name = "South Korea"
    if name == "Lao People's Democratic Republic":
        name = "Laos"
    if name == "Libya  State of":
        name = "Libya"
    if name == "Macedonia  North":
        name = "Macedonia"
    if name == "Micronesia  Federated States of":
        name = "Micronesia"
    if name == "Moldova  Republic of":
        name = "Moldova"
    if name == "Palestine  State of":
        name = "Palestine"
    if name == "Russian Federation":
        name = "Russia"
    if name == "Syrian Arab Republic":
        name = "Syria"
    if name == "Taipei  Chinese":
        name = "Taiwan"
    if name == "Tanzania  United Republic of":
        name = "Tanzania"
    if name == "Venezuela  Bolivarian Republic of":
        name = "Venezuela"
    if name == "Viet Nam":
        name = "Vietnam"
    if int(year) <= 2016 and "before" in name:
        # print("\n\nit is Sudan before so I change name for the reference\n\n", name)
        name = "Sudan"
    return name


def manufacturing(nation, year):  # Extract the manufacturing for a nation in a specific year
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])  # Use as input so not in loop
    manufacturing_df = manufacturing_df.fillna(0)
    # print(manufacturing_df)
    # year = year.split("-")
    # year = year[0]
    if nation in manufacturing_df.index.values:
        if year == "2009":
            manufacturing_value = manufacturing_df[year][nation]
        else:
            manufacturing_value = manufacturing_df[year][nation]/4
    else:
        manufacturing_value = 0
    return manufacturing_value
# print(manufacturing(test, period))


def calc_PV_factor(year, unit, nations_within, percentage, import_export):
    pv_share_unit = pd.read_excel("Share_in_PV_"+unit+".xlsx", index_col=0)  # Move out of loop?
    pv_share_unit_list = pv_share_unit.index.values
    cont = 0
    pv_factor = 0
    if import_export == "Import":
        for nation in nations_within:
            # print(nation)
            if nation == "DataType":
                continue
            if nation in pv_share_unit_list:
                single_value = pv_share_unit[year][nation]*percentage[cont]
            else:
                single_value = pv_share_unit[year]["RoW"]*percentage[cont]
            pv_factor += single_value
            cont = cont+1
    if import_export == "Export":  # Why is this different?
        for nation in nations_within:
            if nation == "DataType":
                continue
            single_value = pv_share_unit[year]["RoW"]*percentage[cont]
            pv_factor += single_value
    return pv_factor, pv_share_unit


def direct_or_mirror(data, unit, import_export, year, name):
    # print(data+import_export+"\\"+name+".xlsx")
    data = pd.read_excel(data+import_export+"\\"+name+".xlsx", index_col=0, na_values=['NA'])
    data = data.fillna(0)  # filling empty spaces with 0
    data = data.replace(to_replace="No Quantity", value=0)  # replacing no quantity with 0
    source = []
    d_count = 0
    m_count = 0
    if unit == "Price":
        add1 = "value in "
        word1 = "Imported "
        word2 = "Exported "
    else:
        add2 = ""
        add1 = ""
        word1 = ""
        word2 = ""
    time_window = [word1+add1+str(year)]
    if import_export == "Export":
        time_window = [word2+add1+str(year)]
    data_period = data[time_window]
    nations_within = data_period.index.values
    for letter in data_period.loc["DataType"]:
        source.append(letter)
        if letter == "D":
            d_count += 1
        else:
            m_count += 1
    t = True
    while t is True:
        if d_count == 4:
            source_data = "D"
            t = False
            continue
        if m_count == 4:
            source_data = "M"
            t = False
            continue
        if m_count < d_count:
            source_data = "D*"
            t = False
            continue
        if m_count > d_count:
            source_data = "M*"
            t = False
        if m_count == d_count:
            source_data = "M*"
            t = False
            continue
    return source_data, data_period, time_window, nations_within


def calc_percentage_import_export(imports, exports, time_window_import, time_window_export): # Should be built more generic, does the same thing twice.
    nations_within_imports = imports.index.values
    nations_within_exports = exports.index.values
    if "World" in nations_within_exports:
        sum_exports = exports.drop(
            ["DataType", "World"]).to_numpy().sum()  # Sum of all export in the time period
    else:
        sum_exports = exports.drop("DataType").to_numpy().sum()  # Sum of all export in the time period
    if "World" in nations_within_imports:
        sum_imports = imports.drop(
            ["DataType", "World"]).to_numpy().sum()  ## Sum of all import in the time period
    else:
        sum_imports = imports.drop("DataType").to_numpy().sum()  ## Sum of all import in the time period

    percentage_imp = []
    for item in nations_within_imports:
        if item == "DataType":
            continue
        if sum_imports == 0:
            percentage_imp.append(0)
            continue
        if item == "World":
            percentage_imp.append(0)
            continue
        else:
            # print(item, time_window_import, imports_period.loc[item, time_window_import])
            value = (sum(imports.loc[item, time_window_import])/sum_imports)  # percentage for each country
            percentage_imp.append(value)

    percentage_exp = []
    for item in nations_within_exports:
        if item == "DataType":
            continue
        if sum_exports == 0:
            percentage_exp.append(0)
            continue
        if item == "World":
            percentage_exp.append(0)
            continue
        else:
            # print(item,time_window_export,sum_exports,exports_period.loc[item,time_window_export])
            value = sum(exports.loc[item, time_window_export])/sum_exports  # percentage for each country
            percentage_exp.append(value)

    return percentage_imp, percentage_exp, sum_imports, sum_exports


# Functions only used in weight calculations
def weight(input, period):
    unit = "Weight"
    nations = os.listdir(input+"\\Export\\")
    module_weight = pd.read_excel("Module_weight.xlsx", index_col=0)
    ref_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
    previous_capacity_W = 0
    output_W_each_year = pd.DataFrame()
    for year_quarter in period:
        year = year_quarter.split("-")
        year = year[0]
        for name in nations:
            name = name.split(".")
            name = name[0]
            if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
                continue
            if int(year) > 2016 and "before" in name:
                # print("\n\nit is Sudan before so I stop\n\n", name)
                continue
            if int(year) <= 2016 and name == "Sudan":
                # print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
                continue
            manufacturing_value = manufacturing(name, year)

            import_source, imports_period, time_window_import, nations_within_imp = direct_or_mirror(input, unit, "Import", year_quarter, name)
            export_source, exports_period, time_window_export, nations_within_exp = direct_or_mirror(input, unit, "Export", year_quarter, name)

            if import_source == export_source: # Can I remove this? Don't see how it is used in the original code?
                source_data_total = export_source
            else:
                source_data_total = "I_"+import_source+"-E_"+export_source

            percentage_imp, percentage_exp, sum_imports, sum_exports = calc_percentage_import_export(imports_period, exports_period, time_window_import, time_window_export)
            PV_factor_imp, PV_share_unit = calc_PV_factor(year, unit, nations_within_imp, percentage_imp, "Import")
            PV_factor_exp, PV_share_unit = calc_PV_factor(year, unit, nations_within_exp, percentage_exp, "Export")

            if sum(percentage_imp) < 1:
                waste = 1-sum(percentage_imp)  # calc the wasted PV per year
                lack_PV = waste*PV_share_unit[year]["RoW"]  # The lacking PV that comes from the waste
                PV_factor_imp += lack_PV  # Update PV_factor_imp

            net_trade = ((sum_imports * PV_factor_imp) - (sum_exports * PV_factor_exp)) * 1000
            previous_capacity_W, installed_capacity = weight_capacity_output(module_weight, year, manufacturing_value, net_trade, previous_capacity_W)

            # if module_weight[year]["Value"] == 0:
            #     installed_capacity = 0
            # else:
            #    installed_capacity = (((net_trade/1000)/module_weight[year]["Value"])/10**6)+(manufacturing_value/4)  # Why divide with 10^6?
            name = name_cleanup(name, year)
            output_W_each_year = create_output_weight(ref_data, year_quarter, year, name, installed_capacity, output_W_each_year)

    return output_W_each_year


def create_output_weight(reference, year_quarter, year, name, installed_capacity, output_W_each_year):
    # Creates the output for calculations of weight.
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
    output_W_each_year.at[name, "NJORD " + year_output] = installed_capacity
    output_W_each_year.at[name, "Ref " + year] = ref_value
    output_W_each_year.at[name, "Source " + year] = source
    output_W_each_year.at[name, "IRENA " + year] = reference[Irena][name]
    output_W_each_year.at[name, "IRENA s " + year] = reference[str(year) + " - IRENA s"][name]
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
    output_col = ["Absolut Country Average [%]", "Total deviation for Data set [%]", "Median [%]", "Median [MW]",
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
                country = name_cleanup(country, year)
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


# Functions only used in Price calculations
def price(input, period):
    unit = "Price"
    nations_list = os.listdir(input + "\\Export\\")
    reference = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
    output_P_each_year = pd.DataFrame()
    output_P_MF_each_year = pd.DataFrame()
    Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
              "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
              "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
              "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands", "Norway", "Poland", "Portugal",
              "Romania",
              "Russian_Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
              "United_Kingdom"]

    for year_quarter in period:
        year = year_quarter.split("-")
        year = year[0]
        for name in nations_list:
            name = name.split(".")
            name = name[0]
            if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
                continue
            if int(year) > 2016 and "before" in name:
                # print("\n\nit is Sudan before so I stop\n\n", name)
                continue
            if int(year) <= 2016 and name == "Sudan":
                # print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
                continue
            manufacturing_value = manufacturing(name, year)
            change1 = pd.read_excel("PVxchange.xlsx", index_col=0)
            # change_list = change.index.values
            import_source, imports_period, time_window_import, nations_within_imp = direct_or_mirror(input, unit, "Import", year_quarter, name)
            export_source, exports_period, time_window_export, nations_within_exp = direct_or_mirror(input, unit, "Export", year_quarter, name)
            percentage_imp, percentage_exp, sum_imports, sum_exports = calc_percentage_import_export(imports_period,
                                                                                                     exports_period,
                                                                                                     time_window_import,
                                                                                                     time_window_export)
            PV_factor_imp, PV_share_unit = calc_PV_factor(year, unit, nations_within_imp, percentage_imp, "Import")
            PV_factor_exp, PV_share_unit = calc_PV_factor(year, unit, nations_within_exp, percentage_exp, "Export")

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
                installed_capacity = ((net_trade/PV_market_price)/10**6)+(manufacturing_value/4)
                installed_capacity_MF = ((net_trade/(PV_market_price*market_factor))/10**6)+manufacturing_value

            name = name_cleanup(name, year)

            output_P_each_year, output_P_MF_each_year = create_output_price(reference, year_quarter, year, name, installed_capacity, installed_capacity_MF, output_P_each_year, output_P_MF_each_year)

    return output_P_each_year, output_P_MF_each_year


def calc_PV_market_price(nations_within, change, percentage, year_quarter, Europe):
    cont = 0
    PV_market_price = 0
    # single_value = 0
    change_list = change.index.values
    for item in nations_within:
        if item == "DataType":
            continue
        if item in change_list:
            single_value = change[year_quarter][item] * percentage[cont]  # value for each single nation
            # print(item, change[year_quarter][item], percentage[cont], year_quarter)
        else:
            if item in Europe:
                single_value = change[year_quarter]["EU"] * percentage[cont]  # value for each single nation
                # print(item, change[year_quarter]["EU"], percentage[cont], year_quarter, "ENTRATO IN EUROPA!!!!!!!!!!!!!!")
            else:
                single_value = change[year_quarter]["RoW"] * percentage[cont]
                # print(item, " entrato ma andato in ROW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")

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

# Functions for combined model


def decide_ref(ref, name, year):
    if ref[PVPS][name] == 0: #Check if there is data from PVPS, if there is use it as ref value else other, then IRENA, then No Ref.
        ref_value = ref[other][name]
        source = "Other"
        if ref[other][name] == 0:
            ref_value = ref[Irena][name]
            source = "Irena"
            if ref[Irena][name] == 0:
                ref_value = 0
                source = "No Ref"
    else:
        ref_value = ref[PVPS][name]
        source = "PVPS"
    combined_MF.at[name, "Ref " + str(2009)] = ref_value
    combined_MF.at[name, "Source " + str(2009)] = source
    combined_MF.at[name, "IRENA " + str(2009)] = reference_data_year[Irena][name]
    combined_MF.at[name, "IRENA s " + str(2009)] = reference_data_year[str(2009) + " - IRENA s"][name]
    combined_MF.at[name, "PVPS " + str(2009)] = reference_data_year[PVPS][name]
    combined_MF.at[name, "Other " + str(2009)] = reference_data_year[other][name]







# test1 = weight(nations_list, path_output)
# test1.to_excel(path_output+"test123.xlsx")
# path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Price\\"  # this is the path_out_final in the script From_html_to_db
# path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data
# os.makedirs(path_output, exist_ok=True)
# nations_list = os.listdir(path_input + "\\Export\\")
# test1, test2 = price(path_input, period)
# test1.to_excel(path_output+"test2.xlsx")
# test_price1, test_price2 = price(nations_list, period)
# test2.to_excel(path_output+"vadihelafriden.xlsx")

