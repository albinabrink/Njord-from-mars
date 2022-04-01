import pandas as pd
import os
#### This script calculate the installed capacity
unit = "Price"

### change path also in lines  453 -454####
path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Price\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

######

os.makedirs(path_output, exist_ok=True)
lista_nazioni=os.listdir(path_input+"\\Export\\")
Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia_and_Herzegovina", "Bulgaria", "Croatia",
          "Cyprus", "Czech_Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
          "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
          "Macedonia__North", "Malta", "Moldova__Republic_of", "Netherlands", "Norway", "Poland", "Portugal", "Romania",
          "Russian_Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
          "United_Kingdom"]
desiderio=["2009-Q4","2010-Q1","2010-Q2","2010-Q3","2010-Q4","2011-Q1","2011-Q2","2011-Q3","2011-Q4","2012-Q1","2012-Q2","2012-Q3","2012-Q4","2013-Q1","2013-Q2","2013-Q3","2013-Q4","2014-Q1","2014-Q2","2014-Q3","2014-Q4","2015-Q1","2015-Q2","2015-Q3","2015-Q4","2016-Q1","2016-Q2","2016-Q3","2016-Q4","2017-Q1","2017-Q2","2017-Q3","2017-Q4","2018-Q1","2018-Q2","2018-Q3","2018-Q4","2019-Q1","2019-Q2","2019-Q3","2019-Q4","2020-Q1","2020-Q2","2020-Q3","2020-Q4"]


#period=["2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"] #2008","2009","2010","2011","2012","2013","2014","2015","2016",
indici=[]
reference_data_year = pd.read_excel("Reference_accumulated_2022.xlsx",index_col=0, na_values=['NA'])
previous_capacity_P = 0
previous_capacity_P_MF = 0
previous_capacity_W = 0
for cat in lista_nazioni:
    zzz = cat.split(".")
    indici.append(zzz[0])

