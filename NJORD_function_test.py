import os
import pandas as pd

unit = "weight"
path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\Raw_data\\Final_database\\Weight\\"  # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Albin\\"# this will be the folder from where the GUI will read the data

os.makedirs(path_output, exist_ok=True)
nations_list = os.listdir(path_input + "\\Export\\")


def name_clean_up(nation_list, period):
    print(nation_list)
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

    for name in nation_list:
        #print(name)
        name = name[0]
        #name = name.replace("_", " ")
        #print(name)
        # if int(year_test) <= 2016 and "before" in name:
        #    print("\n\nit is Sudan before so I change name for the reference\n\n", name)
        #    name = "Sudan"
    return nation_list


print(name_clean_up(nations_list, 0))