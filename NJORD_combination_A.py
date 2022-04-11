import NJORD_function_test
import pandas as pd
import os

path_input = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\Raw_data\\Final_database\\Price\\" # this is the path_out_final in the script From_html_to_db
path_output = "C:\\Users\\lucar\\PycharmProjects\\NJORD_2022_Feb\\"# this will be the folder from where the GUI will read the data

os.makedirs(path_output, exist_ok=True)
nations_list = os.listdir(path_input + "\\Export\\")
Europe = ["Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
          "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece",
          "Greenland", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
          "Macedonia  North", "Malta", "Moldova Republic of", "Netherlands", "Norway", "Poland", "Portugal", "Romania",
          "Russian Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine",
          "United Kingdom"]
# period = ["2009-Q4", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
#             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4", "2014-Q1",
#             "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2",
#             "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4", "2018-Q1", "2018-Q2", "2018-Q3",
#             "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]

outlier_Price = pd.read_excel("outlier_price_quarter.xlsx", index_col=0)
outlier_Weight = pd.read_excel("outlier_weight_quarter.xlsx", index_col=0)

def combination(input, outlier, period):

