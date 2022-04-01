import numpy as np
#### This script calculate the installed capacity
import pandas as pd
import os
#### This script calculate the installed capacity
unit = "Price"
### Change path also in lines 119-120 330-331 #######

path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\Raw_data\\Final_database\\Price\\" # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\"# this will be the folder from where the GUI will read the data

### Change path also in lines 330-331 #######


os.makedirs(path_output, exist_ok=True)
nations_list = os.listdir(path_input + "\\Export\\")
Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
          "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
          "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
          "Macedonia  North", "Malta", "Moldova Republic of", "Netherlands", "Norway", "Poland", "Portugal", "Romania",
          "Russian Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
          "United Kingdom"]
desiderio = ["2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4", # Removed 2010-Q1 and 2009-Q4
             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3"] # and 2020-Q4
#period=["2020-Q4"]#,"2010-Q1","2010-Q2","2010-Q3","2010-Q4","2011-Q1","2011-Q2","2011-Q3","2011-Q4","2012-Q1","2012-Q2","2012-Q3","2012-Q4","2013-Q1","2013-Q2","2013-Q3","2013-Q4","2014-Q1","2014-Q2","2014-Q3","2014-Q4","2015-Q1","2015-Q2","2015-Q3","2015-Q4","2016-Q1","2016-Q2","2016-Q3","2016-Q4","2017-Q1","2017-Q2","2017-Q3","2017-Q4","2018-Q1","2018-Q2","2018-Q3","2018-Q4","2019-Q1","2019-Q2","2019-Q3","2019-Q4","2020-Q1","2020-Q2","2020-Q3","2020-Q4"]
outlier_Price = pd.read_excel("outlier_price_quarter.xlsx", index_col=0)
outlier_Weight = pd.read_excel("outlier_weight_quarter.xlsx", index_col=0)
#period=["2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"] #2008","2009","2010","2011","2012","2013","2014","2015","2016",
index = []
combined = pd.DataFrame()
combined_MF = pd.DataFrame()
reference_data_year = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
previous_capacity_P = 0
previous_capacity_P_MF = 0
previous_capacity_W = 0
for cat in nations_list: # cat means what? split on . and append it to to index. When do we use index?
    zzz = cat.split(".")
    index.append(zzz[0])

for name in nations_list: ### Split and renaming of countries with multiple possible names to one?" Should probably be done in a function
    name = name.split(".")
    name = name[0]
    if "before" in name:
        name = "Sudan"
    if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini": # Skip them
        continue
    name = name.replace("_", " ")
    if name == "Falkland Islands (Malvinas)":
        name = "Falkland Islands"
    if name == "Micronesia  Federated States of":
        name = "Micronesia"
    if name == "Lao People's Democratic Republic":
        name = "Laos"
    if name == "Bolivia  Plurinational State of":
        name = "Bolivia"
    if name == "Congo  Democratic Republic of the":
        name = "Democratic Republic of the Congo"
    if name == "Côte d'Ivoire":
        name = "Côte dIvoire"
    if name == "Falkland Islands (Malvinas)":
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
    PVPS = str(2009) + " - PVPS"
    other = str(2009) + " - Other"
    Irena = str(2009) + " - IRENA"

    if reference_data_year[PVPS][name] == 0: #Check if there is data from PVPS, if there is use it as ref value else other, then IRENA, then No Ref.
        ref_value = reference_data_year[other][name]
        source = "Other"
        if reference_data_year[other][name] == 0:
            ref_value = reference_data_year[Irena][name]
            source = "Irena"
            if reference_data_year[Irena][name] == 0:
                ref_value = 0
                source = "No Ref"
    else:
        ref_value = reference_data_year[PVPS][name]
        source = "PVPS"
    combined_MF.at[name, "Ref " + str(2009)] = ref_value
    combined_MF.at[name, "Source " + str(2009)] = source
    combined_MF.at[name, "IRENA " + str(2009)] = reference_data_year[Irena][name]
    combined_MF.at[name, "IRENA s " + str(2009)] = reference_data_year[str(2009) + " - IRENA s"][name]
    combined_MF.at[name, "PVPS " + str(2009)] = reference_data_year[PVPS][name]
    combined_MF.at[name, "Other " + str(2009)] = reference_data_year[other][name]

cont_col = 0

# Maybe split price and weight in two loops? This is a long loop that does a lot...
for year in desiderio:
    for name in nations_list:
        unit = "Price"
        # ???? #
        path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\Raw_data\\Final_database\\Price\\"  # this is the path_out_final in the script From_html_to_db
        path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\"  # this will be the folder from where the GUI will read the data
        name = name.split(".")
        name = name[0]
        #print(name, year)
        if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
            continue
        ###
        year_test = year.split("-")
        year_test = year_test[0]
        #print(name, year_test)
        ###correction needed for the format inside the table in the excel files ###
        if int(year_test) > 2016 and "before" in name:
            print("\n\nit is Sudan before so I stop\n\n", name)
            continue
        if int(year_test) <= 2016 and name == "Sudan":
            print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
            continue
        if unit == "Price":
            add2 = "value in "
            word1 = "Imported "
            word2 = "Exported "
        else:
            add2 = ""
            add1 = ""
            word1 = ""
            word2 = ""
        ### table with the parameters according to the "unit" selected THEN THE VARIABLE is the same for both calculation ####
        pv_share_unit = pd.read_excel("Share_in_PV_"+unit+".xlsx",index_col=0)  #valid for both
        ### Manufacturing for each country [MW] (same for both units) ####
        manufacturing = pd.read_excel("Manufacturing.xlsx",index_col=0,na_values=['NA'])
        manufacturing = manufacturing.fillna(0)
        if name in manufacturing.index.values:
            if year_test == "2009":
                manufacturing_value = manufacturing[year_test][name]
            else:
                manufacturing_value = manufacturing[year_test][name]/4
        else:
            manufacturing_value = 0
        ### only used if Price
        change = pd.read_excel("PVxchange.xlsx",index_col=0)
        change_list = change.index.values
        ### reading the import and export full raw data
        imports = pd.read_excel(path_input+"Import"+"\\"+name+".xlsx",index_col=0, na_values=['NA'])
        exports = pd.read_excel(path_input+"Export"+"\\"+name+".xlsx",index_col=0, na_values=['NA'])
        imports = imports.fillna(0)  # filling empty spaces with 0
        imports = imports.replace(to_replace="No Quantity", value=0)  # replacing no quantity with 0
        exports = exports.fillna(0)  # filling empty spaces with 0
        exports = exports.replace(to_replace="No Quantity", value=0)
        ### Selecting the time period (Q4 previous year and 1-2-3 of current year)
        time_window_import = [word1+add2+str(year)]
        time_window_export = [word2+add2+str(year)]
        # print(time_window_export)
        ### focusing the data_Set at only the selected period
        imports_period = imports[time_window_import]
        exports_period = exports[time_window_export]
        # print(imports_period)
        ### monitoring the source of the data: Mirror or direct?
        import_source = []
        d_count_import = 0
        m_count_import = 0
        for letter in imports_period.loc["DataType"]:
            import_source.append(letter)
            if letter == "D":
                d_count_import = d_count_import+1
            else:
                m_count_import = m_count_import+1

        export_source = []
        d_count_export = 0
        m_count_export = 0
        # calculating the sum of export and import
        if "World" in exports_period.index.values:
            sum_exports = exports_period.drop(["DataType", "World"]).to_numpy().sum()  # Sum of all export in the time period
        else:
            sum_exports = exports_period.drop("DataType").to_numpy().sum()  # Sum of all export in the time period

        if "World" in imports_period.index.values:
            sum_imports = imports_period.drop(["DataType", "World"]).to_numpy().sum()  # Sum of all import in the time period
        else:
            sum_imports = imports_period.drop("DataType").to_numpy().sum()  # Sum of all import in the time period

        pv_share_unit_list = pv_share_unit.index.values
        nations_within_imports = imports_period.index.values
        nations_within_exports = exports_period.index.values

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
                # print(item,"nazione")
                # print(time_window_import)
                # print(sum_imports,"somma")
                # print(imports_period.loc[item,time_window_import],"valori")
                value = (sum(imports_period.loc[item, time_window_import])/sum_imports)  # percentage for each country
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
                value = sum(exports_period.loc[item, time_window_export])/sum_exports  # percentage for each country
                percentage_exp.append(value)

        # PVa factor
        # pv_share_unit = pd.read_excel("Share_in_PV_"+unit+".xlsx", index_col=0)
        # pv_share_unit_list = pv_share_unit.index.values
        cont = 0
        PV_factor_imp = 0

        for item in nations_within_imports:
            if item == "DataType":
                continue
            if item in pv_share_unit_list:
                single_value = pv_share_unit[year_test][item]*percentage_imp[cont]  # value for each single nation
            else:
                single_value = pv_share_unit[year_test]["RoW"]*percentage_imp[cont]

            PV_factor_imp = PV_factor_imp+single_value
            cont = cont+1
        print(PV_factor_imp)
        cont = 0
        PV_factor_exp = 0

        for item in nations_within_exports:
            if item == "DataType":
                continue
            single_value = pv_share_unit[year_test]["RoW"]*percentage_exp[cont]
            PV_factor_exp = PV_factor_exp+single_value
            cont = cont+1
        # print(PV_factor_exp)

        if sum(percentage_imp) < 1:
            scarto = 1-sum(percentage_imp)
            print("Scarto: ", scarto)
            mancanza = scarto*pv_share_unit[year_test]["RoW"]
            print("Mancanza: ", mancanza)
            PV_factor_imp = PV_factor_imp+mancanza
        print(PV_factor_imp)
        #### installed capacity ###
        ### the PV_factor_imp is the same because it is selected at the beginning according to the unit needed! ###

        # Calculation of the Nemarket_factort Trade
        net_trade_price = ((sum_imports*PV_factor_imp)-(sum_exports*PV_factor_exp))*1000

        ### Preliminary Market size:
        prel_MS = (net_trade_price/change[year]["RoW"])/10**6
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

        #### PV market price (same as PV share)
        cont = 0
        PV_market_price = 0
        single_value = 0
        #####################################################
        #### HERE INSERT THE QUARTERS PRICE DIVISION ########
        #####################################################
        for item in nations_within_imports:
            if item == "DataType":
                continue
            if item in change_list:
                single_value = change[year][item]*percentage_imp[cont] #value for each single nation
                #print(item,change[year][item],percentage_imp[cont],year)
            else:
                if item in Europe:
                    single_value = change[year]["EU"] * percentage_imp[cont]  # value for each single nation
                    # print(item, change[year]["EU"], percentage_imp[cont], year,"ENTRATO IN EUROPA!!!!!!!!!!!!!!")
                else:
                    single_value = change[year]["RoW"]*percentage_imp[cont]
                    # print(item," entrato ma andato in ROW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                # print(item,change[year]["RoW"],percentage_imp[cont],year)

            PV_market_price = PV_market_price+single_value
            # print(PV_market_price,year,single_value,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            cont = cont+1
        ##########################################################################################################
        ##########################################################################################################

       # if unit=="Price":
            #print(net_trade_price,"net trade",PV_market_price,"price factor",market_factor,"market factor")

        #print(sum_imports,sum_exports,net_trade_price,"net trade")
        if unit == "Price":
            if PV_market_price == 0:
                installed_capacity_price = 0
                installed_capacity_MF_price = 0
            else:
                installed_capacity_price = ((net_trade_price/PV_market_price)/10**6)+manufacturing_value
                installed_capacity_MF_price = (net_trade_price/(PV_market_price*market_factor)/10**6) + manufacturing_value

        if int(year_test) <= 2016 and "before" in name:
           # print("\n\nit is Sudan before so I change name for the reference\n\n", name)
            name = "Sudan"
        if int(year_test) <= 2016 and "before" in name:
          #  print("\n\nit is Sudan before so I change name for the reference\n\n", name)
            name = "Sudan"

        unit = "Weight"
        path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
        path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\"  #
        #name = name.split(".")
        #name = name[0]
        # no reference for these
        #year_test = year.split("-")
        #year_test = year_test[0]
        #if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name == "Eswatini":
        #    continue
        # solving the problem of the two reports in sudan and sudan before 2012
        #if int(year_test) > 2016 and "before" in name:
            # print("\n\nit is Sudan before so I stop\n\n", name)
        #    continue
        #if int(year_test) <= 2016 and name == "Sudan":
            # print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
        #    continue
        #print(name, year, year_test)
        ###
        ###correction needed for the format inside the table in the excel files ###
        # if unit == "Price":
        #    add2 = "value in "
        #    word1 = "Imported "
        #    word2 = "Exported "
        # else:
        add2 = ""
        add1 = ""
        word1 = ""
        word2 = ""

        #### only in Weight
        module_weight = pd.read_excel("Module_weight.xlsx", index_col=0)

        # reading the import and export full raw data
        imports = pd.read_excel(path_input + "Import" + "\\" + name + ".xlsx", index_col=0, na_values=['NA'])
        exports = pd.read_excel(path_input + "Export" + "\\" + name + ".xlsx", index_col=0, na_values=['NA'])
        imports = imports.fillna(0)  # filling empty spaces with 0
        imports = imports.replace(to_replace="No Quantity", value=0)  # replacing no quantity with 0
        exports = exports.fillna(0)  # filling empty spaces with 0
        exports = exports.replace(to_replace="No Quantity", value=0)
        # Selecting the time period (Q4 previous year and 1-2-3 of current year)
        # time_window_import=[word1+add2+str(int(year)-1)+"-Q4",word1+add2+year+"-Q1",word1+add2+year+"-Q2",word1+add2+year+"-Q3"]
        # time_window_export=[word2+add2+str(int(year)-1)+"-Q4",word2+add2+year+"-Q1",word2+add2+year+"-Q2",word2+add2+year+"-Q3"]
        time_window_import = [word1 + add2 + str(year)]
        time_window_export = [word2 + add2 + str(year)]
        # focusing the data_Set at only the selected period
        imports_period = imports[time_window_import]
        exports_period = exports[time_window_export]
        # print(exports_period)
        ### monitoring the source of the data: Mirror or direct?
        import_source = []
        d_count_import = 0
        m_count_import = 0
        for letter in imports_period.loc["DataType"]:
            import_source.append(letter)
            if letter == "D":
                d_count_import = d_count_import + 1
            else:
                m_count_import = m_count_import + 1
        export_source = []
        d_count_export = 0
        m_count_export = 0
        for letter in exports_period.loc["DataType"]:
            export_source.append(letter)
            if letter == "D":
                d_count_export = d_count_export + 1
            else:
                m_count_export = m_count_export + 1
        t = True
        while t is True:
            if d_count_import == 4:
                source_data_import = "D"
                t = False
                continue
            if m_count_import == 4:
                source_data_import = "M"
                t = False
                continue
            if m_count_import < d_count_import:
                source_data_import = "D*"
                t = False
                continue
            if m_count_import > d_count_import:
                source_data_import = "M*"
                t = False
            if m_count_import == d_count_import:
                source_data_import = "M*"
                t = False
                continue
        # print(m_count_import,d_count_import,source_data_import,"risultato import")

        q = True
        while q is True:  # very stupid solution for the problem!!!!
            if d_count_export == 4:
                source_data_export = "D"
                q = False
                continue
            if m_count_export == 4:
                source_data_export = "M"
                q = False
                continue
            if m_count_export < d_count_export:
                source_data_export = "D*"
                q = False
                continue
            if m_count_export > d_count_export:
                source_data_export = "M*"
                q = False
            if m_count_export == d_count_export:
                source_data_export = "M*"
                q = False
                continue

        source_data_total = []
        if source_data_import == source_data_export:
            source_data_total = source_data_export
        if source_data_import != source_data_export:
            source_data_total = "I_" + source_data_import + "-E_" + source_data_export
        # calculating the sum of export and import
        if "World" in exports_period.index.values:
            sum_exports = exports_period.drop(
                ["DataType", "World"]).to_numpy().sum()  ## Sum of all export in the time period
        else:
            sum_exports = exports_period.drop(
                "DataType").to_numpy().sum()  ## Sum of all export in the time period

        if "World" in imports_period.index.values:
            sum_imports = imports_period.drop(
                ["DataType", "World"]).to_numpy().sum()  ## Sum of all import in the time period
        else:
            sum_imports = imports_period.drop(
                "DataType").to_numpy().sum()  ## Sum of all import in the time period

        pv_share_unit_list = pv_share_unit.index.values
        nations_within_imports = imports_period.index.values
        nations_within_exports = exports_period.index.values

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
                value = (sum(
                    imports_period.loc[item, time_window_import]) / sum_imports)  # percentage for each country
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
                value = sum(
                    exports_period.loc[item, time_window_export]) / sum_exports  # percentage for each country
                percentage_exp.append(value)

        # PVa factor
        pv_share_unit = pd.read_excel("Share_in_PV_" + unit + ".xlsx", index_col=0)
        pv_share_unit_list = pv_share_unit.index.values
        # print(pv_share_unit_list)
        cont = 0
        PV_factor_imp = 0
        for item in nations_within_imports:
            if item == "DataType":
                continue
            if item in pv_share_unit_list:
                single_value = pv_share_unit[year_test][item] * percentage_imp[
                    cont]  # value for each single nation
            else:
                single_value = pv_share_unit[year_test]["RoW"] * percentage_imp[cont]
            PV_factor_imp = PV_factor_imp + single_value
            cont = cont + 1

        cont = 0
        PV_factor_exp = 0
        for item in nations_within_exports:
            if item == "DataType":
                continue
            single_value = pv_share_unit[year_test]["RoW"] * percentage_exp[cont]
            PV_factor_exp = PV_factor_exp + single_value
            cont = cont + 1
        if sum(percentage_imp) < 1:
            scarto = 1 - sum(percentage_imp)
            mancanza = scarto * pv_share_unit[year_test]["RoW"]
            PV_factor_imp = PV_factor_imp + mancanza
        #### installed capacity ###
        ### the PV_factor_imp is the same because it is selected at the beginning according to the unit needed! ###

        # Calculation of the Nemarket_factort Trade
        net_trade_weight = ((sum_imports * PV_factor_imp) - (sum_exports * PV_factor_exp)) * 1000

        if unit == "Weight":
            if module_weight[year_test]["Value"] == 0:
                installed_capacity_weight = 0
            else:
                installed_capacity_weight = (((net_trade_weight / 1000) / module_weight[year_test]["Value"]) / 10 ** 6)\
                                            + manufacturing_value
            previous_capacity_W = previous_capacity_W + installed_capacity_weight
            # print(installed_capacity_weight,
            #      "Installed capacity [MW] of " + name + " for the year " + year + ", Weight ",
            #     source_data_total)
        name = name.replace("_", " ")
        if name == "Bolivia  Plurinational State of":
            name = "Bolivia"
        if name == "Congo  Democratic Republic of the":
            name = "Democratic Republic of the Congo"
        if name == "Côte d'Ivoire":
            name = "Côte dIvoire"
        if name == "Falkland Islands (Malvinas)":
            name = "Falkland Islands"
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
        # print("test")
        if int(year_test) > 2016 and "before" in name:
            # print("\n\n it is Sudan before so I stop\n\n", name)
            continue
        if int(year_test) <= 2016 and name == "Sudan":
            # print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
            continue
        reference_data_year[Irena][name]
        PVPS = year_test + " - PVPS"
        other = year_test + " - Other"
        Irena = year_test + " - IRENA"
        if reference_data_year[PVPS][name] == 0:
            ref_value = reference_data_year[other][name]
            source = "Other"
            if reference_data_year[other][name] == 0:
                ref_value = reference_data_year[Irena][name]
                source = "Irena"
                if reference_data_year[Irena][name] == 0:
                    ref_value = 0
                    source = "No Ref"
        else:
            ref_value = reference_data_year[PVPS][name]
            source = "PVPS"

        if "Q4" in year:
            year_output = str(int(year_test) + 1) + "-Q1"
            # print(year_output)
        if "Q1" in year:
            year_output = str(year_test) + "-Q2"
        if "Q2" in year:
            year_output = str(year_test) + "-Q3"
        if "Q3" in year:
            year_output = str(year_test) + "-Q4"


        ################################## Selection of the model #####################################################
      #  print(year,"year",year_test,"year test",year_output,"year output","!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
### outlier to be implemented and a way to select the model according to the year###

####################################################################################################
        combined_MF.at[name, "Ref " + year_test] = ref_value
        combined_MF.at[name, "Source " + year_test] = source
        combined_MF.at[name, "IRENA " + year_test] = reference_data_year[Irena][name]
        combined_MF.at[name, "IRENA s " + year_test] = reference_data_year[str(year_test) + " - IRENA s"][name]
        combined_MF.at[name, "PVPS " + year_test] = reference_data_year[PVPS][name]
        combined_MF.at[name, "Other " + year_test] = reference_data_year[other][name]

        # print(installed_capacity_weight,installed_capacity_price,installed_capacity_MF_price,"!!!!!!!!!!!!!!!!!!!!!!!!!!   !!!!!!!!!!!!!!!!")
        column = cont_col+1
        if year_test == "2014" or year_test == "2015" or year_test == "2016" or year_test == "2017" or year_test == \
                "2013" or year_test == "2012" or year_test == "2011" or year_test == "2010" or year_test == "2009" or \
                year_test == "2008":
            # print(name,manufacturing_value,"= manufactering",net_trade_weight,"= net weight",net_trade_price,"= net price",installed_capacity_weight,"= inst weight",installed_capacity_price,"= insta price")
            if name in outlier_Weight.index:
                #  print("is outlier")
                # print(outlier_Weight)
                if outlier_Weight.at[name, year_output] == "Yes":
                    #   print("outlier per il corrente anno")
                    if name in outlier_Price.index and outlier_Price.at[name, year_output] == "Yes":  # both outlier I keep the normal model
                        if manufacturing_value == 0:
                            # print("no manufac")
                            if net_trade_weight <= 0:
                                combined.at[name, "NJORD "+year_output] = installed_capacity_price
                                combined.at[name, column] = "Price"
                                combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                                combined_MF.at[name, column] = "Price"
                                #   print(name, "1")
                            if net_trade_weight >= 0 and installed_capacity_weight <= 0:
                                combined.at[name, "NJORD "+year_output] = installed_capacity_price
                                combined.at[name, column] = "Price"
                                combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                                combined_MF.at[name, column] = "Price"
                                #  print(name, "2")
                            if net_trade_weight >= 0 and installed_capacity_weight >= 0:
                                combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                                combined.at[name, column] = "Weight"
                                combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                                combined_MF.at[name, column] = "Weight"
                                # print(name, "3")
                        else:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined.at[name, column] = "Weight"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined_MF.at[name, column] = "Weight"
                    if name in outlier_Price.index and outlier_Price.at[name, year] != "Yes":  # price result is not outlier, thus it is selected
                        # print("in price the nation is outlier but not for this year")
                        combined.at[name,"NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price-out"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price-out"
                    else:
                        # print("  nation is not  outlier at all")
                        combined.at[name, "NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price-out"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price-out"

                else:
                    #   print("not for the current")
                    if manufacturing_value == 0:
                        if net_trade_weight <= 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_price
                            combined.at[name, column] = "Price"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                            combined_MF.at[name, column] = "Price"
                        #   print(name,"1")
                        if net_trade_weight >= 0 and installed_capacity_weight <= 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_price
                            combined.at[name, column] = "Price"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                            combined_MF.at[name, column] = "Price"
                        #   print(name,"2")
                        if net_trade_weight >= 0 and installed_capacity_weight >= 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined.at[name, column] = "Weight"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined_MF.at[name, column] = "Weight"
                        # print(name, "3")
                    else:
                        if installed_capacity_weight < 0 and installed_capacity_price > 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_price
                            combined.at[name, column] = "Price"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                            combined_MF.at[name, column] = "Price"
                        else:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined.at[name, column] = "Weight"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined_MF.at[name, column] = "Weight"
            else:
                #  print("not outlier")
                if manufacturing_value == 0:
                    if net_trade_weight <= 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price"
                    if net_trade_weight >= 0 and installed_capacity_weight <=0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price"
                    if net_trade_weight >= 0 and installed_capacity_weight >= 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight"
                else:
                    if installed_capacity_weight < 0 and installed_capacity_price > 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price"
                    else:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight"

        if year_test == "2018" or year_test == "2019" or year_test == "2020":
            # print(name,manufacturing_value,"= manufacturing",net_trade_weight,"= net weight",net_trade_price,"= net price",installed_capacity_weight,"= inst weight",installed_capacity_price,"= insta price")
            if name in outlier_Price.index:
                # print(name, " is outlier")
                if outlier_Price.at[name, year_output] == "Yes":
                    #  print(name, " for this year")
                    if name in outlier_Weight.index and outlier_Weight.at[name, year_output] == "Yes":
                        # print("bot outliers")
                        if manufacturing_value == 0:
                            if net_trade_price <= 0:
                                combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                                combined.at[name, column] = "Weight"
                                combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                                combined_MF.at[name, column] = "Weight"
                                #   print(name,"1")
                            if net_trade_price >= 0 and installed_capacity_price <= 0:
                                combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                                combined.at[name, column] = "Weight"
                                combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                                combined_MF.at[name, column] = "Weight"
                                #   print(name, "2")
                            if net_trade_price >= 0 and installed_capacity_price >= 0:
                                combined.at[name, "NJORD "+year_output] = installed_capacity_price
                                combined.at[name, column] = "Price"
                                combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                                combined_MF.at[name, column] = "Price"
                                #  print(name, "3")
                        else:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_price
                            combined.at[name, column] = "Price"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                            combined_MF.at[name, column] = "Price"
                    if name in outlier_Weight.index and outlier_Weight.at[name, year] != "Yes":
                        #  print("replacing because in weight is outlier bet not for this year")
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight_out"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight-out"
                    if name not in outlier_Weight.index:
                        # print("replacing because in weight not outlier at all")
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight_out"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight-out"

                else:
                    #  print("not for this year")
                    if manufacturing_value == 0:
                        if net_trade_price <= 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined.at[name, column] = "Weight"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined_MF.at[name, column] = "Weight"
                        #   print("Price")
                        if net_trade_price >= 0 and installed_capacity_price <= 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined.at[name, column] = "Weight"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined_MF.at[name, column] = "Weight"
                        if net_trade_price >= 0 and installed_capacity_price >= 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_price
                            combined.at[name, column] = "Price"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                            combined_MF.at[name, column] = "Price"
                    else:
                        if installed_capacity_price < 0 and installed_capacity_weight > 0:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined.at[name, column] = "Weight"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                            combined_MF.at[name, column] = "Weight"
                        else:
                            combined.at[name, "NJORD "+year_output] = installed_capacity_price
                            combined.at[name, column] = "Price"
                            combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                            combined_MF.at[name, column] = "Price"
            else:
                if manufacturing_value == 0:
                    if net_trade_price <= 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight"
                    #   print("Price")
                    if net_trade_price >= 0 and installed_capacity_price <= 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight"
                    if net_trade_price >= 0 and installed_capacity_price >= 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price"
                else:
                    if installed_capacity_price < 0 and installed_capacity_weight > 0:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined.at[name, column] = "Weight"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_weight
                        combined_MF.at[name, column] = "Weight"
                    else:
                        combined.at[name, "NJORD "+year_output] = installed_capacity_price
                        combined.at[name, column] = "Price"
                        combined_MF.at[name, "NJORD "+year_output] = installed_capacity_MF_price
                        combined_MF.at[name, column] = "Price"

        if combined.at[name, "NJORD "+year_output] <= 0:
            combined.at[name, "NJORD "+year_output] = 0
            combined.at[name, column] = "Negative"
        if combined_MF.at[name, "NJORD "+year_output] <= 0:
            combined_MF.at[name, "NJORD "+year_output] = 0
            combined_MF.at[name, column] = "Negative"

    cont_col = cont_col+1
combined_MF.to_excel("NJORD-Combined_model_results.xlsx")
print("Hello")

quartly = pd.read_excel("NJORD-Combined_model_results.xlsx", index_col=0,)
yearly = pd.DataFrame()
desiderio = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
print(quartly.columns)
for nation in quartly.index:
    for year in desiderio:
        q1 = quartly.loc[nation, "NJORD "+year+"-Q1"]
        q2 = quartly.loc[nation, "NJORD " + year + "-Q2"]
        q3 = quartly.loc[nation, "NJORD " + year + "-Q3"]
        q4 = quartly.loc[nation, "NJORD " + year + "-Q4"]
        if q1 < 0:
            q1 = 0
        if q2 < 0:
            q2 = 0
        if q3 < 0:
            q3 = 0
        if q4 < 0:
            q4 = 0
        somma = q1+q2+q3+q4
        yearly.at[nation, "NJORD "+year] = somma

for column in quartly.columns:
    if "NJORD" in str(column):
        continue
    else:
        to_add = quartly[column]
        yearly = yearly.join(to_add)

yearly.to_excel("NJORD-Combined_model_results_year.xlsx")

### Förvirrad över vad uppdelningen av alla värdsdelar faktiskt gör i koden? ####
Ref_country = ["Belgium", "Chile", "Denmark", "Finland", "France", "Israel", "Italy", "Spain", "Sweden", "Switzerland"]
Asia = ["Afghanistan", "Bangladesh", "Bhutan", "Brunei_Darussalam", "Cambodia", "China", "Hong_Kong__China", "India",
        "Indonesia", "Japan", "Kazakhstan", "Kyrgyzstan", "Lao_People's_Democratic_Republic", "Malaysia", "Maldives",
        "Myanmar", "Nepal", "Korea__Democratic_People's_Republic_of", "Korea__Republic_of", "Pakistan", "Philippines",
        "Singapore", "Korea__Democratic_People's_Republic_of", "Sri_Lanka", "Taipei__Chinese", "Tajikistan", "Thailand",
        "Turkmenistan", "Uzbekistan", "Viet_Nam", "Mongolia"]
Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
          "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
          "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
          "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands", "Norway", "Poland", "Portugal", "Romania",
          "Russian_Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
          "United_Kingdom"]
Africa = ["Algeria", "Angola", "Benin", "Botswana", "Burkina_Faso", "Burundi", "Cameroon", "Cabo_Verde",
          "Central_African_Republic", "Comoros", "Congo", "Congo__Democratic_Republic_of_the", "Djibouti", "Egypt",
          "Equatorial_Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea_Bissau",
          "Côte_d'Ivoire", "Kenya", "Lesotho", "Liberia", "Libya__State_of", "Mayotte", "Madagascar", "Malawi", "Mali",
          "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Saint_Helena",
          "Sao_Tome_and_Principe", "Senegal", "Seychelles", "Sierra_Leone", "Somalia", "South_Africa", "South_Sudan",
          "Sudan", "Tanzania__United_Republic_of", "Togo", "Tunisia", "Uganda", "Western_Sahara", "Zambia", "Zimbabwe"]
North_America = ["Bermuda", "Canada", "United_States_of_America", "Mexico"]
Central_America = ["Anguilla", "Barbados", "Belize", "Costa_Rica", "Cuba", "Curaçao", "Dominica", "Dominican_Republic",
                   "El_Salvador", "Grenada", "Guatemala", "Honduras", "Nicaragua", "Panama", "Saint_Lucia",
                   "Saint_Vincent_and_the_Grenadines", "Trinidad_and_Tobago", "Antigua_and_Barbuda", "Bahamas", "Haiti",
                   "Jamaica"]
South_America = ["Argentina", "Bolivia__Plurinational_State_of", "Brazil", "Colombia", "Chile", "Ecuador", "Guyana",
                 "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela__Bolivarian_Republic_of"]
Eurasia = ["Armenia", "Azerbaijan", "Turkey"]
Oceania = ["Australia", "Fiji", "Guam", "Micronesia__Federated_States_of", "Norfolk_Island", "New_Caledonia",
           "New_Zealand", "Papua_New_Guinea", "Solomon_Islands", "Kiribati", "New_Caledonia"]
Middle_East = ["Bahrain", "Iran__Islamic_Republic_of", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Palau",
               "Palestine__State_of", "Qatar", "Saudi_Arabia", "Syrian_Arab_Republic", "United_Arab_Emirates", "Yemen",
               "Kuwait", "Lebanon", "Jordan", "Oman"]
index = ["Ref_country", "Asia", "Europe", "Africa", "North_America", "Central_America", "South_America", "Eurasia",
         "Oceania", "Middle_East"]
reference_data_year = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
Combined = pd.read_excel("NJORD-Weight_model_results_year.xlsx", index_col=0, na_values=['NA'])

period_col = ["NJORD 2010", "Ref 2010", "Source 2010", "Diff 2010", "NJORD 2011", "Ref 2011", "Source 2011",
              "Diff 2011", "NJORD 2012", "Ref 2012", "Source 2012", "Diff 2012", "NJORD 2013", "Ref 2013",
              "Source 2013", "Diff 2013", "NJORD 2014", "Ref 2014", "Source 2014", "Diff 2014", "NJORD 2015",
              "Ref 2015", "Source 2015", "Diff 2015", "NJORD 2016", "Ref 2016", "Source 2016", "Diff 2016",
              "NJORD 2017", "Ref 2017", "Source 2017", "Diff 2017", "NJORD 2018", "Ref 2018", "Source 2018",
              "Diff 2018", "NJORD 2019", "Ref 2019", "Source 2019", "Diff 2019", "NJORD 2020", "Ref 2020",
              "Source 2020", "Diff 2020"]
# period=["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
output_column = ["Absolut Country Average [%]", "Total deviation for Data set [%]", "Median [%]", "Median [MW]",
                 "Standard deviation [MW]", "Average deviation [MW]", "T distribution [MW]"]
# Ref_country=Combined.index
Combined_region_results = pd.DataFrame()


for year in period_col:
    print(year)
    if "Ref" in year or "Source" in year or "Diff" in year:
        continue
    for region in index:
        ######################################## DATA SET ################## to change in index:
        difference_sum = 0
        NJORD_value_sum = 0
        ref_value_sum = 0
        ref_tot_irena = 0
        ref_tot_pvps = 0
        ref_tot_other = 0
        for country in eval(region):
            print(country)
            # country=country.replace(" ","_")
            if country == "British_Indian_Ocean_Territory" or country == "Eswatini":
                continue
            only_year = year.split(" ")
            only_year = only_year[1]
            PVPS = only_year + " - PVPS"
            other = only_year + " - Other"
            Irena = only_year + " - IRENA"
            country = country.replace("_", " ")
            if country == "Bolivia  Plurinational State of":
                country = "Bolivia"
            if country == "Congo  Democratic Republic of the":
                country = "Democratic Republic of the Congo"
            if country == "Côte d'Ivoire":
                country = "Côte dIvoire"
            if country == "Falkland Islands (Malvinas)":
                country = "Falkland Islands"
            if country == "Hong Kong  China":
                country = "Hong Kong"
            if country == "Iran  Islamic Republic of":
                country = "Iran"
            if country == "Korea  Democratic People's Republic of":
                country = "North Korea"
            if country == "Korea  Republic of":
                country = "South Korea"
            if country == "Lao People's Democratic Republic":
                country = "Laos"
            if country == "Libya  State of":
                country = "Libya"
            if country == "Macedonia  North":
                country = "Macedonia"
            if country == "Micronesia  Federated States of":
                country = "Micronesia"
            if country == "Moldova  Republic of":
                country = "Moldova"
            if country == "Palestine  State of":
                country = "Palestine"
            if country == "Russian Federation":
                country = "Russia"
            if country == "Syrian Arab Republic":
                country = "Syria"
            if country == "Taipei  Chinese":
                country = "Taiwan"
            if country == "Tanzania  United Republic of":
                country = "Tanzania"
            if country == "Venezuela  Bolivarian Republic of":
                country = "Venezuela"
            if country == "Viet Nam":
                country = "Vietnam"
            ######################################## DATA SET ################## to change
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
            print(ref_value, source, country, year, "Referenza")
            ref_value_sum = ref_value_sum + ref_value
            print(ref_value_sum, "totale", region, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            ref_tot_irena = ref_tot_irena+reference_data_year[Irena][country]
            ref_tot_pvps = ref_tot_pvps+reference_data_year[PVPS][country]
            ref_tot_other = ref_tot_other+reference_data_year[other][country]
        print(NJORD_value_sum, "SOMMA!!!!!!!", region)
        region = region.replace("_", " ")

        Combined_region_results.at[region, "NJORD " + only_year] = NJORD_value_sum
        Combined_region_results.at[region, "Ref " + only_year] = ref_value_sum
        Combined_region_results.at[region, "IRENA " + only_year] = ref_tot_irena
        Combined_region_results.at[region, "PVPS " + only_year] = ref_tot_pvps
        Combined_region_results.at[region, "Other " + only_year] = ref_tot_other


Combined_region_results.to_excel("NJORD-Combined_model_results_regions.xlsx")






