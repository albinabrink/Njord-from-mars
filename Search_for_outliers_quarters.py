import pandas as pd

models=["NJORD-Price","NJORD-Weight"]
period=["2010-Q2","2010-Q3","2010-Q4","2011-Q1","2011-Q2","2011-Q3","2011-Q4","2012-Q1","2012-Q2","2012-Q3","2012-Q4","2013-Q1","2013-Q2","2013-Q3","2013-Q4","2014-Q1","2014-Q2","2014-Q3","2014-Q4","2015-Q1","2015-Q2","2015-Q3","2015-Q4","2016-Q1","2016-Q2","2016-Q3","2016-Q4","2017-Q1","2017-Q2","2017-Q3","2017-Q4","2018-Q1","2018-Q2","2018-Q3","2018-Q4","2019-Q1","2019-Q2","2019-Q3","2019-Q4","2020-Q1","2020-Q2","2020-Q3"]
colonne=["2010-Q2","2010-Q3","2010-Q4","2011-Q1","2011-Q2","2011-Q3","2011-Q4","2012-Q1","2012-Q2","2012-Q3","2012-Q4","2013-Q1","2013-Q2","2013-Q3","2013-Q4","2014-Q1","2014-Q2","2014-Q3","2014-Q4","2015-Q1","2015-Q2","2015-Q3","2015-Q4","2016-Q1","2016-Q2","2016-Q3","2016-Q4","2017-Q1","2017-Q2","2017-Q3","2017-Q4","2018-Q1","2018-Q2","2018-Q3","2018-Q4","2019-Q1","2019-Q2","2019-Q3","2019-Q4","2020-Q1","2020-Q2","2020-Q3"]

outliner_weight_max=pd.DataFrame(columns=colonne)
outliner_price_max=pd.DataFrame(columns=colonne)
among_negative_W_max=pd.DataFrame(columns=colonne)
among_negative_P_max=pd.DataFrame(columns=colonne)
among_negative_P_MF_max=pd.DataFrame(columns=colonne)
contatore_tot=0
contatore_2010=0
contatore_2011=0
contatore_2012 = 0
contatore_2013=0
contatore_2014=0
contatore_2015=0
contatore_2016=0
contatore_2017=0
contatore_2018=0
contatore_2019=0
contatore_2020=0
for item in models:  #loops for all the models
    data=pd.read_excel(item+"_model_results.xlsx",index_col=0)
    for nation in data.index: #loops for all the nations in the data
        for year in period: #loops for the years
            allert=False
            only_year=year.split("-")
            only_year =only_year[0]
            value_current=data.at[nation,"NJORD "+year]
            if "Q4" in year:
                value_prev=data.at[nation,"NJORD "+str(int(only_year))+"-Q3"]
            if "Q3" in year:
                value_prev=data.at[nation,"NJORD "+str(int(only_year))+"-Q2"]
            if "Q2" in year:
                value_prev=data.at[nation,"NJORD "+str(int(only_year))+"-Q1"]
            if "Q1" in year:
                value_prev=data.at[nation,"NJORD "+str(int(only_year)-1)+"-Q4"]
            if value_prev < 0 :
                value_prev=0.1
                allert=True
            if "Q4" in year:
                value_next=data.at[nation,"NJORD "+str(int(only_year)+1)+"-Q1"]
            if "Q3" in year:
                value_next=data.at[nation,"NJORD "+str(int(only_year))+"-Q4"]
            if "Q2" in year:
                value_next=data.at[nation,"NJORD "+str(int(only_year))+"-Q3"]
            if "Q1" in year:
                value_next=data.at[nation,"NJORD "+str(int(only_year))+"-Q2"]
            if value_next < 0 :
                value_next=0.1
                allert = True
            if allert:
                if "Weight" in item:
                    among_negative_W_max.at[nation, year] = "T-B-C"
                if "Price" in item:
                    among_negative_P_max.at[nation, year] = "T-B-C"
            if value_current >0 and value_prev >0 and value_next >0:
                if value_current > 3*value_prev and value_current > 2* value_next:
                    print("outliners",value_prev,value_current,value_next,year,item,nation)
                    if "Weight" in item:
                        outliner_weight_max.at[nation, year] = "Yes"
                    if "Price" in item:
                        outliner_price_max.at[nation, year] = "Yes"
                    contatore_tot=contatore_tot+1
                    if year=="2010":
                        contatore_2010=contatore_2010+1
                    if year=="2011":
                        contatore_2011=contatore_2011+1
                    if year=="2012":
                        contatore_2012=contatore_2012+1
                    if year=="2013":
                        contatore_2013=contatore_2013+1
                    if year=="2014":
                        contatore_2014=contatore_2014+1
                    if year=="2015":
                        contatore_2015=contatore_2015+1
                    if year=="2016":
                        contatore_2016=contatore_2016+1
                    if year=="2017":
                        contatore_2017=contatore_2017+1
                    if year=="2018":
                        contatore_2018=contatore_2018+1
                    if year=="2019":
                        contatore_2019=contatore_2019+1
                    if year=="2020":
                        contatore_2020=contatore_2020+1
                    #print(value_prev,value_current,value_next)

print(contatore_2010,"Total 2010")
print(contatore_2011,"Total 2011")
print(contatore_2012,"Total 2012")
print(contatore_2013,"Total 2013")
print(contatore_2014,"Total 2014")
print(contatore_2015,"Total 2015")
print(contatore_2016,"Total 2016")
print(contatore_2017,"Total 2017")
print(contatore_2018,"Total 2018")
print(contatore_2019,"Total 2019")
print(contatore_2020,"Total 2020")
print(contatore_tot,"Total outliners")
outliner_weight_max.to_excel("Outliners_weight_quarter.xlsx")
outliner_price_max.to_excel("Outliners_price_quarter.xlsx")

among_negative_W_max.to_excel("TBC_Weight_quarter.xlsx")
among_negative_P_max.to_excel("TBC_Price_quarter.xlsx")