output_P_each_year = pd.DataFrame()
output_P_MF_each_year = pd.DataFrame()
for year in desiderio:
    for name in lista_nazioni:
        name = name.split(".")
        name = name[0]
        print(name,year)
        if name == "American_Samoa" or name == "British_Indian_Ocean_Territory" or name =="Eswatini" :
            continue
        ###
        year_test=year.split("-")
        year_test=year_test[0]
        print(year_test)
        ###correction needed for the format inside the table in the excel files ###
        if int(year_test) > 2016 and "before" in name:
            print("\n\nit is Sudan before so I stop\n\n", name)
            continue
        if int(year_test) <=2016 and name=="Sudan":
            print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
            continue
        if unit=="Price":
            add2="value in "
            word1="Imported "
            word2="Exported "
        else:
            add2=""
            add1=""
            word1 = ""
            word2 = ""
        ### table with the parameters according to the "unit" selected THEN THE VARIABLE is the same for both calculaiton ####
        pv_share_unit=pd.read_excel("Share_in_PV_"+unit+".xlsx",index_col=0)  #valid for both
        ###Manufacturing for each country [MW] (same for both units) ####
        manufacturing=pd.read_excel("Manufacturing.xlsx",index_col=0,na_values=['NA'])
        manufacturing=manufacturing.fillna(0)
        if name in manufacturing.index.values:
            manufacturing_value=manufacturing[year_test][name]
        else:
            manufacturing_value=0

        ###only used if Price
        change=pd.read_excel("PVxchange.xlsx",index_col=0)
        change_list=change.index.values
        #reading the import and export full raw data
        imports=pd.read_excel(path_input+"Import"+"\\"+name+".xlsx",index_col=0, na_values=['NA'])
        exports=pd.read_excel(path_input+"Export"+"\\"+name+".xlsx",index_col=0, na_values=['NA'])
        imports=imports.fillna(0) #filling empty spaces with 0
        imports=imports.replace(to_replace="No Quantity",value=0) #replacing no quantity with 0
        exports=exports.fillna(0)#filling empty spaces with 0
        exports=exports.replace(to_replace="No Quantity",value=0)
        # Selecting the time period (Q4 previous year and 1-2-3 of current year)
        time_window_import=[word1+add2+str(year)]
        time_window_export=[word2+add2+str(year)]
        #focusing the data_Set at only the selected period
        imports_period = imports[time_window_import]
        exports_period = exports[time_window_export]
        ###monitoring the source of the data: Mirror or direct?
        import_source=[]
        d_count_import=0
        m_count_import=0
        for letter in imports_period.loc["DataType"]:
            import_source.append(letter)
            if letter == "D":
                d_count_import=d_count_import+1
            else:
                m_count_import=m_count_import+1

        export_source = []
        d_count_export=0
        m_count_export=0

        for letter in exports_period.loc["DataType"]:
            export_source.append(letter)
            if letter == "D":
                d_count_export=d_count_export+1
            else:
                m_count_export=m_count_export+1
        t = True
        while t is True:
            if d_count_import == 4:
                source_data_import="D"
                t = False
                continue
            if m_count_import == 4:
                source_data_import="M"
                t = False
                continue
            if m_count_import < d_count_import:
                source_data_import="D*"
                t = False
                continue
            if m_count_import > d_count_import:
                source_data_import="M*"
                t = False
            if m_count_import == d_count_import:
                source_data_import = "M*"
                t = False
                continue

        q=True
        while q is True:    # very stupid solution for the problem!!!!
            if d_count_export == 4:
                source_data_export="D"
                q=False
                continue
            if m_count_export == 4:
                source_data_export="M"
                q=False
                continue
            if m_count_export < d_count_export:
                source_data_export="D*"
                q=False
                continue
            if m_count_export > d_count_export:
                source_data_export="M*"
                q=False
            if m_count_export == d_count_export:
                source_data_export = "M*"
                q = False
                continue

        source_data_total = []
        if source_data_import == source_data_export:
            source_data_total=source_data_export
        if source_data_import != source_data_export:
            source_data_total="I_"+source_data_import+"-E_"+source_data_export

        #calculating the sum of export and import
        if "World" in exports_period.index.values:
            sum_exports = exports_period.drop(["DataType","World"]).to_numpy().sum() ## Sum of all export in the time period
        else:
            sum_exports = exports_period.drop("DataType").to_numpy().sum()       ## Sum of all export in the time period

        if "World" in imports_period.index.values:
            sum_imports = imports_period.drop(["DataType", "World"]).to_numpy().sum()       ## Sum of all import in the time period
        else:
            sum_imports = imports_period.drop("DataType").to_numpy().sum()       ## Sum of all import in the time period



        pv_share_unit_list=pv_share_unit.index.values
        nations_within_imports = imports_period.index.values
        nations_within_exports = exports_period.index.values

        percentage_imp=[]
        for item in nations_within_imports:
            if item =="DataType":
                continue
            if sum_imports == 0:
                percentage_imp.append(0)
                continue
            if item == "World":
                percentage_imp.append(0)
                continue
            else:
                #print(item,"nazione")
                #print(time_window_import)
                #print(sum_imports,"somma")
                #print(imports_period.loc[item,time_window_import],"valori")
                value=(sum(imports_period.loc[item,time_window_import])/sum_imports)   #percentage for each country
                percentage_imp.append(value)



        percentage_exp=[]
        for item in nations_within_exports:
            if item =="DataType":
                continue
            if sum_exports == 0:
                percentage_exp.append(0)
                continue
            if item == "World":
                percentage_exp.append(0)
                continue
            else:
                value=sum(exports_period.loc[item,time_window_export])/sum_exports    #percentage for each country
                percentage_exp.append(value)

        # PVa factor
        pv_share_unit=pd.read_excel("Share_in_PV_"+unit+".xlsx",index_col=0)
        pv_share_unit_list=pv_share_unit.index.values
        cont=0
        PV_factor_imp=0

        for item in nations_within_imports:
            if item =="DataType":
                continue
            if item in pv_share_unit_list:
                single_value= pv_share_unit[year_test][item]*percentage_imp[cont] #value for each single nation
            else:
                single_value= pv_share_unit[year_test]["RoW"]*percentage_imp[cont]

            PV_factor_imp=PV_factor_imp+single_value
            cont=cont+1

        cont=0
        PV_factor_exp=0
        for item in nations_within_exports:
            if item =="DataType":
                continue
            single_value= pv_share_unit[year_test]["RoW"]*percentage_exp[cont]
            PV_factor_exp=PV_factor_exp+single_value
            cont=cont+1
        if sum(percentage_imp) <1:
            scarto=1-sum(percentage_imp)
            mancanza=scarto*pv_share_unit[year_test]["RoW"]
            PV_factor_imp=PV_factor_imp+mancanza
        #### installed capacity ###
        ### the PV_factor_imp is the same because it is selected at the beginning according to the unit needed! ###

        #Clculaiton of the Nemarket_factort Trade
        net_trade=((sum_imports*PV_factor_imp)-(sum_exports*PV_factor_exp))*1000

        ###Preliminary Market size:
        prel_MS=(net_trade/change[year]["RoW"])/10**6
        all_market_factors=pd.read_excel("Market_size_factor.xlsx",index_col=0)

        #print(prel_MS,"prel")
        if prel_MS <= 1:
            market_factor=all_market_factors["0-1MW"]["Factor"]
        if 1 < prel_MS <=5:
            market_factor = all_market_factors["1-5MW"]["Factor"]
        if 5 < prel_MS <= 10:
            market_factor = all_market_factors["5-10MW"]["Factor"]
        if 10 < prel_MS <= 100:
            market_factor = all_market_factors["10-100MW"]["Factor"]
        if prel_MS > 100:
            market_factor=all_market_factors[">100 MW"]["Factor"]

        #### PV market price (same as PV share)
        cont=0
        PV_market_price=0
        single_value=0

        print(change_list,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        #####################################################
        #### HERE INSERT THE QUARTERS PRICE DIVISION ########
        #####################################################
        for item in nations_within_imports:
            if item =="DataType":
                continue
            if item in change_list:
                single_value= change[year][item]*percentage_imp[cont] #value for each single nation
                print(item,change[year][item],percentage_imp[cont],year)
            else:
                if item in Europe:
                    single_value = change[year]["EU"] * percentage_imp[cont]  # value for each single nation
                    print(item, change[year]["EU"], percentage_imp[cont], year,"ENTRATO IN EUROPA!!!!!!!!!!!!!!")
                else:
                    single_value= change[year]["RoW"]*percentage_imp[cont]
                    print(item," entrato ma andato in ROW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")

                print(item,change[year]["RoW"],percentage_imp[cont],year)

            PV_market_price=PV_market_price+single_value
            #print(PV_market_price,year,single_value,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            cont=cont+1
        ##########################################################################################################
        ##########################################################################################################


        if unit=="Price":
            print(net_trade,"net trade",PV_market_price,"price factor",market_factor,"market factor")


        if unit == "Price":
            if PV_market_price==0:
                installed_capacity=0
                installed_capacity_MF=0
            else:
                installed_capacity=((net_trade/PV_market_price)/10**6)+(manufacturing_value/4)
                installed_capacity_MF=((net_trade/(PV_market_price*market_factor)/10**6))+manufacturing_value
                name = name.replace("_", " ")
                print()
                if name == "Bolivia  Plurinational State of":
                    name = "Bolivia"
                if name == "Congo  Democratic Republic of the":
                    name = "Democratic Republic of the Congo"
                if name == "Côte d'Ivoire":
                    name = "Côte dIvoire"
                if name == "Falkland Islands (Malvinas)":
                    name = "Falkland Islands"
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
                if int(year_test) <= 2016 and "before" in name:
                    print("\n\nit is Sudan before so I change name for the reference\n\n", name)
                    name="Sudan"
                if int(year_test) <= 2016 and "before" in name:
                    print("\n\nit is Sudan before so I change name for the reference\n\n", name)
                    name="Sudan"

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

            if "Q4" in year:
                year_output=str(int(year_test)+1)+"-Q1"
            if "Q1" in year:
                year_output=str(year_test)+"-Q2"
            if "Q2" in year:
                year_output=str(year_test)+"-Q3"
            if "Q3" in year:
                year_output=str(year_test)+"-Q4"

            output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
            output_P_each_year.at[name, "Ref " + year_test] = ref_value
            output_P_each_year.at[name, "Source " + year_test] = source
            output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
            output_P_MF_each_year.at[name, "Ref " + year_test] = ref_value
            output_P_MF_each_year.at[name, "Source " + year_test] = source
            output_P_each_year.at[name, "IRENA " + year_test] = reference_data_year[Irena][name]
            output_P_each_year.at[name, "IRENA s " + year_test] = reference_data_year[str(year_test) + " - IRENA s"][name]
            output_P_each_year.at[name, "PVPS " + year_test] = reference_data_year[PVPS][name]
            output_P_each_year.at[name, "Other " + year_test] = reference_data_year[other][name]
            output_P_MF_each_year.at[name, "IRENA " + year_test] = reference_data_year[Irena][name]
            output_P_MF_each_year.at[name, "IRENA s " + year_test] = reference_data_year[str(year_test) + " - IRENA s"][name]
            output_P_MF_each_year.at[name, "PVPS " + year_test] = reference_data_year[PVPS][name]
            output_P_MF_each_year.at[name, "Other " + year_test] = reference_data_year[other][name]
            print(installed_capacity, "Installed capacity [MW] of "+name+" for the year "+year+" without Market Factor, Price ",source_data_total)
            print(installed_capacity_MF, "Installed capacity [MW] of "+name+" for the year "+year+" with Market Factor, Price ",source_data_total,export_source,import_source)


output_P_MF_each_year.to_excel(path_output+"Price_MF_max_model_results.xlsx")
output_P_each_year.to_excel(path_output+"Price_max_model_results.xlsx")
output_P_MF_each_year.to_excel(path_output+"NJORD-Price_model_results.xlsx")

output_MF_year=pd.DataFrame()

import pandas as pd
import os
#### This script calculate the installed capacity
unit = "Price"
path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\before_maximizing_bk\\Price\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data
os.makedirs(path_output, exist_ok = True)
lista_nazioni = os.listdir(path_input+"\\Export\\")

desiderio=["2009-Q4","2010-Q1","2010-Q2","2010-Q3","2010-Q4","2011-Q1","2011-Q2","2011-Q3","2011-Q4","2012-Q1","2012-Q2","2012-Q3","2012-Q4","2013-Q1","2013-Q2","2013-Q3","2013-Q4","2014-Q1","2014-Q2","2014-Q3","2014-Q4","2015-Q1","2015-Q2","2015-Q3","2015-Q4","2016-Q1","2016-Q2","2016-Q3","2016-Q4","2017-Q1","2017-Q2","2017-Q3","2017-Q4","2018-Q1","2018-Q2","2018-Q3","2018-Q4","2019-Q1","2019-Q2","2019-Q3","2019-Q4","2020-Q1","2020-Q2","2020-Q3","2020-Q4"]


#period=["2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"] #2008","2009","2010","2011","2012","2013","2014","2015","2016",
indici = []
reference_data_year = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0, na_values=['NA'])
previous_capacity_P = 0
previous_capacity_P_MF = 0
previous_capacity_W = 0
for cat in lista_nazioni:
    zzz=cat.split(".")
    indici.append(zzz[0])

