import os
import pandas as pd

unit = "weight"
path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

os.makedirs(path_output, exist_ok=True)
nations_list = os.listdir(path_input + "\\Export\\")

period = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]


def name_clean_up(nation_list):  # Clean up the names of nations from the raw database and return a list of countries
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


# print(name_clean_up(nations_list))
# test = name_clean_up(nations_list)
# test = "Algeria"
# period = "2018-Q1"
def manufacturing(nation, year):  # Extract the manufacturing for a nation in a specific year
    manufacturing_df = pd.read_excel("Manufacturing.xlsx", index_col=0, na_values=['NA'])
    manufacturing_df = manufacturing_df.fillna(0)
    print(manufacturing_df)
    year = year.split("-")
    year = year[0]
    if nation in manufacturing_df.index.values:
        manufacturing_value = manufacturing_df[year][nation]
        return manufacturing_value
    else:
        manufacturing_value = 0
        return manufacturing_value
# print(manufacturing(test, period))