output_P_each_year=pd.DataFrame()
output_P_MF_each_year=pd.DataFrame()
for year in desiderio:
    for name in lista_nazioni:
        name=name.split(".")
        name=name[0]
        print(name,year)
        if name=="American_Samoa" or name=="British_Indian_Ocean_Territory" or name =="Eswatini" :
            continue
        ###
        year_test=year.split("-")
        year_test=year_test[0]
        print(year_test)
        ###correction needed for the format inside the table in the excel files ###
        if int(year_test) > 2016 and "before" in name:
            print("\n\nit is Sudan before so I stop\n\n", name)
            continue
        if int(year_test) <=2016 and name=="Sudan":
            print("\n\n it is Sudan but before 2016 so I stop\n\n",name)
            continue
        if unit=="Price":
            add2="value in "
            word1="Imported "
            word2="Exported "
        else:
            add2=""
            add1=""
            word1 = ""
            word2 = ""
        ### table with the parameters according to the "unit" selected THEN THE VARIABLE is the same for both calculaiton ####
        pv_share_unit=pd.read_excel("Share_in_PV_"+unit+".xlsx",index_col=0)  #valid for both
        ###Manufacturing for each country [MW] (same for both units) ####
        manufacturing=pd.read_excel("Manufacturing.xlsx",index_col=0,na_values=['NA'])
        manufacturing=manufacturing.fillna(0)
        if name in manufacturing.index.values:
            manufacturing_value=manufacturing[year_test][name]
        else:
            manufacturing_value=0

        ###only used if Price
        change=pd.read_excel("PVxchange.xlsx",index_col=0)
        change_list=change.index.values
        #reading the import and export full raw data
        imports=pd.read_excel(path_input+"Import"+"\\"+name+".xlsx",index_col=0, na_values=['NA'])
        exports=pd.read_excel(path_input+"Export"+"\\"+name+".xlsx",index_col=0, na_values=['NA'])
        imports=imports.fillna(0) #filling empty spaces with 0
        imports=imports.replace(to_replace="No Quantity",value=0) #replacing no quantity with 0
        exports=exports.fillna(0)#filling empty spaces with 0
        exports=exports.replace(to_replace="No Quantity",value=0)
        # Selecting the time period (Q4 previous year and 1-2-3 of current year)
        time_window_import=[word1+add2+str(year)]
        time_window_export=[word2+add2+str(year)]
        #focusing the data_Set at only the selected period
        imports_period = imports[time_window_import]
        exports_period = exports[time_window_export]
        ###monitoring the source of the data: Mirror or direct?
        import_source=[]
        d_count_import=0
        m_count_import=0
        for letter in imports_period.loc["DataType"]:
            import_source.append(letter)
            if letter == "D":
                d_count_import=d_count_import+1
            else:
                m_count_import=m_count_import+1

        export_source = []
        d_count_export=0
        m_count_export=0

        for letter in exports_period.loc["DataType"]:
            export_source.append(letter)
            if letter == "D":
                d_count_export=d_count_export+1
            else:
                m_count_export=m_count_export+1
        t = True
        while t is True:
            if d_count_import == 4:
                source_data_import="D"
                t = False
                continue
            if m_count_import == 4:
                source_data_import="M"
                t = False
                continue
            if m_count_import < d_count_import:
                source_data_import="D*"
                t = False
                continue
            if m_count_import > d_count_import:
                source_data_import="M*"
                t = False
            if m_count_import == d_count_import:
                source_data_import = "M*"
                t = False
                continue

        q=True
        while q is True:    # very stupid solution for the problem!!!!
            if d_count_export == 4:
                source_data_export="D"
                q=False
                continue
            if m_count_export == 4:
                source_data_export="M"
                q=False
                continue
            if m_count_export < d_count_export:
                source_data_export="D*"
                q=False
                continue
            if m_count_export > d_count_export:
                source_data_export="M*"
                q=False
            if m_count_export == d_count_export:
                source_data_export = "M*"
                q = False
                continue

        source_data_total = []
        if source_data_import == source_data_export:
            source_data_total=source_data_export
        if source_data_import != source_data_export:
            source_data_total="I_"+source_data_import+"-E_"+source_data_export

        #calculating the sum of export and import
        if "World" in exports_period.index.values:
            sum_exports = exports_period.drop(["DataType","World"]).to_numpy().sum() ## Sum of all export in the time period
        else:
            sum_exports = exports_period.drop("DataType").to_numpy().sum()       ## Sum of all export in the time period

        if "World" in imports_period.index.values:
            sum_imports = imports_period.drop(["DataType", "World"]).to_numpy().sum()       ## Sum of all import in the time period
        else:
            sum_imports = imports_period.drop("DataType").to_numpy().sum()       ## Sum of all import in the time period



        pv_share_unit_list=pv_share_unit.index.values
        nations_within_imports = imports_period.index.values
        nations_within_exports = exports_period.index.values

        percentage_imp=[]
        for item in nations_within_imports:
            if item =="DataType":
                continue
            if sum_imports == 0:
                percentage_imp.append(0)
                continue
            if item == "World":
                percentage_imp.append(0)
                continue
            else:
                #print(item,"nazione")
                #print(time_window_import)
                #print(sum_imports,"somma")
                #print(imports_period.loc[item,time_window_import],"valori")
                value=(sum(imports_period.loc[item,time_window_import])/sum_imports)   #percentage for each country
                percentage_imp.append(value)



        percentage_exp=[]
        for item in nations_within_exports:
            if item =="DataType":
                continue
            if sum_exports == 0:
                percentage_exp.append(0)
                continue
            if item == "World":
                percentage_exp.append(0)
                continue
            else:
                value=sum(exports_period.loc[item,time_window_export])/sum_exports    #percentage for each country
                percentage_exp.append(value)

        # PVa factor
        pv_share_unit=pd.read_excel("Share_in_PV_"+unit+".xlsx",index_col=0)
        pv_share_unit_list=pv_share_unit.index.values
        cont=0
        PV_factor_imp=0

        for item in nations_within_imports:
            if item =="DataType":
                continue
            if item in pv_share_unit_list:
                single_value= pv_share_unit[year_test][item]*percentage_imp[cont] #value for each single nation
            else:
                single_value= pv_share_unit[year_test]["RoW"]*percentage_imp[cont]

            PV_factor_imp=PV_factor_imp+single_value
            cont=cont+1

        cont=0
        PV_factor_exp=0
        for item in nations_within_exports:
            if item =="DataType":
                continue
            single_value= pv_share_unit[year_test]["RoW"]*percentage_exp[cont]
            PV_factor_exp=PV_factor_exp+single_value
            cont=cont+1
        if sum(percentage_imp) <1:
            scarto=1-sum(percentage_imp)
            mancanza=scarto*pv_share_unit[year_test]["RoW"]
            PV_factor_imp=PV_factor_imp+mancanza
        #### installed capacity ###
        ### the PV_factor_imp is the same because it is selected at the beginning according to the unit needed! ###

        #Clculaiton of the Nemarket_factort Trade
        net_trade=((sum_imports*PV_factor_imp)-(sum_exports*PV_factor_exp))*1000

        ###Preliminary Market size:
        prel_MS=(net_trade/change[year]["RoW"])/10**6
        all_market_factors=pd.read_excel("Market_size_factor.xlsx",index_col=0)

        #print(prel_MS,"prel")
        if prel_MS <= 1:
            market_factor=all_market_factors["0-1MW"]["Factor"]
        if 1 < prel_MS <=5:
            market_factor = all_market_factors["1-5MW"]["Factor"]
        if 5 < prel_MS <= 10:
            market_factor = all_market_factors["5-10MW"]["Factor"]
        if 10 < prel_MS <= 100:
            market_factor = all_market_factors["10-100MW"]["Factor"]
        if prel_MS > 100:
            market_factor=all_market_factors[">100 MW"]["Factor"]

        #### PV market price (same as PV share)
        cont=0
        PV_market_price=0
        single_value=0


        #####################################################
        #### HERE INSERT THE QUARTERS PRICE DIVISION ########
        #####################################################
        for item in nations_within_imports:
            if item =="DataType":
                continue
            if item in change_list:
                single_value= change[year][item]*percentage_imp[cont] #value for each single nation
                print(item,change[year][item],percentage_imp[cont],year)
            else:
                if item in Europe:
                    single_value = change[year]["EU"] * percentage_imp[cont]  # value for each single nation
                    print(item, change[year]["EU"], percentage_imp[cont], year,"ENTRATO IN EUROPA!!!!!!!!!!!!!!")
                else:
                    single_value= change[year]["RoW"]*percentage_imp[cont]
                    print(item," entrato ma andato in ROW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")

                print(item,change[year]["RoW"],percentage_imp[cont],year)

            PV_market_price=PV_market_price+single_value
            #print(PV_market_price,year,single_value,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            cont=cont+1
        ##########################################################################################################
        ##########################################################################################################


        if unit=="Price":
            print(net_trade,"net trade",PV_market_price,"price factor",market_factor,"market factor")


        if unit == "Price":
            if PV_market_price==0:
                installed_capacity=0
                installed_capacity_MF=0
            else:
                installed_capacity=((net_trade/PV_market_price)/10**6)+(manufacturing_value/4)
                installed_capacity_MF=((net_trade/(PV_market_price*market_factor)/10**6))+manufacturing_value
                name = name.replace("_", " ")
                print()
                if name == "Bolivia  Plurinational State of":
                    name = "Bolivia"
                if name == "Congo  Democratic Republic of the":
                    name = "Democratic Republic of the Congo"
                if name == "Côte d'Ivoire":
                    name = "Côte dIvoire"
                if name == "Falkland Islands (Malvinas)":
                    name = "Falkland Islands"
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
                if int(year_test) <= 2016 and "before" in name:
                    print("\n\nit is Sudan before so I change name for the reference\n\n", name)
                    name="Sudan"
                if int(year_test) <= 2016 and "before" in name:
                    print("\n\nit is Sudan before so I change name for the reference\n\n", name)
                    name="Sudan"

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

            if "Q4" in year:
                year_output=str(int(year_test)+1)+"-Q1"
            if "Q1" in year:
                year_output=str(year_test)+"-Q2"
            if "Q2" in year:
                year_output=str(year_test)+"-Q3"
            if "Q3" in year:
                year_output=str(year_test)+"-Q4"

            output_P_each_year.at[name, "NJORD " + year_output] = installed_capacity
            output_P_each_year.at[name, "Ref " + year_test] = ref_value
            output_P_each_year.at[name, "Source " + year_test] = source
            output_P_MF_each_year.at[name, "NJORD " + year_output] = installed_capacity_MF
            output_P_MF_each_year.at[name, "Ref " + year_test] = ref_value
            output_P_MF_each_year.at[name, "Source " + year_test] = source
            output_P_each_year.at[name, "IRENA " + year_test] = reference_data_year[Irena][name]
            output_P_each_year.at[name, "IRENA s " + year_test] = reference_data_year[str(year_test) + " - IRENA s"][name]
            output_P_each_year.at[name, "PVPS " + year_test] = reference_data_year[PVPS][name]
            output_P_each_year.at[name, "Other " + year_test] = reference_data_year[other][name]
            output_P_MF_each_year.at[name, "IRENA " + year_test] = reference_data_year[Irena][name]
            output_P_MF_each_year.at[name, "IRENA s " + year_test] = reference_data_year[str(year_test) + " - IRENA s"][name]
            output_P_MF_each_year.at[name, "PVPS " + year_test] = reference_data_year[PVPS][name]
            output_P_MF_each_year.at[name, "Other " + year_test] = reference_data_year[other][name]
            print(installed_capacity,"Installed capacity [MW] of "+name+" for the year "+year+" without Market Factor, Price ",source_data_total)
            print(installed_capacity_MF,"Installed capacity [MW] of "+name+" for the year "+year+" with Market Factor, Price ",source_data_total,export_source,import_source)


output_P_MF_each_year.to_excel(path_output+"Price_MF_model_results.xlsx")
output_P_each_year.to_excel(path_output+"Price_model_results.xlsx")

quartly=pd.read_excel("NJORD-Price_model_results.xlsx",index_col=0,)
yearly=pd.DataFrame()
desiderio=["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"] #2008","2009","2010","2011","2012","2013","2014","2015","2016",
print(quartly.columns)
for nation in quartly.index:
    for year in desiderio:
        q1=quartly.loc[nation,"NJORD "+year+"-Q1"]
        q2 = quartly.loc[nation,"NJORD " + year + "-Q2"]
        q3 = quartly.loc[nation,"NJORD " + year + "-Q3"]
        q4 = quartly.loc[nation,"NJORD " + year + "-Q4"]
        if q1 <0:
            q1=0
        if q2 <0:
            q2=0
        if q3 <0:
            q3=0
        if q4 <0:
            q4=0
        somma=q1+q2+q3+q4
        yearly.at[nation,"NJORD "+year]=somma

for column in quartly.columns:
    if "NJORD" in str(column):
        continue
    else:
        to_add=quartly[column]
        yearly=yearly.join(to_add)

yearly.to_excel("NJORD-Price_model_results_year.xlsx")


Ref_country=["Belgium","Chile","Denmark","Finland","France","Israel","Italy","Spain","Sweden","Switzerland"]
Asia=["Afghanistan","Bangladesh","Bhutan","Brunei_Darussalam","Cambodia","China","Hong_Kong__China","India","Indonesia","Japan","Kazakhstan","Kyrgyzstan","Lao_People's_Democratic_Republic","Malaysia","Maldives","Myanmar","Nepal","Korea__Democratic_People's_Republic_of","Korea__Republic_of","Pakistan","Philippines","Singapore","Korea__Democratic_People's_Republic_of","Sri_Lanka","Taipei__Chinese","Tajikistan","Thailand","Turkmenistan","Uzbekistan","Viet_Nam","Mongolia"]
Europe=["Albania","Andorra","Austria","Belarus","Belgium","Bosnia_and_Herzegovina","Bulgaria","Croatia","Cyprus","Czech_Republic","Denmark","Estonia","Finland","France","Georgia","Germany","Greece","Greenland","Hungary","Iceland","Ireland","Italy","Latvia","Lithuania","Luxembourg","Macedonia__North","Malta","Moldova__Republic_of","Netherlands","Norway","Poland","Portugal","Romania","Russian_Federation","Serbia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Ukraine","United_Kingdom"]
Europa=["Albania","Andorra","Austria","Belarus","Belgium","Bosnia and Herzegovina","Bulgaria","Croatia","Cyprus","Czech Republic","Denmark","Estonia","Finland","France","Georgia","Germany","Greece","Greenland","Hungary","Iceland","Ireland","Italy","Latvia","Lithuania","Luxembourg","Macedonia  North","Malta","Moldova Republic of","Netherlands","Norway","Poland","Portugal","Romania","Russian Federation","Serbia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Ukraine","United Kingdom"]
Africa=["Algeria","Angola","Benin","Botswana","Burkina_Faso","Burundi","Cameroon","Cabo_Verde","Central_African_Republic","Comoros","Congo","Congo__Democratic_Republic_of_the","Djibouti","Egypt","Equatorial_Guinea","Eritrea","Ethiopia","Gabon","Gambia","Ghana","Guinea","Guinea_Bissau","Côte_d'Ivoire","Kenya","Lesotho","Liberia","Libya__State_of","Mayotte","Madagascar","Malawi","Mali","Mauritania","Mauritius","Morocco","Mozambique","Namibia","Niger","Nigeria","Rwanda","Saint_Helena","Sao_Tome_and_Principe","Senegal","Seychelles","Sierra_Leone","Somalia","South_Africa","South_Sudan","Sudan","Tanzania__United_Republic_of","Togo","Tunisia","Uganda","Western_Sahara","Zambia","Zimbabwe"]
North_America=["Bermuda","Canada","United_States_of_America","Mexico"]
Central_America=["Anguilla","Barbados","Belize","Costa_Rica","Cuba","Curaçao","Dominica","Dominican_Republic","El_Salvador","Grenada","Guatemala","Honduras","Nicaragua","Panama","Saint_Lucia","Saint_Vincent_and_the_Grenadines","Trinidad_and_Tobago","Antigua_and_Barbuda","Bahamas","Haiti","Jamaica"]
South_America=["Argentina","Bolivia__Plurinational_State_of","Brazil","Colombia","Chile","Ecuador","Guyana","Paraguay","Peru","Suriname","Uruguay","Venezuela__Bolivarian_Republic_of"]
Eurasia=["Armenia","Azerbaijan","Turkey"]
Oceania=["Australia","Fiji","Guam","Micronesia__Federated_States_of","Norfolk_Island","New_Caledonia","New_Zealand","Papua_New_Guinea","Solomon_Islands","Kiribati","New_Caledonia"]
Middle_East=["Bahrain","Iran__Islamic_Republic_of","Iraq","Israel","Jordan","Kuwait","Lebanon","Oman","Palau","Palestine__State_of","Qatar","Saudi_Arabia","Syrian_Arab_Republic","United_Arab_Emirates","Yemen","Kuwait","Lebanon","Jordan","Oman"]
indici=["Ref_country","Asia","Europe","Africa","North_America","Central_America","South_America","Eurasia","Oceania","Middle_East"]
reference_data_year=pd.read_excel("Reference_accumulated_2022.xlsx",index_col=0, na_values=['NA'])
Combined = pd.read_excel("NJORD-Price_model_results_year.xlsx",index_col=0, na_values=['NA'])

period_col=["NJORD 2010","Ref 2010","Source 2010","Diff 2010","NJORD 2011","Ref 2011","Source 2011","Diff 2011","NJORD 2012","Ref 2012","Source 2012","Diff 2012","NJORD 2013","Ref 2013","Source 2013","Diff 2013","NJORD 2014","Ref 2014","Source 2014","Diff 2014","NJORD 2015","Ref 2015","Source 2015","Diff 2015","NJORD 2016","Ref 2016","Source 2016","Diff 2016","NJORD 2017","Ref 2017","Source 2017","Diff 2017","NJORD 2018","Ref 2018","Source 2018","Diff 2018","NJORD 2019","Ref 2019","Source 2019","Diff 2019","NJORD 2020","Ref 2020","Source 2020","Diff 2020"]
#period=["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
output_column=["Absolut Country Average [%]","Total deviation for Data set [%]","Median [%]","Median [MW]","Standard deviation [MW]","Average deviation [MW]","T distribution [MW]"]
#Ref_country=Combined.index
Combined_region_results=pd.DataFrame()



for year in period_col:
    print(year)
    if "Ref" in year or "Source" in year or "Diff" in year:
        continue
    for region in indici:
        difference_sum = 0
        NJORD_value_sum = 0
        ref_value_sum = 0
        ref_tot_irena = 0
        ref_tot_pvps = 0
        ref_tot_other = 0
        for country in eval(region):
            print(country)
            #country=country.replace(" ","_")
            if country == "British_Indian_Ocean_Territory" or country == "Eswatini":
                continue
            only_year=year.split(" ")
            only_year=only_year[1]
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
            NJORD_value=Combined[year][country] ######################################## DATA SET ################## to change
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
            if NJORD_value <0:
                NJORD_value=0
                NJORD_value_sum = NJORD_value_sum + NJORD_value
            else:
                NJORD_value_sum = NJORD_value_sum + NJORD_value
            print(ref_value,source,country,year,"Referenza")
            ref_value_sum = ref_value_sum + ref_value
            print(ref_value_sum,"totale",region,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            ref_tot_irena = ref_tot_irena+reference_data_year[Irena][country]
            ref_tot_pvps = ref_tot_pvps+reference_data_year[PVPS][country]
            ref_tot_other = ref_tot_other+reference_data_year[other][country]
        print(NJORD_value_sum,"SOMMA!!!!!!!",region)
        region=region.replace("_"," ")

        Combined_region_results.at[region, "NJORD " + only_year] = NJORD_value_sum
        Combined_region_results.at[region, "Ref " + only_year] = ref_value_sum
        Combined_region_results.at[region, "IRENA " + only_year] = ref_tot_irena
        Combined_region_results.at[region, "PVPS " + only_year] = ref_tot_pvps
        Combined_region_results.at[region, "Other " + only_year] = ref_tot_other


Combined_region_results.to_excel("NJORD-Price_model_results_regions.xlsx")




