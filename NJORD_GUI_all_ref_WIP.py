from tkinter import *
import pandas as pd
import numpy as np
import matplotlib
import operator
import collections
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        #exit(self.qapp.exec_())
        root.mainloop()


matplotlib.use('Qt5Agg')
###############################################################################################################

#           This is the graphic interface to explore NJORD predictions. It is possible to plot the accumulated
#           installed capacity for each nation, for nations in the same region using 1 or 2 models

###############################################################################################################
root = Tk()
root.title("NJORD installed Capacity")
root.geometry("1200x750")
year = 2020
regions = ["Africa","Asia","Central America","Eurasia","Europe","Middle East","North America","Oceania","Ref. country","South America","World"]
list_colors = [(15,100,90,10), (0,90,85,0), (0,80,95,0), (0,50,100,0), (0,35,85,0), (5,0,90,0), (20,0,100,0), (50,0,100,0), (75,0,100,0), (85,10,100,10), (90,30,95,30)]
check_box_list = []
check_box_list2 = []
class ChecklistBox(Frame):
    def __init__(self, parent, choices, **kwargs):
        Frame.__init__(self, parent, **kwargs)

        self.vars = []
        bg = self.cget("background")
        for choice in choices:
            var = StringVar(value=choice)
            self.vars.append(var)
            cb = Checkbutton(self, var=var, text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0
            )
            cb.pack(side="top", fill="x", anchor="w")
    def getCheckedItems(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value:
                values.append(value)
        return values

#models=["NJORD-Weight","NJORD-Price","NJORD-Combined","Price","Price_MF","Price_max","Weight"]
models=["NJORD-Weight","NJORD-Price","NJORD-Combined"]

################################################################################################
#               To add more periods in these two variables as ,"2021-Q1","2021-Q2" etc...

desiderio = ["2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
             "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4",
             "2014-Q1", "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4",
             "2016-Q1", "2016-Q2", "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4",
             "2018-Q1", "2018-Q2", "2018-Q3", "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4",
             "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]

#label for the output
desiderio_lab = ["Prev", "2010-Q1", "2010-Q2", "2010-Q3", "2010-Q4", "2011-Q1", "2011-Q2", "2011-Q3", "2011-Q4",
                 "2012-Q1", "2012-Q2", "2012-Q3", "2012-Q4", "2013-Q1", "2013-Q2", "2013-Q3", "2013-Q4",
                 "2014-Q1", "2014-Q2", "2014-Q3", "2014-Q4", "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4",
                 "2016-Q1", "2016-Q2", "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4",
                 "2018-Q1", "2018-Q2", "2018-Q3", "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4",
                 "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4"]

# also this line has to be changed when increasing years...just change 2022 with the desired final year
#ax0.set_xticks((np.arange(2009, 2022, 1.0)))

labels_NJORD=["2009 NJ [MW]","2010 NJ [MW]","2011 NJ [MW]","2012 NJ [MW]","2013 NJ [MW]","2014 NJ [MW]","2015 NJ [MW]","2016 NJ [MW]","2017 NJ [MW]","2018 NJ [MW]","2019 NJ [MW]","2020 NJ [MW]",]
labels_reference=["2009 Ref. [MW]","2010 Ref. [MW]","2011 Ref. [MW]","2012 Ref. [MW]","2013 Ref. [MW]","2014 Ref. [MW]","2015 Ref. [MW]","2016 Ref. [MW]","2017 Ref. [MW]","2018 Ref. [MW]","2019 Ref. [MW]","2020 Ref. [MW]"]
year_2009_2020=["2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020",]
year_2010_2020=["2010","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020",]

################################################################################################


list_color_bc=["#C30017","#FF1926","#FF330D","#FF8000","#FFA626","#F2FF19","#CCFF00","#80FF00","#40FF00","#22CF00","#127D09"]
Ref_country=["Belgium","Chile","Denmark","Finland","France","Israel","Italy","Spain","Sweden","Switzerland"]
Asia=["Afghanistan","Bangladesh","Bhutan","Brunei Darussalam","Cambodia","China","Hong Kong","India","Indonesia","Japan","Kazakhstan","Kyrgyzstan","Laos","Malaysia","Maldives","Mongolia","Myanmar","Nepal","North Korea","South Korea","Pakistan","Philippines","Singapore","Sri_Lanka","Taiwan","Tajikistan","Thailand","Turkmenistan","Uzbekistan","Vietnam",]
Europe=["Albania","Andorra","Austria","Belarus","Belgium","Bosnia and Herzegovina","Bulgaria","Croatia","Cyprus","Czech Republic","Denmark","Estonia","Finland","France","Georgia","Germany","Greece","Greenland","Hungary","Iceland","Ireland","Italy","Latvia","Lithuania","Luxembourg","Macedonia","Malta","Moldova","Netherlands","Norway","Poland","Portugal","Romania","Russia","Serbia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Ukraine","United Kingdom"]
Africa=["Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi","Cameroon","Cabo Verde","Central African Republic","Comoros","Congo","Democratic Republic of the Congo","Djibouti","Egypt","Equatorial Guinea","Eritrea","Ethiopia","Gabon","Gambia","Ghana","Guinea","Guinea_Bissau","Côte dIvoire","Kenya","Lesotho","Liberia","Libya","Mayotte","Madagascar","Malawi","Mali","Mauritania","Mauritius","Morocco","Mozambique","Namibia","Niger","Nigeria","Rwanda","Saint Helena","Sao Tome and Principe","Senegal","Seychelles","Sierra Leone","Somalia","South Africa","South Sudan","Sudan","Tanzania","Togo","Tunisia","Uganda","Western_Sahara","Zambia","Zimbabwe"]
North_America=["Bermuda","Canada","United States of America","Mexico"]
Central_America=["Anguilla","Barbados","Belize","Costa Rica","Cuba","Curaçao","Dominica","Dominican Republic","El Salvador","Grenada","Guatemala","Honduras","Nicaragua","Panama","Saint Lucia","Saint Vincent and the Grenadines","Trinidad and Tobago","Antigua and Barbuda","Bahamas","Haiti","Jamaica"]
South_America=["Argentina","Bolivia","Brazil","Colombia","Chile","Ecuador","Guyana","Paraguay","Peru","Suriname","Uruguay","Venezuela"]
Eurasia=["Armenia","Azerbaijan","Turkey"]
Oceania=["Australia","Fiji","Guam","Micronesia","Norfolk Island","New_Caledonia","New Zealand","Papua New Guinea","Solomon Islands","Kiribati"]
Middle_East=["Bahrain","Iran","Iraq","Israel","Jordan","Kuwait","Lebanon","Oman","Palau","Palestine","Qatar","Saudi Arabia","Syria","United Arab Emirates","Yemen","Kuwait","Lebanon","Jordan","Oman"]
World=["Africa","Asia","Central America","Europe","North America","South America","Eurasia","Oceania","Middle East"]

dict_ref_country={}
dict_asia={}
dict_africa={}
dict_central_america={}
dict_north_america={}
dict_south_america={}
dict_europe={}
dict_oceania={}
dict_eurasia={}
dict_middle_east={}
output_table = pd.DataFrame()
ref_table = pd.DataFrame()

# In the visualization function are presented comments to explain the code. The other functions are similar.
# The only difference is in the plotting step, where in the two_model_comparison will be printed the results
# of the two different model for a single nation/region an in the two_states_comparison will be shown the result using the same model
# for two different nations/regions

def visualization(name,year,model):    #this is the part that plots the single nation or group using only 1 model
    output_table = pd.DataFrame()
    ref_table = pd.DataFrame()
    ref_table_irena = pd.DataFrame()
    ref_table_other = pd.DataFrame()
    ref_table_pvps = pd.DataFrame()
    ref_table_im = pd.DataFrame()
    ref_table_irena_sour = pd.DataFrame()
    cont_col = 0
    if my_entry_0.get() != "":  #check the input to decide if a single nation or more nation at the same time have to be presented
        if my_entry_0.get() == "World": # if World is selected
            posizione_testo = 0
            nation_order = []
            stacking = []
            stacking.append(0)
            aggiornamento = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0] #needed to stack the single nations NJORD output one on top of each other
            aggiornamento_ref = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]#needed to stack the single nations references one on top of each other
            aggiornamento_ref_irena = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]#needed to stack the single nations references one on top of each other
            aggiornamento_ref_other = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]#needed to stack the single nations references one on top of each other
            aggiornamento_ref_pvps = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]#needed to stack the single nations references one on top of each other

            fig, ax = plt.subplots(figsize=(18, 32))
            G = gridspec.GridSpec(2, 1) #divide the figure in a 2x2 matrix
            ax0 = plt.subplot(G[0, :]) # first row both columns
            ax1 = plt.subplot(G[1, :])# second row both column (in the other visualization options this is changed
            row_table = []
            for name in World:
                    NJORD = pd.read_excel(model + "_model_results_regions.xlsx", index_col=0) #read the NJORD value according to the model
                    accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0) #read the reference
                    accumulated_installed_2009 = accumulated_reference_data["2009 - Total"] #read the reference for 2009 that will be the starting point for the accumulated installed capacity
                    x_axis = []
                    x_axis_ref = []
                    source_list = []
                    source_list_irena = []
                    name = name.replace(" ", "_")  #needed to format the nation name for all the different source of data
                    row_table.append(name)
                    exec("%s_var_ref = []" % (name)) #create the variable used to store the data for each nation
                    exec("%s_var_ref_irena = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ref_pvps = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ref_other = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ref_im = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_njord = []" % (name)) #create the variable used to store the data for each nation
                    valore_y = round(float(accumulated_installed_2009[name.replace("_", " ")]),2)
                    print(valore_y)
                    (eval(name + "_var_njord")).append(valore_y)
                    x_axis.append(2009)
                    output_table.at[name, "2009 NJ [MW]"] = valore_y
                    ref_table.at[name, "2009 Ref. [MW]"] = valore_y
                    ref_table_irena.at[name,"2009 Irena [MW]"]=accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")]
                    ref_table_irena.at[name, "2009 Irena "] = accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")]
                    ref_table_other.at[name,"2009 other [MW]"]=accumulated_reference_data["2009 - Other"][name.replace("_", " ")]
                    ref_table_pvps.at[name,"2009 PVPS [MW]"]=accumulated_reference_data["2009 - PVPS"][name.replace("_", " ")]
                    #ref_table_im.at[name, "2009 IM [MW]"]=accumulated_reference_data["2009 - IM"][name.replace("_", " ")]
                    #source_list_irena.append(str(["2009 - IRENA s"][name.replace("_", " ")]))
                    (eval(name + "_var_ref")).append(accumulated_reference_data["2009 - Total"][name.replace("_", " ")])
                    (eval(name + "_var_ref_irena")).append(accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")])
                    (eval(name + "_var_ref_pvps")).append(accumulated_reference_data["2009 - PVPS"][name.replace("_", " ")])
                    (eval(name + "_var_ref_other")).append(accumulated_reference_data["2009 - Other"][name.replace("_", " ")])
                    #(eval(name + "_var_ref_im")).append(accumulated_reference_data["2009 - IM"][name.replace("_", " ")])
                    x_axis_ref.append(2009)

                    for anno in range(2010, int(year) + 1): #NJORD values, reference and reference source are extrapolated from 2010 till 2020 for each nation
                        valore_NJORD = NJORD["NJORD " + str(anno)][name.replace("_", " ")]
                        valore_reference = accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")]

                        print(valore_reference, "valore", source_list)
                        if valore_NJORD < 0: #if NJORD value is 0 it is not added to the sum
                            valore_y = float(valore_y)
                        else:
                            valore_y = float(valore_y) + float(NJORD["NJORD " + str(anno)][name.replace("_", " ")]) #increment of the NJORD variable
                        (eval(name + "_var_njord")).append(valore_y)
                        (eval(name + "_var_ref")).append(valore_reference)
                        (eval(name + "_var_ref_irena")).append(accumulated_reference_data[str(anno) + " - IRENA"][name.replace("_", " ")])
                        (eval(name + "_var_ref_pvps")).append(accumulated_reference_data[str(anno) + " - PVPS"][name.replace("_", " ")])
                        (eval(name + "_var_ref_other")).append(accumulated_reference_data[str(anno) + " - Other"][name.replace("_", " ")])
                        (eval(name + "_var_ref_im")).append(accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")])
                        output_table.at[name, str(anno)+" NJ [MW]"] = round(valore_y, 2)
                        ref_table.at[name, str(anno)+" Ref [MW]"] = round(valore_reference, 2)
                        #output_table.at[name, str(anno) + " Ref."] = round(valore_reference, 2)
                        x_axis.append(int(anno))
                        x_axis_ref.append((int(anno)))
                    shifts = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12] #needed to plot the reference data close to NJORD data
                    print(x_axis)
                    x_ax1 = np.add(x_axis, shifts) #needed to plot the reference data close to NJORD data
                    x_ax2 = np.subtract(x_axis, shifts) #needed to plot the reference data close to NJORD data
                    referenza = valore_comma.get() #option in the GUI to plot or not reference data
                    referenza_irena = valore_comma_irena.get()  # option in the GUI to plot or not reference data
                    referenza_other = valore_comma_other.get()  # option in the GUI to plot or not reference data
                    referenza_pvps = valore_comma_pvps.get()  # option in the GUI to plot or not reference data
                    if referenza ==1:
                        ax0.bar(x_ax1, eval(name + "_var_njord"), width=0.2, label=name.replace("_", " "),bottom=aggiornamento, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                        ax0.bar(x_ax2, eval(name + "_var_ref"), width=0.2,bottom=aggiornamento_ref, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2,alpha=0.3)
                        print("REFERENZA massima")
                    elif referenza_irena == 1:
                        ax0.bar(x_ax1, eval(name + "_var_njord"), width=0.2, label=name.replace("_", " "),
                                bottom=aggiornamento, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                        ax0.bar(x_ax2, eval(name + "_var_ref_irena"), width=0.2, bottom=aggiornamento_ref_irena,
                                color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2, alpha=0.3)
                        print("REFERENZA IRENA",eval(name + "_var_ref_irena"))
                    elif referenza_other == 1:
                        ax0.bar(x_ax1, eval(name + "_var_njord"), width=0.2, label=name.replace("_", " "),
                                bottom=aggiornamento, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                        ax0.bar(x_ax2, eval(name + "_var_ref_other"), width=0.2, bottom=aggiornamento_ref_other,
                                color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2, alpha=0.3)
                        print("REFERENZA Other")
                    elif referenza_pvps == 1:
                        ax0.bar(x_ax1, eval(name + "_var_njord"), width=0.2, label=name.replace("_", " "),
                                bottom=aggiornamento, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                        ax0.bar(x_ax2, eval(name + "_var_ref_pvps"), width=0.2, bottom=aggiornamento_ref_pvps,
                                color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2, alpha=0.3)
                        print("REFERENZA PVPS")
                    else:
                        x_ax1 = x_axis
                        ax0.bar(x_ax1, eval(name + "_var_njord"), width=0.2, label=name.replace("_", " "),
                                bottom=aggiornamento, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                        print("REFERENZA NESSUNA")


                    #creation of the bar plot stacking each new nation/region on top of each other
                    print(aggiornamento, "aggiornamento 0")
                    posizione_testo = posizione_testo + 1
                    ripartenza = eval(name + "_var_njord") #new NJORD value of single nation
                    aggiornamento = [x + y for x, y in zip(aggiornamento, ripartenza)] #old value plus the new value to continue the stacking of values
                    ripartenza_ref = eval(name + "_var_ref") #new ref value
                    aggiornamento_ref = [x + y for x, y in zip(aggiornamento_ref, ripartenza_ref)] #stacking reference
                    ripartenza_ref_irena = eval(name + "_var_ref_irena") #new ref value
                    aggiornamento_ref_irena = [x + y for x, y in zip(aggiornamento_ref_irena, ripartenza_ref_irena)] #stacking reference
                    ripartenza_ref_other = eval(name + "_var_ref_other") #new ref value
                    aggiornamento_ref_other = [x + y for x, y in zip(aggiornamento_ref_other, ripartenza_ref_other)] #stacking reference
                    ripartenza_ref_pvps = eval(name + "_var_ref_pvps") #new ref value
                    aggiornamento_ref_pvps = [x + y for x, y in zip(aggiornamento_ref_pvps, ripartenza_ref_pvps)] #stacking reference
                    print(ripartenza, "rip")
                    print(aggiornamento, "aggiornamento 2")
                    print(posizione_testo, "posizione testo")
                    cont_col = cont_col + 1
            if referenza == 1 or referenza_irena==1 or referenza_other==1 or referenza_pvps==1:
                ax0.bar(2020, 0, width=0.2, label="References", color="blue",alpha=0.1)

            # plotting the total value in the figure
            ax0.text(x_ax1[0], aggiornamento[0], round(aggiornamento[0], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[1], aggiornamento[1], round(aggiornamento[1], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[2], aggiornamento[2], round(aggiornamento[2], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[3], aggiornamento[3], round(aggiornamento[3], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[4], aggiornamento[4], round(aggiornamento[4], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[5], aggiornamento[5], round(aggiornamento[5], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[6], aggiornamento[6], round(aggiornamento[6], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[7], aggiornamento[7], round(aggiornamento[7], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[8], aggiornamento[8], round(aggiornamento[8], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[9], aggiornamento[9], round(aggiornamento[9], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[10], aggiornamento[10], round(aggiornamento[10], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[11], aggiornamento[11], round(aggiornamento[11], 2), verticalalignment='bottom',horizontalalignment='left')
            # table with the information on each single nation
            the_table = ax1.table(cellText=output_table.values, colLabels=labels_NJORD, rowLabels=row_table,loc="best")
            the_table.auto_set_column_width(col=list(range(len(output_table.columns))))
            the_table.auto_set_font_size(False)
            the_table.set_fontsize(10)
            the_table.scale(1, 1.5)

            # the_table.auto_set_row_width(row=list(range(len(output_table.rows))))

            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis("off")

            ax0.set_title("Predicted accumulated capacity [MW] for "+r"$\bf{" + str(my_list_0.get(ANCHOR)) + "}$ using "+ r"$\bf{" + str(my_list_2.get(ANCHOR).replace("_","-")) + "}$ model", fontsize=25,  loc="center")
            ax0.set_xlabel("Year", fontsize=20)
            ax0.set_ylabel("Accumulated capacity [MW]", fontsize=20)
            ax0.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax0.set_xticks((np.arange(2009, 2021, 1.0)))
            plt.tight_layout()
            a = ScrollableWindow(fig) #if Wor #
        else:
            ### similar with the World plot, commented only the differences
            posizione_testo = 0
            nation_order = []
            stacking = []
            stacking.append(0)
            aggiornamento = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            aggiornamento_ref = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            aggiornamento = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0]  # needed to stack the single nations NJORD output one on top of each other
            aggiornamento_ref = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0]  # needed to stack the single nations references one on top of each other
            aggiornamento_ref_irena = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0]  # needed to stack the single nations references one on top of each other
            aggiornamento_ref_other = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0]  # needed to stack the single nations references one on top of each other
            aggiornamento_ref_pvps = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0]  # needed to stack the single nations references one on top of each other
            # here are readed the dictionary linked to the check boxes in the GUI to show only
            # NJORD values of the checked nations
            if my_list_0.get(ANCHOR) == "Africa":
                dictionary = dict_africa
            if my_list_0.get(ANCHOR) == "Asia":
                dictionary = dict_asia
            if my_list_0.get(ANCHOR) == "Central America":
                dictionary = dict_central_america
            if my_list_0.get(ANCHOR) == "Eurasia":
                dictionary = dict_eurasia
            if my_list_0.get(ANCHOR) == "Europe":
                dictionary = dict_europe
            if my_list_0.get(ANCHOR) == "Middle East":
                dictionary = dict_middle_east
            if my_list_0.get(ANCHOR) == "North America":
                dictionary = dict_north_america
            if my_list_0.get(ANCHOR) == "Oceania":
                dictionary = dict_oceania
            if my_list_0.get(ANCHOR) == "Ref. country":
                dictionary = dict_ref_country
            if my_list_0.get(ANCHOR) == "South America":
                dictionary = dict_south_america
            fig, ax = plt.subplots(figsize=(20, 40))
            G = gridspec.GridSpec(2, 1)
            ax0 = plt.subplot(G[0, :])
            ax1 = plt.subplot(G[1, :])
            row_table = []
            variable_list = []
            for name, value in zip(dictionary, dictionary.values()):
                # print(name,value.get())
                # print(dict_asia[name])
                if cont_col == 10:
                    cont_col = 0
                if value.get() == 0:
                    print(name)  # check if the nation has been checked in the GUI
                    continue
                else:
                    row_table.append(name)  # needed during the plot to plot all the nation
                    print(name)
                    name = name.replace(" ", "_")
                    print(name, "dopo")
                    nation_order.append(name)
                    exec("%s_var_ref = []" % (name))
                    exec("%s_var_njord = []" % (name))
                    exec("%s_var_ref_irena = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ref_pvps = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ref_other = []" % (name))  # create the variable used to store the data for each nation
                    exec("%s_var_ref_im = []" % (name))  # create the variable used to store the data for each nation

                    variable_list.append(name + "_var_njord")  # needed during the plot to plot all the nation
                    # print(eval(name + "_var_njord"))
                    NJORD = pd.read_excel(model + "_model_results_year.xlsx", index_col=0)
                    accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
                    accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
                    x_axis = []
                    x_axis_ref = []
                    source_list = []
                    valore_y = float(accumulated_installed_2009[name.replace("_", " ")])
                    print(valore_y)
                    (eval(name + "_var_njord")).append(valore_y)
                    x_axis.append(2009)
                    output_table.at[name, "2009 NJ [MW]"] = valore_y
                    ref_table.at[name, "2009 Ref. [MW]"] = accumulated_reference_data["2009 - Total"][
                        name.replace("_", " ")]
                    (eval(name + "_var_ref")).append(accumulated_reference_data["2009 - Total"][name.replace("_", " ")])

                    x_axis_ref.append(2009)
                    source_0 = (NJORD["Source 2009"][name.replace("_", " ")])
                    if source_0 == "Irena":
                        lettera = "Irena"
                    if source_0 == "No Ref":
                        lettera = "No ref"
                    if source_0 == "Other":
                        lettera = "Other"
                    if source_0 == "PVPS":
                        lettera = "PVPS"
                    if name in regions:
                        lettera = "regions"
                    source_list.append("SP")
                    for anno in range(2010, int(year) + 1):
                        valore_NJORD = NJORD["NJORD " + str(anno)][name.replace("_", " ")]
                        valore_reference = accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")]
                        source = NJORD["Source " + str(anno)][name.replace("_", " ")]
                        if source == "Irena":
                            lettera = "Irena"
                        if source == "No Ref":
                            lettera = "No ref"
                        if source == "Other":
                            lettera = "Other"
                        if source == "PVPS":
                            lettera = "PVPS"
                        source_list.append(lettera)
                        print(valore_reference, "valore", source_list)
                        if valore_NJORD < 0:
                            valore_y = float(valore_y)
                        else:
                            valore_y = float(valore_y) + float(NJORD["NJORD " + str(anno)][name.replace("_", " ")])
                        (eval(name + "_var_njord")).append(valore_y)
                        (eval(name + "_var_ref")).append(valore_reference)
                        (eval(name + "_var_ref_irena")).append(
                            accumulated_reference_data[str(anno) + " - IRENA"][name.replace("_", " ")])
                        (eval(name + "_var_ref_pvps")).append(
                            accumulated_reference_data[str(anno) + " - PVPS"][name.replace("_", " ")])
                        (eval(name + "_var_ref_other")).append(
                            accumulated_reference_data[str(anno) + " - Other"][name.replace("_", " ")])
                        (eval(name + "_var_ref_im")).append(
                            accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")])
                        x_axis.append(int(anno))
                        x_axis_ref.append((int(anno)))
                        output_table.at[name, str(anno) + " NJ [MW]"] = round(valore_y, 2)
                        ref_table.at[name, str(anno) + " Ref [MW]"] = round(valore_reference, 2)
            final_order = {}
            all_max = []
            # stack the NJORD values and references for the bar plot of the selected nations and order the nations
            # to have as first 10 nations the ones with higher max increase for the whole period
            for treno in variable_list:
                exec("%s_diff = []" % (treno))
                exec("%s_max = []" % (treno))
                for i in range(0, len(eval(treno)) - 1):
                    eval(treno + "_diff").append(eval(treno)[i + 1] - eval(treno)[i])
                eval(treno + "_max").append(max(eval(treno + "_diff")))
                print(eval(treno + "_max"), "massimi!!!!")
                final_order[treno] = max(eval(treno + "_diff"))
            print(final_order, "ORDINE FINALE PRIMA")
            final_order = sorted(final_order.items(), key=operator.itemgetter(1), reverse=True)
            final_order_2 = collections.OrderedDict(final_order)
            print(final_order_2, "ORDINE FINALE DOPO")
            # print(max(diff),"massimo")
            cont_col = 0
            aggiornamento_new = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            aggiornamento_ref_new = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            num_other = 0
            shifts = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12]
            print(x_axis)
            x_ax1 = np.add(x_axis, shifts)
            x_ax2 = np.subtract(x_axis, shifts)
            referenza = valore_comma.get()
            ### plot only the first 10 nations with a unique color and put all the other nation in a single box with the same color
            for key in final_order_2.keys():
                if cont_col < 10:
                    print(key, "&&&&&&&&&&&&&&&&&&&&&&&66")
                    if referenza == 1:
                        ax0.bar(x_ax1, eval(key), width=0.2, label=key.replace("_var_njord", " "), bottom=aggiornamento,
                                color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                        ax0.bar(x_ax2, eval(key.replace("njord", "ref")), width=0.2, bottom=aggiornamento_ref,
                                color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2, alpha=0.3)
                    else:
                        x_ax1 = x_axis
                        ax0.bar(x_ax1, eval(key), width=0.2, label=key.replace("_var_njord", " "), bottom=aggiornamento,
                                color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                    ripartenza = eval(key)
                    aggiornamento = [x + y for x, y in zip(aggiornamento, ripartenza)]
                    cont_col = cont_col + 1
                    ripartenza_ref = eval(key.replace("njord", "ref"))
                    aggiornamento_ref = [x + y for x, y in zip(aggiornamento_ref, ripartenza_ref)]
                    ripartenza_ref_irena = eval(key.replace("var_njord", "") + "var_ref_irena")  # new ref value
                    aggiornamento_ref_irena = [x + y for x, y in
                                               zip(aggiornamento_ref_irena, ripartenza_ref_irena)]  # stacking reference
                    ripartenza_ref_other = eval(key.replace("var_njord", "") + "var_ref_other")  # new ref value
                    aggiornamento_ref_other = [x + y for x, y in
                                               zip(aggiornamento_ref_other, ripartenza_ref_other)]  # stacking reference
                    ripartenza_ref_pvps = eval(key.replace("var_njord", "") + "var_ref_pvps")  # new ref value
                    aggiornamento_ref_pvps = [x + y for x, y in zip(aggiornamento_ref_pvps, ripartenza_ref_pvps)]
                else:
                    print(key)
                    ripartenza = eval(key)
                    aggiornamento_new = [x + y for x, y in zip(aggiornamento_new, ripartenza)]
                    num_other = num_other + 1
                    ripartenza_ref = eval(key.replace("njord", "ref"))
                    aggiornamento_ref_new = [x + y for x, y in zip(aggiornamento_ref_new, ripartenza_ref)]
                    ripartenza_ref_irena = eval(key.replace("var_njord", "") + "var_ref_irena")  # new ref value
                    aggiornamento_ref_irena = [x + y for x, y in
                                               zip(aggiornamento_ref_irena, ripartenza_ref_irena)]  # stacking reference
                    ripartenza_ref_other = eval(key.replace("var_njord", "") + "var_ref_other")  # new ref value
                    aggiornamento_ref_other = [x + y for x, y in
                                               zip(aggiornamento_ref_other, ripartenza_ref_other)]  # stacking reference
                    ripartenza_ref_pvps = eval(key.replace("var_njord", "") + "var_ref_pvps")  # new ref value
                    aggiornamento_ref_pvps = [x + y for x, y in zip(aggiornamento_ref_pvps, ripartenza_ref_pvps)]
            referenza = valore_comma.get()  # option in the GUI to plot or not reference data
            referenza_irena = valore_comma_irena.get()  # option in the GUI to plot or not reference data
            referenza_other = valore_comma_other.get()  # option in the GUI to plot or not reference data
            referenza_pvps = valore_comma_pvps.get()  #
            if cont_col >= 10:
                if referenza == 1:
                    ax0.bar(x_ax1, aggiornamento_new, width=0.2, label="Other " + str(num_other) + " nations",
                            bottom=aggiornamento, color=list_color_bc[10], edgecolor='black', linewidth=1.2)
                    ax0.bar(x_ax2, aggiornamento_ref_new, width=0.2, bottom=aggiornamento_ref, color=list_color_bc[10],
                            edgecolor='black', linewidth=1.2, alpha=0.3)
                else:
                    x_ax1 = x_axis
                    ax0.bar(x_ax1, aggiornamento_new, width=0.2, label="Other " + str(num_other) + " nations",
                            bottom=aggiornamento, color=list_color_bc[10], edgecolor='black', linewidth=1.2)
            if cont_col >= 10:
                color_1 = "gray"
                alpha_1 = 0.8
                color_2 = "black"
                alpha_2 = 1
            else:
                color_1 = "black"
                alpha_1 = 1
                color_2 = "black"
                alpha_2 = 1

            # plotting of the sum of each year
            if cont_col >= 10:
                ax0.text(x_ax1[0], aggiornamento[0] + aggiornamento_new[0],
                         round(aggiornamento[0] + aggiornamento_new[0], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[1], aggiornamento[1] + aggiornamento_new[1],
                         round(aggiornamento[1] + aggiornamento_new[1], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[2], aggiornamento[2] + aggiornamento_new[2],
                         round(aggiornamento[2] + aggiornamento_new[2], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[3], aggiornamento[3] + aggiornamento_new[3],
                         round(aggiornamento[3] + aggiornamento_new[3], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[4], aggiornamento[4] + aggiornamento_new[4],
                         round(aggiornamento[4] + aggiornamento_new[4], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[5], aggiornamento[5] + aggiornamento_new[5],
                         round(aggiornamento[5] + aggiornamento_new[5], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[6], aggiornamento[6] + aggiornamento_new[6],
                         round(aggiornamento[6] + aggiornamento_new[6], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[7], aggiornamento[7] + aggiornamento_new[7],
                         round(aggiornamento[7] + aggiornamento_new[7], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[8], aggiornamento[8] + aggiornamento_new[8],
                         round(aggiornamento[8] + aggiornamento_new[8], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[9], aggiornamento[9] + aggiornamento_new[9],
                         round(aggiornamento[9] + aggiornamento_new[9], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[10], aggiornamento[10] + aggiornamento_new[10],
                         round(aggiornamento[10] + aggiornamento_new[10], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)
                ax0.text(x_ax1[11], aggiornamento[11] + aggiornamento_new[11],
                         round(aggiornamento[11] + aggiornamento_new[11], 2), verticalalignment='bottom',
                         horizontalalignment='left', color=color_2, alpha=alpha_2)

            ax0.text(x_ax1[0], aggiornamento[0], round(aggiornamento[0], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[1], aggiornamento[1], round(aggiornamento[1], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[2], aggiornamento[2], round(aggiornamento[2], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[3], aggiornamento[3], round(aggiornamento[3], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[4], aggiornamento[4], round(aggiornamento[4], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[5], aggiornamento[5], round(aggiornamento[5], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[6], aggiornamento[6], round(aggiornamento[6], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[7], aggiornamento[7], round(aggiornamento[7], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[8], aggiornamento[8], round(aggiornamento[8], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[9], aggiornamento[9], round(aggiornamento[9], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[10], aggiornamento[10], round(aggiornamento[10], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            ax0.text(x_ax1[11], aggiornamento[11], round(aggiornamento[11], 2), verticalalignment='bottom',
                     horizontalalignment='left', color=color_1, alpha=alpha_1)
            if referenza == 1:
                ax0.bar(2020, 0, width=0.2, label="References", edgecolor='black', color="blue", alpha=0.1)
            # print(aggiornamento,"aggiornamento 0")
            posizione_testo = posizione_testo + 1
            # ripartenza=eval(treno)
            # aggiornamento = [x + y for x, y in zip(aggiornamento, ripartenza)]
            the_table = ax1.table(cellText=output_table.values, colLabels=labels_NJORD, rowLabels=row_table, loc="best")
            the_table.auto_set_column_width(col=list(range(len(output_table.columns))))
            the_table.auto_set_font_size(False)
            the_table.set_fontsize(10)
            the_table.scale(1, 1.5)
            # the_table.auto_set_row_width(row=list(range(len(output_table.rows))))
            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis("off")
            ax0.set_title("Predicted accumulated capacity [MW] for " + r"$\bf{" + str(
                my_list_0.get(ANCHOR)) + "}$ using " + r"$\bf{" + str(
                my_list_2.get(ANCHOR).replace("_", "-")) + "}$ model", fontsize=24, loc="center")
            ax0.set_xlabel("Year", fontsize=20)
            ax0.set_ylabel("Accumulated capacity [MW]", fontsize=20)
            ax0.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax0.set_xticks((np.arange(2009, 2021, 1.0)))
            plt.tight_layout()
            a = ScrollableWindow(fig)
            # plt.show()
    else:
        ### this is the part of the code that is performed if the region box is empty. In this case, the single nations
        ### input will be read.
        NJORD=pd.read_excel(model+"_model_results.xlsx",index_col=0)
        accumulated_reference_data=pd.read_excel("Reference_accumulated_2022.xlsx",index_col=0)
        accumulated_installed_2009=accumulated_reference_data["2009 - Total"]
        ref_irena = []
        ref_pvps = []
        ref_other = []
        ref_im = []
        x_axis=[]
        y_axis=[]
        y_axis_ref=[]
        x_axis_ref=[]
        source_list=[]
        valore_y=float(accumulated_installed_2009[name])
        print(valore_y)
        y_axis.append(valore_y)
        x_axis.append(2009.75)
        y_axis_ref.append(accumulated_reference_data["2009 - Total"][name])
        x_axis_ref.append(2010)
        output_table.at["2009", "NJORD [MW]"] = "-"
        output_table.at["2009", "Ref. value [MW]"] = accumulated_reference_data["2009 - Total"][name]
        ref_table_irena.at["2009", " Irena [MW]"] = accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")]
        #ref_table_irena.at["2009", " Irena source"] = accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")]
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "q":
            ref_table_irena.at["2009", " Irena source"] = "Questionnaire"
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "o":
            ref_table_irena.at["2009", " Irena source"] = "Official"
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "u":
            ref_table_irena.at["2009", " Irena source"] = "Unofficial"
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "e":
            ref_table_irena.at["2009", " Irena source"] = "Estimates"
        ref_table_other.at["2009", " Other [MW]"] = accumulated_reference_data["2009 - Other"][name.replace("_", " ")]
        ref_table_pvps.at["2009", " PVPS [MW]"] = accumulated_reference_data["2009 - PVPS"][name.replace("_", " ")]
        # ref_table_im.at[name, "2009 IM [MW]"]=accumulated_reference_data["2009 - IM"][name.replace("_", " ")]
        ref_irena.append(accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")])
        ref_pvps.append(accumulated_reference_data["2009 - PVPS"][name.replace("_", " ")])
        ref_other.append(accumulated_reference_data["2009 - Other"][name.replace("_", " ")])
        # (eval(name + "_var_ref_im")).append(accumulated_reference_data["2009 - IM"][name.replace("_", " ")])
        source_0=(NJORD["Source 2009"][name])
        if source_0 == "Irena":
            lettera = "Irena"
        if source_0 == "No Ref":
            lettera = "No ref"
        if source_0 == "Other":
            lettera = "Other"
        if source_0 == "PVPS":
            lettera = "PVPS"
        if name in regions:
            lettera="regions"
        output_table.at["2009", "Ref. Source"] = source_0
        source_list.append("SP")
        x_value=2009.75
        for anno in desiderio:
            only_anno=anno.split("-")
            only_anno=only_anno[0]
            valore_NJORD=NJORD["NJORD "+str(anno)][name]
            valore_reference=accumulated_reference_data[str(only_anno)+" - Total"][name]
            source=NJORD["Source " + str(only_anno)][name]
            if source == "Irena":
                lettera="Irena"
            if source =="No Ref":
                lettera="No ref"
            if source =="Other":
                lettera="Other"
            if source=="PVPS":
                lettera="PVPS"
            source_list.append(lettera)
            output_table.at[anno, "Ref. Source"] = lettera
            print(valore_reference,"valore",source_list)
            if valore_NJORD < 0:
                valore_y = float(valore_y)
            else:
                valore_y=float(valore_y)+float(NJORD["NJORD "+str(anno)][name])
            output_table.at[anno, "NJORD [MW]"] =round(valore_y,2)
            output_table.at[anno, "Ref. value [MW]"]=valore_reference
            ref_table_irena.at[anno, " Irena [MW]"] = accumulated_reference_data[str(only_anno)+" - IRENA"][name.replace("_", " ")]
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "q":
                ref_table_irena.at[anno, " Irena source"] = "Questionnaire"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "o":
                ref_table_irena.at[anno, " Irena source"] = "Official"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "u":
                ref_table_irena.at[anno, " Irena source"] = "Unofficial"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "e":
                ref_table_irena.at[anno, " Irena source"] = "Estimates"

            ref_table_other.at[anno, " Other [MW]"] = accumulated_reference_data[str(only_anno)+" - Other"][name.replace("_", " ")]
            ref_table_pvps.at[anno, " PVPS [MW]"] = accumulated_reference_data[str(only_anno)+" - PVPS"][name.replace("_", " ")]
            y_axis.append(valore_y)
            y_axis_ref.append(valore_reference)
            ref_irena.append(accumulated_reference_data[str(only_anno) + " - IRENA"][name.replace("_", " ")])
            ref_pvps.append(accumulated_reference_data[str(only_anno) + " - PVPS"][name.replace("_", " ")])
            ref_other.append(accumulated_reference_data[str(only_anno) + " - Other"][name.replace("_", " ")])
            ref_im.append(accumulated_reference_data[str(only_anno) + " - Total"][name.replace("_", " ")])
            x_value=x_value+0.25
            x_axis.append(x_value)
            if only_anno =="2009":
                x_axis_ref.append(2009)
                continue
            else:
                x_axis_ref.append((int(only_anno)+1))

        fig, ax = plt.subplots(figsize=(18,30))
        G = gridspec.GridSpec(3, 1)
        ax0 = plt.subplot(G[0, 0])
        ax1 = plt.subplot(G[1:2, 0])
        #ax2 = plt.subplot(G[-1, 1])

        xlabell = "References source for each year: "
        for i in range(1, len(x_axis)):
            xlabell = str(xlabell) + r"$\bf{" + str(source_list[i]) + ",   " + "}$"

        referenza = valore_comma.get()
        referenza_irena = valore_comma_irena.get()  # option in the GUI to plot or not reference data
        referenza_other = valore_comma_other.get()  # option in the GUI to plot or not reference data
        referenza_pvps = valore_comma_pvps.get()
        if referenza_pvps==1:
            ax0.plot(x_axis_ref, ref_pvps, marker="<", label="PVPS ref", alpha=0.3)
            output_table=output_table.join(ref_table_pvps)
        if referenza_irena==1:
            ax0.plot(x_axis_ref, ref_irena, marker="^", label="Ref Irena", alpha=0.3)
            output_table = output_table.join(ref_table_irena)

        if referenza_other==1:
            ax0.plot(x_axis_ref, ref_other, marker="*", label="Ref Other", alpha=0.3)
            output_table = output_table.join(ref_table_other)
        if referenza == 0:
            print("no ref")
        else:
            ax0.plot(x_axis_ref, y_axis_ref, marker="+", label="Reference", alpha=0.3,color="#FF1926")
        # ax.text(min(x_axis), max(y_axis), 'boxed italics text in data coords', style='italic',bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        ax0.legend()

        #the_table.auto_set_column_width(col=list(range(len(output_table.columns))))
        #axs[1].xaxis.set_visible(False)
        #axs[1].yaxis.set_visible(False)
        #axs[1].axis("off")
        #the_table.set_fontsize(8)
        #the_table.scale(1, 1.5)
        ax0.set_xticks((np.arange(2009, 2022, 1.0)))
        #plt.tight_layout()
        # plt.subplots_adjust(left=0.2, top=0.8)
        #a = ScrollableWindow(fig)
        #plt.show()
        #root.mainloop()
        print(len(output_table.values),len(desiderio_lab),len(output_table.columns))
        the_table_1 = ax1.table(cellText=output_table.values, rowLabels=desiderio_lab, colLabels=output_table.columns,
                                loc="best")
        the_table_1.auto_set_column_width(col=list(range(len(output_table.columns))))
        # ax.set(xlabel=str(xlabell),ylabel="Accumulated capacity [MW]",fontsize=10)
        # ax.set(xlabel="Year \nReferences:"+str(x_axis[0])+":"+str(source_list[0])+", "+str(x_axis[1])+":"+str(source_list[1])+", "+str(x_axis[2])+":"+str(source_list[2])+", "+str(x_axis[3])+":"+str(source_list[3])+", "+str(x_axis[4])+":"+str(source_list[4])+", "+str(x_axis[5])+":"+str(source_list[5])+", "+str(x_axis[6])+":"+str(source_list[6]),ylabel="Accumulated capacity [MW]",title="Accumulated installed capacity for "+r"$\bf{" + name + "}$"+"\n NJORD value: "+str(round(valore_y,2))+"MW and reference value: "+ str(round(valore_reference,2))+"MW\n")
        # axs[1].set_title("\n \n NJORD value: "+str(round(valore_y,2))+"MW  Total reference value: "+ str(round(valore_reference,2))+"MW\n",fontsize=14)
        ax0.set_title("" + "Accumulated installed capacity for " + r"$\bf{" + name + "}$ ", fontsize=18)
        ax0.plot(x_axis, y_axis, marker="o", label=model, alpha=0.6,color="#C30017")
        the_table_1.auto_set_font_size(False)
        the_table_1.set_fontsize(10)
        the_table_1.scale(1, 1.5)
        ax1.set_title("Result for model: "r"$\bf{" + model + "}$ ", fontsize=16 )
        ax1.xaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
        ax1.axis("off")
        ax0.set_xlabel("Year", fontsize=10)
        ax0.set_ylabel("Accumulated capacity [MW]", fontsize=15)
        #ax0.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax0.legend()
        ax0.set_xticks((np.arange(2009, 2022, 1.0)))
        a = ScrollableWindow(fig)
        fig.tight_layout()
        print("stampo")
        #plt.show()
        root.mainloop()

def two_model_comparison(name,year,model_1,model_2):
    output_table_model1 = pd.DataFrame()
    output_table_model2 = pd.DataFrame()
    output_table_ref=pd.DataFrame()
    cont_col=0
    ref_table = pd.DataFrame()
    ref_table_irena = pd.DataFrame()
    ref_table_other = pd.DataFrame()
    ref_table_pvps = pd.DataFrame()
    if my_entry_0.get() != "":
        nation_order = []
        stacking = []
        stacking.append(0)
        aggiornamento_1 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        aggiornamento_1_ref = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        aggiornamento_2 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        row_table = []
        if my_entry_0.get() == "World":
            fig, ax = plt.subplots(figsize=(20, 40))
            G = gridspec.GridSpec(3, 1)#,width_ratios=[1],height_ratios=[1,0.1,0.1])
            ax0 = plt.subplot(G[0, :])
            ax1 = plt.subplot(G[2, :])
            ax2 = plt.subplot(G[1, :])
            for name in World:
                print(name, "name")
                row_table.append(name)
                print(row_table, "row")
                print(name)
                name = name.replace(" ", "_")
                print(name, "dopo")
                nation_order.append(name)
                exec("%s_var_ref_model_1 = []" % (name))
                exec("%s_var_njord_model_1= []" % (name))
                exec("%s_var_ref_model_2 = []" % (name))
                exec("%s_var_njord_model_2= []" % (name))
                # print(eval(name + "_var_njord"))
                NJORD_model_1 = pd.read_excel(model_1 + "_model_results_regions.xlsx", index_col=0)
                NJORD_model_2 = pd.read_excel(model_2 + "_model_results_regions.xlsx", index_col=0)
                accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
                accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
                x_axis = []
                x_axis_ref = []
                valore_y_1 = 0
                valore_y_2 = 0
                source_list = []
                valore_y_1 = round(float(accumulated_installed_2009[name.replace("_", " ")]), 2)
                valore_y_2 = round(float(accumulated_installed_2009[name.replace("_", " ")]), 2)
                print(valore_y_1)
                (eval(name + "_var_njord_model_1")).append(valore_y_1)
                (eval(name + "_var_njord_model_2")).append(valore_y_2)
                x_axis.append(2009)
                (eval(name + "_var_ref_model_1")).append(accumulated_reference_data["2009 - Total"][name.replace("_", " ")])
                (eval(name + "_var_ref_model_2")).append(accumulated_reference_data["2009 - Total"][name.replace("_", " ")])
                x_axis_ref.append(2009)
                output_table_ref.at[name, "2009 Ref"] = round(accumulated_installed_2009[name.replace("_", " ")],2)
                # output_table_model2.at[name, "2009 Ref"] = round(accumulated_installed_2009[name.replace("_", " ")],2)
                output_table_model1.at[name, "2009 [MW]"] = round(accumulated_installed_2009[name.replace("_", " ")],2)
                output_table_model2.at[name, "2009 [MW]"] = round(accumulated_installed_2009[name.replace("_", " ")],2)

                for anno in range(2010, int(year) + 1):
                    valore_NJORD_1 = NJORD_model_1["NJORD " + str(anno)][name.replace("_", " ")]
                    valore_NJORD_2 = NJORD_model_2["NJORD " + str(anno)][name.replace("_", " ")]
                    valore_reference = accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")]

                    print(valore_reference, "valore", source_list)
                    if valore_NJORD_1 < 0:
                        valore_y_1 = float(valore_y_1)
                    else:
                        valore_y_1 = float(valore_y_1) + float(NJORD_model_1["NJORD " + str(anno)][name.replace("_", " ")])
                    if valore_NJORD_2 < 0:
                        valore_y_2 = float(valore_y_2)
                    else:
                        valore_y_2 = float(valore_y_2) + float(NJORD_model_2["NJORD " + str(anno)][name.replace("_", " ")])
                    output_table_model1.at[name, str(anno)+" [MW]"] = round(valore_y_1, 2)
                    output_table_model2.at[name, str(anno)+" [MW]"] = round(valore_y_2, 2)
                    #output_table_model1.at[name, str(anno)+" Ref"] = round(valore_y_1, 2)
                    output_table_ref.at[name, str(anno)+" Ref"] = round(valore_y_2, 2)
                    (eval(name + "_var_njord_model_1")).append(valore_y_1)
                    (eval(name + "_var_ref_model_1")).append(valore_reference)
                    (eval(name + "_var_njord_model_2")).append(valore_y_2)
                    (eval(name + "_var_ref_model_2")).append(valore_reference)
                    x_axis.append(int(anno))
                    x_axis_ref.append((int(anno)))
                shifts = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12]
                print(x_axis)
                x_ax1 = np.add(x_axis, shifts)
                x_ax2 = np.subtract(x_axis, shifts)
                referenza = valore_comma.get()
                if referenza == 1:
                    shifts = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
                    print(x_axis)
                    x_ax1 = np.add(x_axis, shifts)
                    x_ax2 = np.subtract(x_axis, shifts)
                    print(eval(name + "_var_ref_model_1"),"valore referenza!!!!")
                    ax0.bar(x_ax2, eval(name + "_var_ref_model_1"), width=0.2,bottom=aggiornamento_1_ref, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2,alpha=0.3)
                    x_ax2=x_axis
                ax0.bar(x_ax1, eval(name + "_var_njord_model_1"), width=0.2, label=name.replace("_", " "),bottom=aggiornamento_1, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                ax0.bar(x_ax2, eval(name + "_var_njord_model_2"), width=0.2, bottom=aggiornamento_2,color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                ripartenza_1_ref = eval(name + "_var_ref_model_1")
                ripartenza_1 = eval(name + "_var_njord_model_1")
                ripartenza_2 = eval(name + "_var_njord_model_2")
                aggiornamento_1_ref = [x + y for x, y in zip(aggiornamento_1_ref, ripartenza_1_ref)]
                aggiornamento_1 = [x + y for x, y in zip(aggiornamento_1, ripartenza_1)]
                aggiornamento_2 = [x + y for x, y in zip(aggiornamento_2, ripartenza_2)]
                cont_col = cont_col + 1
                    # print(output_table_model1,"table!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(row_table)
            if referenza == 1:
                ax0.bar(2020, 0, width=0.2, label="References", color="blue",alpha=0.1)
            ax0.text(x_ax1[0], aggiornamento_1[0], round(aggiornamento_1[0], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[1], aggiornamento_1[1], round(aggiornamento_1[1], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[2], aggiornamento_1[2], round(aggiornamento_1[2], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[3], aggiornamento_1[3], round(aggiornamento_1[3], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[4], aggiornamento_1[4], round(aggiornamento_1[4], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[5], aggiornamento_1[5], round(aggiornamento_1[5], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[6], aggiornamento_1[6], round(aggiornamento_1[6], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[7], aggiornamento_1[7], round(aggiornamento_1[7], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[8], aggiornamento_1[8], round(aggiornamento_1[8], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[9], aggiornamento_1[9], round(aggiornamento_1[9], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[10], aggiornamento_1[10], round(aggiornamento_1[10], 2), verticalalignment='bottom',horizontalalignment='left')
            ax0.text(x_ax1[11], aggiornamento_1[11], round(aggiornamento_1[11], 2), verticalalignment='bottom',horizontalalignment='left')

            ax0.text(x_ax2[0], aggiornamento_2[0], round(aggiornamento_2[0], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[1], aggiornamento_2[1], round(aggiornamento_2[1], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[2], aggiornamento_2[2], round(aggiornamento_2[2], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[3], aggiornamento_2[3], round(aggiornamento_2[3], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[4], aggiornamento_2[4], round(aggiornamento_2[4], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[5], aggiornamento_2[5], round(aggiornamento_2[5], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[6], aggiornamento_2[6], round(aggiornamento_2[6], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[7], aggiornamento_2[7], round(aggiornamento_2[7], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[8], aggiornamento_2[8], round(aggiornamento_2[8], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[9], aggiornamento_2[9], round(aggiornamento_2[9], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[10], aggiornamento_2[10], round(aggiornamento_2[10], 2), verticalalignment='bottom',horizontalalignment='right')
            ax0.text(x_ax2[11], aggiornamento_2[11], round(aggiornamento_2[11], 2), verticalalignment='bottom',horizontalalignment='right')

            the_table_1 = ax1.table(cellText=output_table_model1.values, colLabels=year_2009_2020, rowLabels=row_table,
                                    loc="best")
            the_table_1.auto_set_column_width(col=list(range(len(output_table_model1.columns))))
            the_table_2 = ax2.table(cellText=output_table_model2.values, colLabels=year_2009_2020, rowLabels=row_table,
                                    loc="best")
            the_table_2.auto_set_column_width(col=list(range(len(output_table_model2.columns))))
            the_table_1.auto_set_font_size(False)
            the_table_1.set_fontsize(12)
            the_table_1.scale(1, 1.5)
            the_table_2.auto_set_font_size(False)
            the_table_2.set_fontsize(12)
            the_table_2.scale(1, 1.5)
            ax1.set_title("Result for model: "r"$\bf{" + model_1.replace("_"," ") + "}$ ", fontsize=20, )
            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis("off")
            ax2.set_title("Result for model: "r"$\bf{" + model_2.replace("_"," ") + "}$ ", fontsize=20, )
            ax2.xaxis.set_visible(False)
            ax2.yaxis.set_visible(False)
            ax2.axis("off")
            ax0.set_title("Predicted accumulated capacity [MW] for: " + r"$\bf{" + str(my_list_0.get(ANCHOR)) + "}$ ",           fontsize=15)
            ax0.set_xlabel("Year", fontsize=10)
            ax0.set_ylabel("Accumulated capacity [MW]", fontsize=10)
            ax0.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax0.set_xticks((np.arange(2009, 2021, 1.0)))
            plt.tight_layout()
            print("stampo")
            a = ScrollableWindow(fig)
            # plt.show()
            root.mainloop()
        else:
            posizione_testo = 0
            nation_order = []
            stacking = []
            stacking.append(0)
            aggiornamento_1 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            aggiornamento_2 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            if my_list_0.get(ANCHOR) == "Africa":
                dictionary = dict_africa
            if my_list_0.get(ANCHOR) == "Asia":
                dictionary = dict_asia
            if my_list_0.get(ANCHOR) == "Central America":
                dictionary = dict_central_america
            if my_list_0.get(ANCHOR) == "Eurasia":
                dictionary = dict_eurasia
            if my_list_0.get(ANCHOR) == "Europe":
                dictionary = dict_europe
            if my_list_0.get(ANCHOR) == "Middle East":
                dictionary = dict_middle_east
            if my_list_0.get(ANCHOR) == "North America":
                dictionary = dict_north_america
            if my_list_0.get(ANCHOR) == "Oceania":
                dictionary = dict_oceania
            if my_list_0.get(ANCHOR) == "Ref. country":
                dictionary = dict_ref_country
            if my_list_0.get(ANCHOR) == "South America":
                dictionary = dict_south_america
            fig, ax = plt.subplots(figsize=(20, 40))
            G = gridspec.GridSpec(3, 1)
            ax0 = plt.subplot(G[0, :])
            ax1 = plt.subplot(G[2, :])
            ax2 = plt.subplot(G[1, :])
            row_table = []
            variable_list_model_1=[]
            variable_list_model_2 = []
            aggiornamento_new_1 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            aggiornamento_1_ref = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            aggiornamento_1_ref_new = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            aggiornamento_new_2 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            for name, value in zip(dictionary, dictionary.values()):
                if cont_col == 10:
                    cont_col = 0
                #print(name,value.get())
                #print(dictionary[name])
                if value.get() == 0:
                    continue
                else:
                    print(name,"name")
                    row_table.append(name)
                    print(row_table,"row")
                    print(name)
                    name = name.replace(" ", "_")
                    print(name, "dopo")
                    nation_order.append(name)
                    exec("%s_var_ref_model_1 = []" % (name))
                    exec("%s_var_njord_model_1= []" % (name))
                    variable_list_model_1.append(name + "_var_njord_model_1")
                    exec("%s_var_ref_model_2 = []" % (name))
                    exec("%s_var_njord_model_2= []" % (name))
                    variable_list_model_2.append(name + "_var_njord_model_2")
                    # print(eval(name + "_var_njord"))
                    NJORD_model_1 = pd.read_excel(model_1 + "_model_results_year.xlsx", index_col=0)
                    NJORD_model_2 = pd.read_excel(model_2 + "_model_results_year.xlsx", index_col=0)
                    accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
                    accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
                    x_axis = []
                    x_axis_ref = []
                    valore_y_1=0
                    valore_y_2=0
                    source_list = []
                    valore_y_1 = float(accumulated_installed_2009[name.replace("_", " ")])
                    valore_y_2 = float(accumulated_installed_2009[name.replace("_", " ")])
                    print(valore_y_1)
                    (eval(name + "_var_njord_model_1")).append(valore_y_1)
                    (eval(name + "_var_njord_model_2")).append(valore_y_2)
                    x_axis.append(2009)
                    (eval(name + "_var_ref_model_1")).append(accumulated_reference_data["2009 - Total"][name.replace("_", " ")])
                    (eval(name + "_var_ref_model_2")).append(accumulated_reference_data["2009 - Total"][name.replace("_", " ")])
                    x_axis_ref.append(2009)
                    output_table_model1.at[name, "2009 NJ [MW]"] = accumulated_installed_2009[name.replace("_", " ")]
                    output_table_model2.at[name, "2009 NJ [MW]"] = accumulated_installed_2009[name.replace("_", " ")]
                    ref_table.at[name, "2009 Ref. [MW]"] = accumulated_installed_2009[name.replace("_", " ")]

                    for anno in range(2010, int(year) + 1):
                        valore_NJORD_1 = NJORD_model_1["NJORD " + str(anno)][name.replace("_", " ")]
                        valore_NJORD_2 = NJORD_model_2["NJORD " + str(anno)][name.replace("_", " ")]
                        valore_reference = accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")]

                        print(valore_reference, "valore", source_list)
                        if valore_NJORD_1 < 0:
                            valore_y_1 = float(valore_y_1)
                        else:
                            valore_y_1 = float(valore_y_1) + float(NJORD_model_1["NJORD " + str(anno)][name.replace("_", " ")])
                        if valore_NJORD_2 < 0:
                            valore_y_2 = float(valore_y_2)
                        else:
                            valore_y_2 = float(valore_y_2) + float(NJORD_model_2["NJORD " + str(anno)][name.replace("_", " ")])
                        output_table_model1.at[name, str(anno)+" NJ [MW]"] = round(valore_y_1, 2)
                        output_table_model2.at[name, str(anno)+" NJ [MW]"] = round(valore_y_2, 2)
                        #ref_table.at[name, str(anno)+" Ref. [MW]"]
                        (eval(name + "_var_njord_model_1")).append(valore_y_1)
                        (eval(name + "_var_ref_model_1")).append(valore_reference)
                        (eval(name + "_var_njord_model_2")).append(valore_y_2)
                        (eval(name + "_var_ref_model_2")).append(valore_reference)
                        x_axis.append(int(anno))
                        x_axis_ref.append((int(anno)))

            referenza = valore_comma.get()
            if referenza ==1:
                shifts = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
                print(x_axis)
                x_ax1 = np.add(x_axis, shifts)
                x_ax2 = np.subtract(x_axis, shifts)

            else:
                shifts = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12,0.12,0.12,0.12,0.12,0.12,0.12]
                print(x_axis)
                x_ax1=np.add(x_axis,shifts)
                x_ax2=np.subtract(x_axis,shifts)
                x_axis = x_ax2


            final_order_1 = {}
            final_order_2 = {}
            all_max = []

            for treno in variable_list_model_1:
                print(treno,"valore lista model 1")
                exec("%s_diff = []" % (treno))
                exec("%s_max = []" % (treno))
                for i in range(0, len(eval(treno)) - 1):
                    eval(treno + "_diff").append(eval(treno)[i + 1] - eval(treno)[i])  # -exec("eval(treno)[i]")
                eval(treno + "_max").append(max(eval(treno + "_diff")))
                print(eval(treno + "_max"), "massimi!!!!")
                final_order_1[treno] = max(eval(treno + "_diff"))
            final_order_1 = sorted(final_order_1.items(), key=operator.itemgetter(1), reverse=True)
            final_order_1_sorted = collections.OrderedDict(final_order_1)
            for treno in variable_list_model_2:
                exec("%s_diff = []" % (treno))
                exec("%s_max = []" % (treno))
                for i in range(0, len(eval(treno)) - 1):
                    eval(treno + "_diff").append(eval(treno)[i + 1] - eval(treno)[i])  # -exec("eval(treno)[i]")
                eval(treno + "_max").append(max(eval(treno + "_diff")))
                print(eval(treno + "_max"), "massimi!!!!")
                final_order_2[treno] = max(eval(treno + "_diff"))
            final_order_2 = sorted(final_order_2.items(), key=operator.itemgetter(1), reverse=True)
            final_order_2_sorted = collections.OrderedDict(final_order_2)
            print(final_order_1_sorted,"Primo")
            print(final_order_2_sorted,"Secondo")
            # print(max(diff),"massimo")
            cont_col = 0
            aggiornamento_new = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
            num_other = 0
            for key_1 in final_order_1_sorted.keys():
                if cont_col < 10:
                    print(key_1)
                    if referenza == 1:
                        ax0.bar(x_ax2, eval(key_1.replace("njord","ref")), width=0.2,bottom=aggiornamento_1_ref, color=list_color_bc[cont_col], edgecolor='black',linewidth=1.2,alpha=0.3)
                    ax0.bar(x_ax1, eval(key_1), width=0.2, label=key_1.replace("_var_njord_model_1", " "),bottom=aggiornamento_1, color=list_color_bc[cont_col], edgecolor='black',linewidth=1.2)
                    ax0.bar(x_axis, eval(key_1.replace("model_1","model_2")), width=0.2, bottom=aggiornamento_2, color=list_color_bc[cont_col], edgecolor='black',linewidth=1.2)
                    ripartenza_1 = eval(key_1)
                    aggiornamento_1 = [x + y for x, y in zip(aggiornamento_1, ripartenza_1)]
                    ripartenza_1_ref = eval(key_1.replace("njord","ref"))
                    aggiornamento_1_ref = [x + y for x, y in zip(aggiornamento_1_ref, ripartenza_1_ref)]
                    ripartenza_2 = eval(key_1.replace("model_1","model_2"))
                    aggiornamento_2 = [x + y for x, y in zip(aggiornamento_2, ripartenza_2)]
                    cont_col = cont_col + 1
                else:
                    print(key_1)
                    ripartenza_1 = eval(key_1)
                    aggiornamento_new_1 = [x + y for x, y in zip(aggiornamento_new_1, ripartenza_1)]
                    ripartenza_1_ref = eval(key_1.replace("njord","ref"))
                    aggiornamento_1_ref_new = [x + y for x, y in zip(aggiornamento_1_ref_new, ripartenza_1_ref)]
                    ripartenza_2 = eval(key_1.replace("model_1","model_2"))
                    aggiornamento_new_2 = [x + y for x, y in zip(aggiornamento_new_2, ripartenza_2)]
                    num_other = num_other + 1

            if cont_col >=10:
                color_1="gray"
                alpha_1=0.8
                color_2="black"
                alpha_2=1
            else:
                color_1="black"
                alpha_1=1
                color_2="black"
                alpha_2=1


            if cont_col >= 10:
                ax0.bar(x_ax1, aggiornamento_new_1, width=0.2, bottom=aggiornamento_1,color=list_color_bc[10], edgecolor='black', linewidth=1.2)
                ax0.bar(x_axis, aggiornamento_new_2, width=0.2, label="Other "+str(num_other)+" nations", bottom=aggiornamento_2,color=list_color_bc[10], edgecolor='black', linewidth=1.2)
                if referenza == 1:
                    ax0.bar(x_ax2,aggiornamento_1_ref_new, width=0.2,color=list_color_bc[10],bottom=aggiornamento_1_ref,edgecolor='black',linewidth=1.2,alpha=0.3)


            if cont_col >= 10:
                ax0.text(x_ax1[0], aggiornamento_1[0]+aggiornamento_new_1[0], round(aggiornamento_1[0]+aggiornamento_new_1[0], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[1], aggiornamento_1[1]+aggiornamento_new_1[1], round(aggiornamento_1[1]+aggiornamento_new_1[1], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[2], aggiornamento_1[2]+aggiornamento_new_1[2], round(aggiornamento_1[2]+aggiornamento_new_1[2], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[3], aggiornamento_1[3]+aggiornamento_new_1[3], round(aggiornamento_1[3]+aggiornamento_new_1[3], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[4], aggiornamento_1[4]+aggiornamento_new_1[4], round(aggiornamento_1[4]+aggiornamento_new_1[4], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[5], aggiornamento_1[5]+aggiornamento_new_1[5], round(aggiornamento_1[5]+aggiornamento_new_1[5], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[6], aggiornamento_1[6]+aggiornamento_new_1[6], round(aggiornamento_1[6]+aggiornamento_new_1[6], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[7], aggiornamento_1[7]+aggiornamento_new_1[7], round(aggiornamento_1[7]+aggiornamento_new_1[7], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[8], aggiornamento_1[8]+aggiornamento_new_1[8], round(aggiornamento_1[8]+aggiornamento_new_1[8], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[9], aggiornamento_1[9]+aggiornamento_new_1[9], round(aggiornamento_1[9]+aggiornamento_new_1[9], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[10], aggiornamento_1[10]+aggiornamento_new_1[10], round(aggiornamento_1[10]+aggiornamento_new_1[10], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_ax1[11], aggiornamento_1[11]+aggiornamento_new_1[11], round(aggiornamento_1[11]+aggiornamento_new_1[11], 2), verticalalignment='bottom',
                         horizontalalignment='left',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[0], aggiornamento_2[0]+aggiornamento_new_2[0], round(aggiornamento_2[0]+aggiornamento_new_2[0], 2), verticalalignment='bottom',
                         horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[1], aggiornamento_2[1]+aggiornamento_new_2[1], round(aggiornamento_2[1]+aggiornamento_new_2[1], 2), verticalalignment='bottom',
                         horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[2], aggiornamento_2[2]+aggiornamento_new_2[2], round(aggiornamento_2[2]+aggiornamento_new_2[2], 2), verticalalignment='bottom',
                         horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[3], aggiornamento_2[3]+aggiornamento_new_2[3], round(aggiornamento_2[3]+aggiornamento_new_2[3], 2), verticalalignment='bottom',
                         horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[4], aggiornamento_2[4]+aggiornamento_new_2[4], round(aggiornamento_2[4]+aggiornamento_new_2[4], 2), verticalalignment='bottom',
                         horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[5], aggiornamento_2[5]+aggiornamento_new_2[5], round(aggiornamento_2[5]+aggiornamento_new_2[5], 2), verticalalignment='bottom',
                         horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[6], aggiornamento_2[6]+aggiornamento_new_2[6], round(aggiornamento_2[6]+aggiornamento_new_2[6], 2), verticalalignment='bottom',horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[7], aggiornamento_2[7]+aggiornamento_new_2[7], round(aggiornamento_2[7]+aggiornamento_new_2[7], 2), verticalalignment='bottom',horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[8], aggiornamento_2[8]+aggiornamento_new_2[8], round(aggiornamento_2[8]+aggiornamento_new_2[8], 2), verticalalignment='bottom',horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[9], aggiornamento_2[9]+aggiornamento_new_2[9], round(aggiornamento_2[9]+aggiornamento_new_2[9], 2), verticalalignment='bottom',horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[10], aggiornamento_2[10]+aggiornamento_new_2[10], round(aggiornamento_2[10]+aggiornamento_new_2[10], 2), verticalalignment='bottom',horizontalalignment='right',color=color_2,alpha=alpha_2)
                ax0.text(x_axis[11], aggiornamento_2[11]+aggiornamento_new_2[11], round(aggiornamento_2[11]+aggiornamento_new_2[11], 2), verticalalignment='bottom',horizontalalignment='right',color=color_2,alpha=alpha_2)

                if referenza == 1:
                    ax0.bar(2020, 0, width=0.2, label="References", color="blue",alpha=0.1)

            ax0.text(x_ax1[0], aggiornamento_1[0], round(aggiornamento_1[0], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[1], aggiornamento_1[1], round(aggiornamento_1[1], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[2], aggiornamento_1[2], round(aggiornamento_1[2], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[3], aggiornamento_1[3], round(aggiornamento_1[3], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[4], aggiornamento_1[4], round(aggiornamento_1[4], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[5], aggiornamento_1[5], round(aggiornamento_1[5], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[6], aggiornamento_1[6], round(aggiornamento_1[6], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[7], aggiornamento_1[7], round(aggiornamento_1[7], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[8], aggiornamento_1[8], round(aggiornamento_1[8], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[9], aggiornamento_1[9], round(aggiornamento_1[9], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[10], aggiornamento_1[10], round(aggiornamento_1[10], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)
            ax0.text(x_ax1[11], aggiornamento_1[11], round(aggiornamento_1[11], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_1,alpha=alpha_1)

            ax0.text(x_axis[0], aggiornamento_2[0], round(aggiornamento_2[0], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[1], aggiornamento_2[1], round(aggiornamento_2[1], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[2], aggiornamento_2[2], round(aggiornamento_2[2], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[3], aggiornamento_2[3], round(aggiornamento_2[3], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[4], aggiornamento_2[4], round(aggiornamento_2[4], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[5], aggiornamento_2[5], round(aggiornamento_2[5], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[6], aggiornamento_2[6], round(aggiornamento_2[6], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[7], aggiornamento_2[7], round(aggiornamento_2[7], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[8], aggiornamento_2[8], round(aggiornamento_2[8], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[9], aggiornamento_2[9], round(aggiornamento_2[9], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[10], aggiornamento_2[10], round(aggiornamento_2[10], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)
            ax0.text(x_axis[11], aggiornamento_2[11], round(aggiornamento_2[11], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_1,alpha=alpha_1)

            the_table_1 = ax1.table(cellText=output_table_model1.values, colLabels=labels_NJORD,rowLabels=row_table,loc="best")
            the_table_1.auto_set_column_width(col=list(range(len(output_table_model1.columns))))
            the_table_2 = ax2.table(cellText=output_table_model2.values, colLabels=labels_NJORD,rowLabels=row_table,loc="best")
            the_table_2.auto_set_column_width(col=list(range(len(output_table_model2.columns))))
            the_table_1.auto_set_font_size(False)
            the_table_1.set_fontsize(10)
            the_table_1.scale(1,1.5)
            the_table_2.auto_set_font_size(False)
            the_table_2.set_fontsize(10)
            the_table_2.scale(1,1.5)
            ax1.set_title("Result for model: "r"$\bf{" + model_1.replace("_"," ") + "}$ ", fontsize=20, )
            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis("off")
            ax2.set_title("Result for model: "r"$\bf{" + model_2.replace("_"," ") + "}$ ", fontsize=20, )
            ax2.xaxis.set_visible(False)
            ax2.yaxis.set_visible(False)
            ax2.axis("off")
            ax0.set_title("Predicted accumulated capacity [MW] for: " + r"$\bf{" + str(my_list_0.get(ANCHOR)) + "}$ ",fontsize=15)
            ax0.set_xlabel("Year", fontsize=15)
            ax0.set_ylabel("Accumulated capacity [MW]", fontsize=15)
            ax0.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax0.set_xticks((np.arange(2009, 2021, 1.0)))
            plt.tight_layout()
            print("stampo")
            a = ScrollableWindow(fig)
            #plt.show()
            root.mainloop()
    else:

        NJORD_model_1 = pd.read_excel(model_1 + "_model_results.xlsx", index_col=0)
        NJORD_model_2 = pd.read_excel(model_2 + "_model_results.xlsx", index_col=0)
        accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
        accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
        x_axis = []
        y_axis_model_1 = []
        y_axis_model_2 = []
        y_axis_ref = []
        x_axis_ref = []
        ref_irena = []
        ref_pvps = []
        ref_other = []
        source_list = []
        valore_y_1 = float(accumulated_installed_2009[name])
        valore_y_2 = float(accumulated_installed_2009[name])
        print(valore_y_1)
        y_axis_model_1.append(valore_y_1)
        y_axis_model_2.append(valore_y_2)
        x_axis.append(2009.75)
        y_axis_ref.append(accumulated_reference_data["2009 - Total"][name])
        x_axis_ref.append(2009.75)
        output_table_model1.at["2009", "NJORD [MW]"] = "-"
        output_table_model1.at["2009", "Ref. value"] = accumulated_reference_data["2009 - Total"][name]
        output_table_model2.at["2009", "NJORD [MW]"] = "-"
        output_table_model2.at["2009", "Ref. value"] = accumulated_reference_data["2009 - Total"][name]
        ref_table_irena.at[ "2009", " Irena [MW]"] = accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")]

        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "q":
            ref_table_irena.at["2009", " Irena source"] = "Questionnaire"
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "o":
            ref_table_irena.at["2009", " Irena source"] = "Official"
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "u":
            ref_table_irena.at["2009", " Irena source"] = "Unofficial"
        if accumulated_reference_data["2009 - IRENA s"][name.replace("_", " ")] == "e":
            ref_table_irena.at["2009", " Irena source"] = "Estimates"

        ref_table_other.at["2009", " Other [MW]"] = accumulated_reference_data["2009 - Other"][name.replace("_", " ")]
        ref_table_pvps.at["2009", " PVPS [MW]"] = accumulated_reference_data["2009 - PVPS"][name.replace("_", " ")]
        source_0 = (NJORD_model_1["Source 2009"][name])
        ref_irena.append(accumulated_reference_data["2009 - IRENA"][name.replace("_", " ")])
        ref_pvps.append(accumulated_reference_data["2009 - PVPS"][name.replace("_", " ")])
        ref_other.append(accumulated_reference_data["2009 - Other"][name.replace("_", " ")])
        if source_0 == "Irena":
            lettera = "Irena"
        if source_0 == "No Ref":
            lettera = "No ref"
        if source_0 == "Other":
            lettera = "Other"
        if source_0 == "PVPS":
            lettera = "PVPS"
        source_list.append("SP")
        output_table_model1.at["2009", "Ref. Source"] = lettera
        output_table_model2.at["2009", "Ref. Source"] = lettera
        x_value=2009.75
        for anno in desiderio:
            only_anno = anno.split("-")
            only_anno = only_anno[0]
            valore_NJORD_model_1 = NJORD_model_1["NJORD " + str(anno)][name]
            valore_NJORD_model_2 = NJORD_model_2["NJORD " + str(anno)][name]
            valore_reference = accumulated_reference_data[str(only_anno) + " - Total"][name]
            source = NJORD_model_1["Source " + str(only_anno)][name]
            if source == "Irena":
                lettera = "Irena"
            if source == "No Ref":
                lettera = "No ref"
            if source == "Other":
                lettera = "Other"
            if source == "PVPS":
                lettera = "PVPS"
            source_list.append(lettera)
            output_table_model1.at[anno, "Ref. Source"] = lettera
            output_table_model2.at[anno, "Ref. Source"] = lettera
            output_table_model1.at[anno, "Ref. value"] = valore_reference
            output_table_model2.at[anno, "Ref. value"] = valore_reference
            ref_table_irena.at[anno, " Irena [MW]"] = accumulated_reference_data[str(only_anno) + " - IRENA"][
                name.replace("_", " ")]
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "q":
                ref_table_irena.at[anno, " Irena source"] = "Questionnaire"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "o":
                ref_table_irena.at[anno, " Irena source"] = "Official"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "u":
                ref_table_irena.at[anno, " Irena source"] = "Unofficial"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name.replace("_", " ")] == "e":
                ref_table_irena.at[anno, " Irena source"] = "Estimates"
            ref_table_other.at[anno, " Other [MW]"] = accumulated_reference_data[str(only_anno) + " - Other"][
                name.replace("_", " ")]
            ref_table_pvps.at[anno, " PVPS [MW]"] = accumulated_reference_data[str(only_anno) + " - PVPS"][
                name.replace("_", " ")]
            print(valore_reference, "valore", source_list)
            if valore_NJORD_model_1 < 0:
                valore_y_1 = float(valore_y_1)
            else:
                valore_y_1 = float(valore_y_1) + float(NJORD_model_1["NJORD " + str(anno)][name])
            if valore_NJORD_model_2 < 0:
                valore_y_2 = float(valore_y_2)
            else:
                valore_y_2 = float(valore_y_2) + float(NJORD_model_2["NJORD " + str(anno)][name])
            output_table_model1.at[anno, "NJORD [MW]"] = round(valore_y_1,2)
            output_table_model2.at[anno, "NJORD [MW]"] = round(valore_y_2,2)
            ref_irena.append(accumulated_reference_data[str(only_anno) + " - IRENA"][name.replace("_", " ")])
            ref_pvps.append(accumulated_reference_data[str(only_anno) + " - PVPS"][name.replace("_", " ")])
            ref_other.append(accumulated_reference_data[str(only_anno) + " - Other"][name.replace("_", " ")])
            #ref_im.append(accumulated_reference_data[str(anno) + " - Total"][name.replace("_", " ")])
            y_axis_model_1.append(valore_y_1)
            y_axis_model_2.append(valore_y_2)
            y_axis_ref.append(valore_reference)
            x_value=x_value+0.25
            x_axis.append(x_value)
            if only_anno == "2009":
                x_axis_ref.append(2009.75)
                continue
            else:
                x_axis_ref.append((int(only_anno)+1))

        fig, ax = plt.subplots(figsize=(18,30))
        G = gridspec.GridSpec(3, 2)
        ax0 = plt.subplot(G[0, :])
        ax1 = plt.subplot(G[1:2, 0])
        ax2 = plt.subplot(G[1:2, 1])
        xlabell = "References source for each year: "
        for i in range(1, len(x_axis)):
            xlabell = str(xlabell) + r"$\bf{" + str(source_list[i]) + ",   " + "}$"

        # ax.set(xlabel=str(xlabell),ylabel="Accumulated capacity [MW]",fontsize=10)
        ax0.set_xlabel("Year", fontsize=14)
        ax0.set_ylabel("Accumulated capacity [MW]", fontsize=14)
        # ax.set(xlabel="Year \nReferences:"+str(x_axis[0])+":"+str(source_list[0])+", "+str(x_axis[1])+":"+str(source_list[1])+", "+str(x_axis[2])+":"+str(source_list[2])+", "+str(x_axis[3])+":"+str(source_list[3])+", "+str(x_axis[4])+":"+str(source_list[4])+", "+str(x_axis[5])+":"+str(source_list[5])+", "+str(x_axis[6])+":"+str(source_list[6]),ylabel="Accumulated capacity [MW]",title="Accumulated installed capacity for "+r"$\bf{" + name + "}$"+"\n NJORD value: "+str(round(valore_y,2))+"MW and reference value: "+ str(round(valore_reference,2))+"MW\n")
        #plt.title("\n \n NJORD 1: " + str(round(valore_y_1, 2)) + "MW,NJORD 2: " + str(round(valore_y_2, 2)) + "MW  Total reference value: " + str(round(valore_reference, 2)) + "MW\n", fontsize=14)
        ax0.set_title("" + "Accumulated installed capacity for " + r"$\bf{" + name + "}$ ", fontsize=19)
        ax0.plot(x_axis, y_axis_model_1, marker="o", label=model_1,color="#C30017" )
        ax0.plot(x_axis, y_axis_model_2, marker="o", label=model_2 ,color="#FFA626")
        referenza = valore_comma.get()
        referenza_irena = valore_comma_irena.get()  # option in the GUI to plot or not reference data
        referenza_other = valore_comma_other.get()  # option in the GUI to plot or not reference data
        referenza_pvps = valore_comma_pvps.get()
        if referenza_pvps==1:
            ax0.plot(x_axis_ref, ref_pvps, marker="<",linestyle='--', label="PVPS ref", alpha=0.3)
            output_table_model1 = output_table_model1.join(ref_table_pvps)
            output_table_model2 = output_table_model2.join(ref_table_pvps)
        if referenza_irena==1:
            ax0.plot(x_axis_ref, ref_irena, marker="^",linestyle='-.', label="Ref Irena", alpha=0.3)
            output_table_model1 = output_table_model1.join(ref_table_irena)
            output_table_model2 = output_table_model2.join(ref_table_irena)
        if referenza_other==1:
            ax0.plot(x_axis_ref, ref_other, marker="*",linestyle='--', label="Ref Other", alpha=0.3)
            output_table_model1 = output_table_model1.join(ref_table_other)
            output_table_model2 = output_table_model2.join(ref_table_other)
        if referenza == 0:
            print("no ref")
        else:
            ax0.plot(x_axis_ref, y_axis_ref, marker="+", label="Reference", alpha=0.3,color="#FF1926")
        # ax.text(min(x_axis), max(y_axis), 'boxed italics text in data coords', style='italic',bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        ax0.legend()
        #ax0.set_xticks(range(min(x_axis), max(x_axis) + 1))
        the_table_1 = ax1.table(cellText=output_table_model1.values, rowLabels=desiderio_lab, colLabels=output_table_model1.columns, loc="best")
        the_table_1.auto_set_column_width(col=list(range(len(output_table_model1.columns))))
        the_table_2 = ax2.table(cellText=output_table_model2.values, rowLabels=desiderio_lab, colLabels=output_table_model2.columns,loc="best")
        the_table_2.auto_set_column_width(col=list(range(len(output_table_model2.columns))))
        ax1.set_title("Result for model: "r"$\bf{" + model_1.replace("_",".") + "}$ ", fontsize=18)
        ax1.xaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
        ax1.axis("off")
        ax2.set_title("Result for model: "r"$\bf{" + model_2.replace("_",".") + "}$ ", fontsize=18)
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.axis("off")
        the_table_1.set_fontsize(10)
        the_table_1.scale(1, 1.5)
        the_table_2.set_fontsize(10)
        the_table_2.scale(1, 1.5)
        ax0.set_xticks((np.arange(2009, 2022, 1.0)))
        a = ScrollableWindow(fig)
        plt.tight_layout()
        #plt.text(0.18, 0.01, xlabell, fontsize=10, transform=plt.gcf().transFigure)
        #plt.show()
        root.mainloop()
        plt.close()

def two_states_comparison(name_1,name_2,year,model):
    cont_col = 0
    output_table_name1 = pd.DataFrame()
    output_table_name2 = pd.DataFrame()
    legend_1=[]
    legend_2=[]
    variable_list_name_1=[]
    variable_list_name_2 = []
    ref_table_irena_1 = pd.DataFrame()
    ref_table_other_1 = pd.DataFrame()
    ref_table_pvps_1 = pd.DataFrame()
    ref_table_irena_2 = pd.DataFrame()
    ref_table_other_2 = pd.DataFrame()
    ref_table_pvps_2 = pd.DataFrame()
    if my_entry_0.get() != "":
        posizione_testo = 0
        nation_order = []
        stacking = []
        stacking.append(0)
        aggiornamento_1 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        aggiornamento_2 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        aggiornamento_new_1 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        aggiornamento_new_2 = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]

        if my_list_0.get(ANCHOR) == "Africa":
            dictionary = dict_africa
        if my_list_0.get(ANCHOR) == "Asia":
            dictionary = dict_asia
        if my_list_0.get(ANCHOR) == "Central America":
            dictionary = dict_central_america
        if my_list_0.get(ANCHOR) == "Eurasia":
            dictionary = dict_eurasia
        if my_list_0.get(ANCHOR) == "Europe":
            dictionary = dict_europe
        if my_list_0.get(ANCHOR) == "Middle East":
            dictionary = dict_middle_east
        if my_list_0.get(ANCHOR) == "North America":
            dictionary = dict_north_america
        if my_list_0.get(ANCHOR) == "Oceania":
            dictionary = dict_oceania
        if my_list_0.get(ANCHOR) == "Ref. country":
            dictionary = dict_ref_country
        if my_list_0.get(ANCHOR) == "South America":
            dictionary = dict_south_america
        fig, ax = plt.subplots(figsize=(20, 40))
        G = gridspec.GridSpec(3, 1)
        ax0 = plt.subplot(G[0, :])
        ax1 = plt.subplot(G[1, :])
        ax2 = plt.subplot(G[2, :])
        row_1=[]
        row_2=[]
        for name_1, value in zip(dictionary, dictionary.values()):
            if cont_col == 10:
                cont_col = 0
            # print(name,value.get())
            # print(dict_asia[name])
            if value.get() == 0:
                continue
            else:
                row_1.append(name_1)

                print(name_1)
                name_1 = name_1.replace(" ", "_")
                print(name_1, "dopo")
                nation_order.append(name_1)
                exec("%s_var_ref = []" % (name_1))
                exec("%s_var_njord = []" % (name_1))
                variable_list_name_1.append(name_1 + "_var_njord")

                # print(eval(name + "_var_njord"))
                NJORD = pd.read_excel(model + "_model_results_year.xlsx", index_col=0)
                accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
                accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
                x_axis = []
                x_axis_ref = []
                source_list = []
                valore_y_1 = 0
                valore_y_1 = float(accumulated_installed_2009[name_1.replace("_", " ")])
                print(valore_y_1)
                (eval(name_1 + "_var_njord")).append(valore_y_1)
                x_axis.append(2009)
                (eval(name_1 + "_var_ref")).append(accumulated_reference_data["2009 - Total"][name_1.replace("_", " ")])
                x_axis_ref.append(2009)
                output_table_name1.at[name_1, "2009"] = accumulated_reference_data["2009 - Total"][name_1.replace("_", " ")]

                for anno in range(2010, int(year) + 1):
                    valore_NJORD_1 = NJORD["NJORD " + str(anno)][name_1.replace("_", " ")]
                    valore_reference_1 = accumulated_reference_data[str(anno) + " - Total"][name_1.replace("_", " ")]

                    print(valore_reference_1, "valore", source_list)
                    if valore_NJORD_1 < 0:
                        valore_y_1 = float(valore_y_1)
                    else:
                        valore_y_1 = float(valore_y_1) + float(NJORD["NJORD " + str(anno)][name_1.replace("_", " ")])
                    (eval(name_1 + "_var_njord")).append(valore_y_1)
                    (eval(name_1 + "_var_ref")).append(valore_reference_1)
                    x_axis.append(int(anno))
                    x_axis_ref.append((int(anno)))
                    output_table_name1.at[name_1, anno] = round(valore_y_1,2)
                shifts = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
                print(x_axis)
                x_ax1 = np.add(x_axis, shifts)
                x_ax2 = np.subtract(x_axis, shifts)

        if my_list_7.get(ANCHOR) == "Africa":
            dictionary = dict_africa
        if my_list_7.get(ANCHOR) == "Asia":
            dictionary = dict_asia
        if my_list_7.get(ANCHOR) == "Central America":
            dictionary = dict_central_america
        if my_list_7.get(ANCHOR) == "Eurasia":
            dictionary = dict_eurasia
        if my_list_7.get(ANCHOR) == "Europe":
            dictionary = dict_europe
        if my_list_7.get(ANCHOR) == "Middle East":
            dictionary = dict_middle_east
        if my_list_7.get(ANCHOR) == "North America":
            dictionary = dict_north_america
        if my_list_7.get(ANCHOR) == "Oceania":
            dictionary = dict_oceania
        if my_list_7.get(ANCHOR) == "Ref. country":
            dictionary = dict_ref_country
        if my_list_7.get(ANCHOR) == "South America":
            dictionary = dict_south_america
        cont_col =0
        value=0
        for name_2, value in zip(dictionary, dictionary.values()):
            # print(name,value.get())
            # print(dict_asia[name])
            if value.get() == 0:
                continue
            else:
                if cont_col == 10:
                    cont_col = 0
                row_2.append(name_2)
                print(name_2)

                name_2 = name_2.replace(" ", "_")
                print(name_2, "dopo")
                nation_order.append(name_2)
                exec("%s_var_ref = []" % (name_2))
                exec("%s_var_njord = []" % (name_2))
                variable_list_name_2.append(name_2 + "_var_njord")
                # print(eval(name + "_var_njord"))
                NJORD = pd.read_excel(model + "_model_results_year.xlsx", index_col=0)
                accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
                accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
                x_axis = []
                x_axis_ref = []
                source_list = []
                valore_y_2 = 0
                valore_y_2 = float(accumulated_installed_2009[name_2.replace("_", " ")])
                print(valore_y_2)
                (eval(name_2 + "_var_njord")).append(valore_y_2)
                x_axis.append(2009)
                (eval(name_2 + "_var_ref")).append(accumulated_reference_data["2009 - Total"][name_2.replace("_", " ")])
                x_axis_ref.append(2009)
                output_table_name2.at[name_2, "2009"] =accumulated_reference_data["2009 - Total"][name_2.replace("_", " ")]
                source_0 = (NJORD["Source 2009"][name_2.replace("_", " ")])
                if source_0 == "Irena":
                    lettera = "Irena"
                if source_0 == "No Ref":
                    lettera = "No ref"
                if source_0 == "Other":
                    lettera = "Other"
                if source_0 == "PVPS":
                    lettera = "PVPS"
                if name_2 in regions:
                    lettera = "regions"
                source_list.append("SP")
                for anno in range(2010, int(year) + 1):
                    valore_NJORD_2 = NJORD["NJORD " + str(anno)][name_2.replace("_", " ")]
                    valore_reference_2 = accumulated_reference_data[str(anno) + " - Total"][name_2.replace("_", " ")]
                    source = NJORD["Source " + str(anno)][name_2.replace("_", " ")]
                    if source == "Irena":
                        lettera = "Irena"
                    if source == "No Ref":
                        lettera = "No ref"
                    if source == "Other":
                        lettera = "Other"
                    if source == "PVPS":
                        lettera = "PVPS"
                    source_list.append(lettera)
                    print(valore_reference_2, "valore", source_list)
                    if valore_NJORD_2 < 0:
                        valore_y_2 = float(valore_y_2)
                    else:
                        valore_y_2 = float(valore_y_2) + float(NJORD["NJORD " + str(anno)][name_2.replace("_", " ")])
                    (eval(name_2 + "_var_njord")).append(valore_y_2)
                    (eval(name_2 + "_var_ref")).append(valore_reference_2)
                    x_axis.append(int(anno))
                    x_axis_ref.append((int(anno)))
                    output_table_name2.at[name_2, anno] = round(valore_y_2,2)

        final_order_1 = {}
        final_order_2 = {}
        all_max = []
        print(variable_list_name_1)
        print(variable_list_name_2)
        for treno in variable_list_name_1:
            print(treno, "valore lista model 1")
            exec("%s_diff = []" % (treno))
            exec("%s_max = []" % (treno))
            for i in range(0, len(eval(treno)) - 1):
                eval(treno + "_diff").append(eval(treno)[i + 1] - eval(treno)[i])  # -exec("eval(treno)[i]")
            eval(treno + "_max").append(max(eval(treno + "_diff")))
            print(eval(treno + "_max"), "massimi!!!!")
            final_order_1[treno] = max(eval(treno + "_diff"))
        final_order_1 = sorted(final_order_1.items(), key=operator.itemgetter(1), reverse=True)
        final_order_1_sorted = collections.OrderedDict(final_order_1)
        for treno in variable_list_name_2:
            exec("%s_diff = []" % (treno))
            exec("%s_max = []" % (treno))
            for i in range(0, len(eval(treno)) - 1):
                eval(treno + "_diff").append(eval(treno)[i + 1] - eval(treno)[i])  # -exec("eval(treno)[i]")
            eval(treno + "_max").append(max(eval(treno + "_diff")))
            print(eval(treno + "_max"), "massimi!!!!")
            final_order_2[treno] = max(eval(treno + "_diff"))
        final_order_2 = sorted(final_order_2.items(), key=operator.itemgetter(1), reverse=True)
        final_order_2_sorted = collections.OrderedDict(final_order_2)
        print(final_order_1_sorted, "Primo")
        print(final_order_2_sorted, "Secondo")
        # print(max(diff),"massimo")
        cont_col = 0
        aggiornamento_new = [0, 0, 0, 0, 0, 0, 0,0,0,0,0,0]
        num_other = 0
        num_other_2 = 0
        ax0.bar(2020, 0, label="Nations for dx:")
        for key_1 in final_order_1_sorted.keys():
            if cont_col < 10:
                print(key_1)
                ax0.bar(x_ax1, eval(key_1), width=0.2, label=key_1.replace("_var_njord", " "),bottom=aggiornamento_1, color=list_color_bc[cont_col], edgecolor='black', linewidth=1.2)
                ripartenza_1 = eval(key_1)
                aggiornamento_1 = [x + y for x, y in zip(aggiornamento_1, ripartenza_1)]
                cont_col = cont_col + 1
            else:
                print(key_1)
                ripartenza_1 = eval(key_1)
                aggiornamento_new_1 = [x + y for x, y in zip(aggiornamento_new_1, ripartenza_1)]
                num_other = num_other + 1
        ax0.bar(2019,0,label="Nations for sx:")
        cont_col_2=0
        num_other_2=0
        for key_2 in final_order_2_sorted.keys():
            if cont_col_2 < 10:
                print(key_2)
                ax0.bar(x_ax2, eval(key_2), width=0.2, label=key_2.replace("_var_njord", " "), bottom=aggiornamento_2,color=list_color_bc[cont_col_2], edgecolor='black', linewidth=1.2)
                ripartenza_2 = eval(key_2)
                aggiornamento_2 = [x + y for x, y in zip(aggiornamento_2, ripartenza_2)]
                cont_col_2 = cont_col_2 + 1
            else:
                print(key_2)
                ripartenza_2 = eval(key_2.replace("name_1", "name_2"))
                aggiornamento_new_2 = [x + y for x, y in zip(aggiornamento_new_2, ripartenza_2)]
                num_other_2 = num_other_2 + 1
        if cont_col >= 10:
            ax0.bar(x_ax1, aggiornamento_new_1, width=0.2,label="Other " + str(num_other) + " nations for dx", bottom=aggiornamento_1, color=list_color_bc[10],edgecolor='black', linewidth=1.2)

        if cont_col_2 >= 10:
            ax0.bar(x_ax2, aggiornamento_new_2, width=0.2, label="Other " + str(num_other_2) + " nations for sx",bottom=aggiornamento_2, color=list_color_bc[10], edgecolor='black', linewidth=1.2)

        if cont_col >= 10:
            color_11 = "gray"
            alpha_11 = 0.8
            color_21 = "black"
            alpha_21 = 1
        else:
            color_11 = "black"
            alpha_11 = 1
            color_21 = "black"
            alpha_21 = 1

        if cont_col_2 >= 10:
            color_12 = "gray"
            alpha_12 = 0.8
            color_22 = "black"
            alpha_22 = 1
        else:
            color_12 = "black"
            alpha_12 = 1
            color_22 = "black"
            alpha_22 = 1

        if cont_col >= 10:
            ax0.text(x_ax1[0], aggiornamento_1[0] + aggiornamento_new_1[0],
                     round(aggiornamento_1[0] + aggiornamento_new_1[0], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[1], aggiornamento_1[1] + aggiornamento_new_1[1],
                     round(aggiornamento_1[1] + aggiornamento_new_1[1], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[2], aggiornamento_1[2] + aggiornamento_new_1[2],
                     round(aggiornamento_1[2] + aggiornamento_new_1[2], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[3], aggiornamento_1[3] + aggiornamento_new_1[3],
                     round(aggiornamento_1[3] + aggiornamento_new_1[3], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[4], aggiornamento_1[4] + aggiornamento_new_1[4],
                     round(aggiornamento_1[4] + aggiornamento_new_1[4], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[5], aggiornamento_1[5] + aggiornamento_new_1[5],
                     round(aggiornamento_1[5] + aggiornamento_new_1[5], 2), verticalalignment='bottom',
                     horizontalalignment='left',color=color_21,alpha=alpha_21)

            ax0.text(x_ax1[6], aggiornamento_1[6] + aggiornamento_new_1[6],round(aggiornamento_1[6] + aggiornamento_new_1[6], 2), verticalalignment='bottom',horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[7], aggiornamento_1[7] + aggiornamento_new_1[7],round(aggiornamento_1[7] + aggiornamento_new_1[7], 2), verticalalignment='bottom',horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[8], aggiornamento_1[8] + aggiornamento_new_1[8],round(aggiornamento_1[8] + aggiornamento_new_1[8], 2), verticalalignment='bottom',horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[9], aggiornamento_1[9] + aggiornamento_new_1[9],round(aggiornamento_1[9] + aggiornamento_new_1[9], 2), verticalalignment='bottom',horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[10], aggiornamento_1[10] + aggiornamento_new_1[10],round(aggiornamento_1[10] + aggiornamento_new_1[10], 2), verticalalignment='bottom',horizontalalignment='left',color=color_21,alpha=alpha_21)
            ax0.text(x_ax1[11], aggiornamento_1[11] + aggiornamento_new_1[11],round(aggiornamento_1[11] + aggiornamento_new_1[11], 2), verticalalignment='bottom',horizontalalignment='left',color=color_21,alpha=alpha_21)

        if cont_col_2 >= 10:
            ax0.text(x_ax2[0], aggiornamento_2[0] + aggiornamento_new_2[0],
                     round(aggiornamento_2[0] + aggiornamento_new_2[0], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[1], aggiornamento_2[1] + aggiornamento_new_2[1],
                     round(aggiornamento_2[1] + aggiornamento_new_2[1], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[2], aggiornamento_2[2] + aggiornamento_new_2[2],
                     round(aggiornamento_2[2] + aggiornamento_new_2[2], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[3], aggiornamento_2[3] + aggiornamento_new_2[3],
                     round(aggiornamento_2[3] + aggiornamento_new_2[3], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[4], aggiornamento_2[4] + aggiornamento_new_2[4],
                     round(aggiornamento_2[4] + aggiornamento_new_2[0], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[5], aggiornamento_2[5] + aggiornamento_new_2[5],
                     round(aggiornamento_2[5] + aggiornamento_new_2[5], 2), verticalalignment='bottom',
                     horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[6], aggiornamento_2[6] + aggiornamento_new_2[6],round(aggiornamento_2[6] + aggiornamento_new_2[6], 2), verticalalignment='bottom',horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[7], aggiornamento_2[7] + aggiornamento_new_2[7],round(aggiornamento_2[7] + aggiornamento_new_2[7], 2), verticalalignment='bottom',horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[8], aggiornamento_2[8] + aggiornamento_new_2[8],round(aggiornamento_2[8] + aggiornamento_new_2[8], 2), verticalalignment='bottom',horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[9], aggiornamento_2[9] + aggiornamento_new_2[9],round(aggiornamento_2[9] + aggiornamento_new_2[9], 2), verticalalignment='bottom',horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[10], aggiornamento_2[10] + aggiornamento_new_2[10],round(aggiornamento_2[10] + aggiornamento_new_2[10], 2), verticalalignment='bottom',horizontalalignment='right',color=color_22,alpha=alpha_22)
            ax0.text(x_ax2[11], aggiornamento_2[11] + aggiornamento_new_2[11],round(aggiornamento_2[11] + aggiornamento_new_2[11], 2), verticalalignment='bottom',horizontalalignment='right',color=color_22,alpha=alpha_22)

        ax0.text(x_ax1[0], aggiornamento_1[0], round(aggiornamento_1[0], 2), verticalalignment='bottom',
                 horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[1], aggiornamento_1[1], round(aggiornamento_1[1], 2), verticalalignment='bottom',
                 horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[2], aggiornamento_1[2], round(aggiornamento_1[2], 2), verticalalignment='bottom',
                 horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[3], aggiornamento_1[3], round(aggiornamento_1[3], 2), verticalalignment='bottom',
                 horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[4], aggiornamento_1[4], round(aggiornamento_1[4], 2), verticalalignment='bottom',
                 horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[5], aggiornamento_1[5], round(aggiornamento_1[5], 2), verticalalignment='bottom',
                 horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[6], aggiornamento_1[6], round(aggiornamento_1[6], 2), verticalalignment='bottom',horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[7], aggiornamento_1[7], round(aggiornamento_1[7], 2), verticalalignment='bottom',horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[8], aggiornamento_1[8], round(aggiornamento_1[8], 2), verticalalignment='bottom',horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[9], aggiornamento_1[9], round(aggiornamento_1[9], 2), verticalalignment='bottom',horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[10], aggiornamento_1[10], round(aggiornamento_1[10], 2), verticalalignment='bottom',horizontalalignment='left',color=color_11,alpha=alpha_11)
        ax0.text(x_ax1[11], aggiornamento_1[11], round(aggiornamento_1[11], 2), verticalalignment='bottom',horizontalalignment='left',color=color_11,alpha=alpha_11)

        ax0.text(x_ax2[0], aggiornamento_2[0], round(aggiornamento_2[0], 2), verticalalignment='bottom',
                 horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[1], aggiornamento_2[1], round(aggiornamento_2[1], 2), verticalalignment='bottom',
                 horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[2], aggiornamento_2[2], round(aggiornamento_2[2], 2), verticalalignment='bottom',
                 horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[3], aggiornamento_2[3], round(aggiornamento_2[3], 2), verticalalignment='bottom',
                 horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[4], aggiornamento_2[4], round(aggiornamento_2[4], 2), verticalalignment='bottom',
                 horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[5], aggiornamento_2[5], round(aggiornamento_2[5], 2), verticalalignment='bottom',
                 horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[6], aggiornamento_2[6], round(aggiornamento_2[6], 2), verticalalignment='bottom',horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[7], aggiornamento_2[7], round(aggiornamento_2[7], 2), verticalalignment='bottom',horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[8], aggiornamento_2[8], round(aggiornamento_2[8], 2), verticalalignment='bottom',horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[9], aggiornamento_2[9], round(aggiornamento_2[9], 2), verticalalignment='bottom',horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[10], aggiornamento_2[10], round(aggiornamento_2[10], 2), verticalalignment='bottom',horizontalalignment='right',color=color_12,alpha=alpha_12)
        ax0.text(x_ax2[11], aggiornamento_2[11], round(aggiornamento_2[11], 2), verticalalignment='bottom',horizontalalignment='right',color=color_12,alpha=alpha_12)

        the_table_1 = ax2.table(cellText=output_table_name1.values,  colLabels=labels_NJORD, rowLabels=row_1,loc="best")
        the_table_1.auto_set_column_width(col=list(range(len(output_table_name1.columns))))
        the_table_2 = ax1.table(cellText=output_table_name2.values, colLabels=labels_NJORD, rowLabels=row_2,loc="best")
        the_table_2.auto_set_column_width(col=list(range(len(output_table_name2.columns))))
        #ax2.set_title("Result for model: "+my_entry_0.get(), fontsize=20,font="Myriad Pro")
        the_table_1.auto_set_font_size(False)
        the_table_1.set_fontsize(10)
        the_table_1.scale(1,1.5)
        the_table_2.auto_set_font_size(False)
        the_table_2.set_fontsize(10)
        the_table_2.scale(1,1.5)
        ax1.set_title("Result for model: " + r"$\bf{" + str(my_list_7.get(ANCHOR)) + "}$ ", fontsize=18, )
        ax1.xaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
        ax1.axis("off")
        ax2.set_title("Result for model: " + r"$\bf{" + str(my_list_0.get(ANCHOR)) + "}$ ", fontsize=20, )
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.axis("off")
        ax0.set_title("Predicted accumulated capacity [MW] for: " + r"$\bf{" + str(my_list_0.get(ANCHOR)) + "}$ ",fontsize=18)
        ax0.set_xlabel("Year", fontsize=15)
        ax0.set_ylabel("Accumulated capacity [MW]", fontsize=15)
        ax0.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax0.set_xticks((np.arange(2009, 2021, 1.0)))
        plt.tight_layout()
        a = ScrollableWindow(fig)
        #plt.text(0.18, 0.01, xlabell, fontsize=10, transform=plt.gcf().transFigure)
        #plt.show()
        root.mainloop()
        #ax0.set_xticks(range(min(x_ax1), max(x_ax1) + 1))
    else:
        NJORD = pd.read_excel(model + "_model_results.xlsx", index_col=0)
        accumulated_reference_data = pd.read_excel("Reference_accumulated_2022.xlsx", index_col=0)
        accumulated_installed_2009 = accumulated_reference_data["2009 - Total"]
        x_axis_1 = []
        y_axis_1 = []
        y_axis_ref_1 = []
        x_axis_ref_1 = []
        x_axis_2 = []
        y_axis_2 = []
        y_axis_ref_2 = []
        x_axis_ref_2 = []
        source_list_1 = []
        source_list_2 = []
        ref_irena_1 = []
        ref_pvps_1 = []
        ref_other_1 = []
        ref_irena_2 = []
        ref_pvps_2 = []
        ref_other_2 = []
        valore_y_1 = float(accumulated_installed_2009[name_1])
        valore_y_2 = float(accumulated_installed_2009[name_2])
        y_axis_1.append(valore_y_1)
        x_axis_1.append(2009.75)
        y_axis_ref_1.append(accumulated_reference_data["2009 - Total"][name_1])
        x_axis_ref_1.append(2009.75)
        y_axis_2.append(valore_y_2)
        x_axis_2.append(2009.75)
        y_axis_ref_2.append(accumulated_reference_data["2009 - Total"][name_2])
        x_axis_ref_2.append(2009.75)
        source_0_1 = (NJORD["Source 2009"][name_1])
        source_0_2 = (NJORD["Source 2009"][name_2])
        output_table_name1.at["2009", "NJORD [MW]"] = "-"
        output_table_name1.at["2009", "Ref. value"] = accumulated_reference_data["2009 - Total"][name_1]
        output_table_name2.at["2009", "NJORD [MW]"] = "-"
        output_table_name2.at["2009", "Ref. value"] = accumulated_reference_data["2009 - Total"][name_2]
        ref_table_irena_1.at["2009", " Irena [MW]"] = accumulated_reference_data["2009 - IRENA"][name_1.replace("_", " ")]

        if accumulated_reference_data["2009 - IRENA s"][name_1.replace("_", " ")] == "q":
            ref_table_irena_1.at["2009", " Irena source"] = "Questionnaire"
        if accumulated_reference_data["2009 - IRENA s"][name_1.replace("_", " ")] == "o":
            ref_table_irena_1.at["2009", " Irena source"] = "Official"
        if accumulated_reference_data["2009 - IRENA s"][name_1.replace("_", " ")] == "u":
            ref_table_irena_1.at["2009", " Irena source"] = "Unofficial"
        if accumulated_reference_data["2009 - IRENA s"][name_1.replace("_", " ")] == "e":
            ref_table_irena_1.at["2009", " Irena source"] = "Estimates"

        if accumulated_reference_data["2009 - IRENA s"][name_2.replace("_", " ")] == "q":
            ref_table_irena_2.at["2009", " Irena source"] = "Questionnaire"
        if accumulated_reference_data["2009 - IRENA s"][name_2.replace("_", " ")] == "o":
            ref_table_irena_2.at["2009", " Irena source"] = "Official"
        if accumulated_reference_data["2009 - IRENA s"][name_2.replace("_", " ")] == "u":
            ref_table_irena_2.at["2009", " Irena source"] = "Unofficial"
        if accumulated_reference_data["2009 - IRENA s"][name_2.replace("_", " ")] == "e":
            ref_table_irena_2.at["2009", " Irena source"] = "Estimates"

        ref_table_other_1.at["2009", " Other [MW]"] = accumulated_reference_data["2009 - Other"][name_1.replace("_", " ")]
        ref_table_pvps_1.at["2009", " PVPS [MW]"] = accumulated_reference_data["2009 - PVPS"][name_1.replace("_", " ")]
        ref_table_irena_2.at["2009", " Irena [MW]"] = accumulated_reference_data["2009 - IRENA"][name_2.replace("_", " ")]
        ref_table_other_2.at["2009", " Other [MW]"] = accumulated_reference_data["2009 - Other"][name_2.replace("_", " ")]
        ref_table_pvps_2.at["2009", " PVPS [MW]"] = accumulated_reference_data["2009 - PVPS"][name_2.replace("_", " ")]
        ref_irena_1.append(accumulated_reference_data["2009 - IRENA"][name_1.replace("_", " ")])
        ref_pvps_1.append(accumulated_reference_data["2009 - PVPS"][name_1.replace("_", " ")])
        ref_other_1.append(accumulated_reference_data["2009 - Other"][name_1.replace("_", " ")])
        ref_irena_2.append(accumulated_reference_data["2009 - IRENA"][name_2.replace("_", " ")])
        ref_pvps_2.append(accumulated_reference_data["2009 - PVPS"][name_2.replace("_", " ")])
        ref_other_2.append(accumulated_reference_data["2009 - Other"][name_2.replace("_", " ")])
        if source_0_1 == "Irena":
            lettera_1 = "Irena"
        if source_0_1 == "No Ref":
            lettera_1 = "No ref"
        if source_0_1 == "Other":
            lettera_1 = "Other"
        if source_0_1 == "PVPS":
            lettera_1 = "PVPS"
        if name_1 in regions:
            lettera_1 = "regions"
        if source_0_2 == "Irena":
            lettera_2 = "Irena"
        if source_0_2 == "No Ref":
            lettera_2 = "No ref"
        if source_0_2 == "Other":
            lettera_2 = "Other"
        if source_0_2 == "PVPS":
            lettera_2 = "PVPS"
        if name_2 in regions:
            lettera_2 = "regions"
        source_list_1.append("St Po")
        source_list_2.append("St Po")
        output_table_name1.at["2009", "Ref. Source"] =lettera_1
        output_table_name2.at["2009", "Ref. Source"] = lettera_2
        x_value = 2009.75
        for anno in desiderio:
            only_anno = anno.split("-")
            only_anno = only_anno[0]
            x_value=x_value+0.25
            valore_NJORD_1 = NJORD["NJORD " + str(anno)][name_1]
            valore_reference_1 = accumulated_reference_data[str(only_anno) + " - Total"][name_1]
            ref_table_irena_1.at[anno, " Irena [MW]"] = accumulated_reference_data[str(only_anno) + " - IRENA"][name_1.replace("_", " ")]

            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_1.replace("_", " ")] == "q":
                ref_table_irena_1.at[anno, " Irena source"] = "Questionnaire"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_1.replace("_", " ")] == "o":
                ref_table_irena_1.at[anno, " Irena source"] = "Official"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_1.replace("_", " ")] == "u":
                ref_table_irena_1.at[anno, " Irena source"] = "Unofficial"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_1.replace("_", " ")] == "e":
                ref_table_irena_1.at[anno, " Irena source"] = "Estimates"

            ref_table_other_1.at[anno, " Other [MW]"] = accumulated_reference_data[str(only_anno) +" - Other"][name_1.replace("_", " ")]
            ref_table_pvps_1.at[anno, " PVPS [MW]"] = accumulated_reference_data[str(only_anno) +" - PVPS"][name_1.replace("_", " ")]
            ref_table_irena_2.at[anno, " Irena [MW]"] = accumulated_reference_data[str(only_anno) +" - IRENA"][name_2.replace("_", " ")]

            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_2.replace("_", " ")] == "q":
                ref_table_irena_2.at[anno, " Irena source"] = "Questionnaire"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_2.replace("_", " ")] == "o":
                ref_table_irena_2.at[anno, " Irena source"] = "Official"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_2.replace("_", " ")] == "u":
                ref_table_irena_2.at[anno, " Irena source"] = "Unofficial"
            if accumulated_reference_data[str(only_anno)+" - IRENA s"][name_2.replace("_", " ")] == "e":
                ref_table_irena_2.at[anno, " Irena source"] = "Estimates"

            ref_table_other_2.at[anno, " Other [MW]"] = accumulated_reference_data[str(only_anno) +" - Other"][name_2.replace("_", " ")]
            ref_table_pvps_2.at[anno, " PVPS [MW]"] = accumulated_reference_data[str(only_anno) +" - PVPS"][name_2.replace("_", " ")]
            source_1 = NJORD["Source " + str(only_anno)][name_1]

            if source_1 == "Irena":
                lettera_1 = "Irena"
            if source_1 == "No Ref":
                lettera_1 = "No ref"
            if source_1 == "Other":
                lettera_1 = "Other"
            if source_1 == "PVPS":
                lettera_1 = "PVPS"
            source_list_1.append(lettera_1)
            print(valore_reference_1, "valore", source_list_1)
            if valore_NJORD_1 < 0:
                valore_y_1 = float(valore_y_1)
            else:
                valore_y_1 = float(valore_y_1) + float(NJORD["NJORD " + str(anno)][name_1])
            y_axis_1.append(valore_y_1)
            y_axis_ref_1.append(valore_reference_1)
            x_axis_1.append(x_value)
            x_axis_ref_1.append((int(only_anno)+1))
            valore_NJORD_2 = NJORD["NJORD " + str(anno)][name_2]
            valore_reference_2 = accumulated_reference_data[str(only_anno) + " - Total"][name_2]
            source_2 = NJORD["Source " + str(only_anno)][name_2]
            ref_irena_1.append(accumulated_reference_data[str(only_anno) + " - IRENA"][name_1.replace("_", " ")])
            ref_pvps_1.append(accumulated_reference_data[str(only_anno) + " - PVPS"][name_1.replace("_", " ")])
            ref_other_1.append(accumulated_reference_data[str(only_anno) + " - Other"][name_1.replace("_", " ")])
            ref_irena_2.append(accumulated_reference_data[str(only_anno) + " - IRENA"][name_2.replace("_", " ")])
            ref_pvps_2.append(accumulated_reference_data[str(only_anno) + " - PVPS"][name_2.replace("_", " ")])
            ref_other_2.append(accumulated_reference_data[str(only_anno) + " - Other"][name_2.replace("_", " ")])
            if source_2 == "Irena":
                lettera_2 = "Irena"
            if source_2 == "No Ref":
                lettera_2 = "No ref"
            if source_2 == "Other":
                lettera_2 = "Other"
            if source_2 == "PVPS":
                lettera_2 = "PVPS"
            source_list_2.append(lettera_2)
            print(valore_reference_2, "valore", source_list_2)
            if valore_NJORD_2 < 0:
                valore_y_2 = float(valore_y_2)
            else:
                valore_y_2 = float(valore_y_2) + float(NJORD["NJORD " + str(anno)][name_2])
            y_axis_2.append(valore_y_2)
            y_axis_ref_2.append(valore_reference_2)
            x_axis_2.append(x_value)
            x_axis_ref_2.append((int(only_anno)+1))
            output_table_name1.at[anno, "Ref. Source"] = lettera_1
            output_table_name2.at[anno, "Ref. Source"] = lettera_2
            output_table_name1.at[anno, "Ref. value"] = valore_reference_1
            output_table_name2.at[anno, "Ref. value"] = valore_reference_2
            output_table_name1.at[anno, "NJORD [MW]"] = round(valore_y_1,2)
            output_table_name2.at[anno, "NJORD [MW]"] = round(valore_y_2,2)
        fig, ax = plt.subplots(figsize=(18,30))
        G = gridspec.GridSpec(3, 2)
        ax0 = plt.subplot(G[0, :])
        ax1 = plt.subplot(G[1:2, 0])
        ax2 = plt.subplot(G[1:2, 1])

        xlabell_1 = "References source for each year: "
        xlabell_2 = "References source for each year: "
        for i in range(1, len(x_axis_1)):
            xlabell_1 = str(xlabell_1) + r"$\bf{" + str(source_list_1[i]) + ",   " + "}$"
        for i in range(1, len(x_axis_2)):
            xlabell_2 = str(xlabell_2) + r"$\bf{" + str(source_list_2[i]) + ",   " + "}$"

        # ax.set(xlabel=str(xlabell),ylabel="Accumulated capacity [MW]",fontsize=10)
        ax0.set_xlabel("Year", fontsize=15)
        ax0.set_ylabel("Accumulated capacity [MW]", fontsize=15)
        # ax.set(xlabel="Year \nReferences:"+str(x_axis[0])+":"+str(source_list[0])+", "+str(x_axis[1])+":"+str(source_list[1])+", "+str(x_axis[2])+":"+str(source_list[2])+", "+str(x_axis[3])+":"+str(source_list[3])+", "+str(x_axis[4])+":"+str(source_list[4])+", "+str(x_axis[5])+":"+str(source_list[5])+", "+str(x_axis[6])+":"+str(source_list[6]),ylabel="Accumulated capacity [MW]",title="Accumulated installed capacity for "+r"$\bf{" + name + "}$"+"\n NJORD value: "+str(round(valore_y,2))+"MW and reference value: "+ str(round(valore_reference,2))+"MW\n")
        ax0.set_title("\n \n NJORD value for "+r"$\bf{" + name_1 + "}$"" and " +r"$\bf{" + name_2 + "}$ ",  fontsize=19)
        #plt.suptitle("" + "Accumulated installed capacity for " + r"$\bf{" + name_1 + "}$ "+"and "+r"$\bf{" + name_2 + "}$ ", fontsize=15)
        referenza = valore_comma.get()
        referenza_irena = valore_comma_irena.get()  # option in the GUI to plot or not reference data
        referenza_other = valore_comma_other.get()  # option in the GUI to plot or not reference data
        referenza_pvps = valore_comma_pvps.get()
        if referenza_pvps == 1:
            ax0.plot(x_axis_ref_1, ref_pvps_1, marker="<", linestyle='--', label="PVPS ref for " + name_1, alpha=0.3)
            output_table_name1 = output_table_name1.join(ref_table_pvps_1)
            ax0.plot(x_axis_ref_2, ref_pvps_2, marker="<", linestyle='--', label="PVPS reffor " + name_2, alpha=0.3)
            output_table_name2 = output_table_name2.join(ref_table_pvps_2)
        if referenza_irena == 1:
            ax0.plot(x_axis_ref_1, ref_irena_1, marker="^", linestyle='-.', label="Ref Irena for " + name_1, alpha=0.3)
            output_table_name1 = output_table_name1.join(ref_table_irena_1)
            ax0.plot(x_axis_ref_2, ref_irena_2, marker="^", linestyle='-.', label="Ref Irena for " + name_2, alpha=0.3)
            output_table_name2 = output_table_name2.join(ref_table_irena_2)
        if referenza_other == 1:
            ax0.plot(x_axis_ref_1, ref_other_1, marker="*", linestyle='--', label="Ref Other for " + name_1, alpha=0.3)
            output_table_name1 = output_table_name1.join(ref_table_other_1)
            ax0.plot(x_axis_ref_2, ref_other_2, marker="*", linestyle='--', label="Ref Other for " + name_2, alpha=0.3)
            output_table_name2 = output_table_name2.join(ref_table_other_2)
        if referenza == 0:
            print("no ref")
        else:
            ax0.plot(x_axis_ref_1, y_axis_ref_1, marker="+", label="Reference for " + name_1, alpha=0.3, color="#FF1926")
            ax0.plot(x_axis_ref_2, y_axis_ref_2, marker="+", label="Reference for " + name_2, alpha=0.3, color="#CCFF00")
        ax0.plot(x_axis_1, y_axis_1, marker="o", label=name_1,color="#C30017")
        ax0.plot(x_axis_2, y_axis_2, marker="o", label=name_2,color="#FFA626")
        # ax.text(min(x_axis), max(y_axis), 'boxed italics text in data coords', style='italic',bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        the_table_1 = ax1.table(cellText=output_table_name1.values, rowLabels=desiderio_lab, colLabels=output_table_name1.columns,loc="best")
        the_table_1.auto_set_column_width(col=list(range(len(output_table_name1.columns))))
        the_table_2 = ax2.table(cellText=output_table_name2.values, rowLabels=desiderio_lab, colLabels=output_table_name2.columns,loc="best")
        the_table_2.auto_set_column_width(col=list(range(len(output_table_name2.columns))))
        ax1.set_title("Result for model: "r"$\bf{" + name_1.replace("_"," ") + "}$ ", fontsize=18)
        ax1.xaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
        ax1.axis("off")
        ax2.set_title("Result for model: "r"$\bf{" + name_2.replace("_"," ") + "}$ ", fontsize=18)
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.axis("off")
        the_table_1.set_fontsize(10)
        the_table_1.scale(1, 1.5)
        the_table_2.set_fontsize(10)
        the_table_2.scale(1, 1.5)
        ax0.legend()
        ax0.set_xticks((np.arange(2009, 2022, 1.0)))

        a = ScrollableWindow(fig)  # if Wor #
        plt.tight_layout()
        #plt.text(0.18, 0.03, xlabell_1, fontsize=10, transform=plt.gcf().transFigure)
        #plt.text(0.18, 0.01, xlabell_2, fontsize=10, transform=plt.gcf().transFigure)
        #plt.show()
        root.mainloop()
        plt.close()

            ## functions to read the input from the GUI ###
        #IMPORTANT: the region input box is checked for inputs, if no input is present the single region
        #           will be read!

def model_comparison():
    try:
        name=my_entry_0.get()
        #year = my_entry_1.get()
        model_1 = my_entry_5.get()
        model_2 = my_entry_2.get()
        two_model_comparison(name, year, model_1, model_2)
    except KeyError:
        print("I use single nation") # Why is this thrown every run?
    else:
        name = my_entry.get()
        #year = my_entry_1.get()
        model_1 = my_entry_5.get()
        model_2 = my_entry_2.get()
        two_model_comparison(name, year, model_1, model_2)
    name = my_entry.get()
    model_1 = my_entry_5.get()
    model_2 = my_entry_2.get()
    two_model_comparison(name, year, model_1, model_2)


def nations_comparison():
    try:
        name_1=my_entry_0.get()
        name_2=my_entry_7.get()
        # year = my_entry_1.get()
        model = my_entry_2.get()
        two_states_comparison(name_1, name_2, year, model)
    except KeyError:
        print("I use single nation")
    else:
        name_1 = my_entry.get()
        name_2=my_entry_4.get()
        # year = my_entry_1.get()
        model = my_entry_2.get()
        two_states_comparison(name_1, name_2, year, model)
    name_1 = my_entry.get()
    name_2 = my_entry_4.get()
    # year = my_entry_1.get()
    model = my_entry_2.get()
    two_states_comparison(name_1, name_2, year, model)


def single_models():
    try:
        name = my_entry_0.get()
        # year = my_entry_1.get()
        model = my_entry_2.get()
        visualization(name, year, model)
    except KeyError:
        print("I use single nation")
        name = my_entry.get()
        # year= my_entry_1.get()
        model = my_entry_2.get()
        visualization(name, year, model)
            ##############################################


        #### functions used to update the input boxes and to do the auto-filling
def update15(data):
    ### Clear list box ##
    my_list_15.delete(0, END)
    ### add Nations ###
    for item in data:
        my_list_15.insert(END, item)
def update7(data):
    ### Clear list box ##
    my_list_7.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_7.insert(END, item)
def update0(data):
    ### Clear list box ##
    my_list_0.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_0.insert(END, item)
def update(data):
    ### Clear list box ##
    my_list.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list.insert(END, item)
def update1(data):
    ### Clear list box ##
    #my_list_1.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_1.insert(END, item)
def update2(data):
    ### Clear list box ##
    my_list_2.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_2.insert(END, item)
def update3(data):
    ### Clear list box ##
    my_list_3.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_3.insert(END, item)
def update4(data):
    ### Clear list box ##
    my_list_4.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_4.insert(END, item)
def update5(data):
    ### Clear list box ##
    my_list_5.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_5.insert(END, item)
def update6(data):
    ### Clear list box ##
    my_list_6.delete(0,END)
    ### add Nations ###
    for item in data:
        my_list_6.insert(END, item)
def fillout7(event):
    my_entry_7.delete(0, END)
    my_entry_7.insert(0,my_list_7.get(ACTIVE))
    my_list_7.bind("<<ListboxSelect>>", liste2)
def fillout0(event):
    my_entry_0.delete(0, END)
    my_entry_0.insert(0,my_list_0.get(ACTIVE))
    my_list_0.bind("<<ListboxSelect>>", liste)
def fillout(event):
    my_entry.delete(0, END)
    my_entry.insert(0,my_list.get(ACTIVE))
def fillout1(event):
    my_entry_1.delete(0, END)
    my_entry_1.insert(0,my_list_1.get(ACTIVE))
def fillout2(event):
    my_entry_2.delete(0, END)
    my_entry_2.insert(0,my_list_2.get(ACTIVE))
def fillout2(event):
    my_entry_2.delete(0, END)
    my_entry_2.insert(0,my_list_2.get(ACTIVE))
def fillout3(event):
    my_entry_3.delete(0, END)
    my_entry_3.insert(0,my_list_3.get(ACTIVE))
def fillout4(event):
    my_entry_4.delete(0, END)
    my_entry_4.insert(0,my_list_4.get(ACTIVE))
def fillout5(event):
    my_entry_5.delete(0, END)
    my_entry_5.insert(0,my_list_5.get(ACTIVE))
def fillout15(event):
    my_entry_5.delete(0, END)
    my_entry_5.insert(0,my_list_5.get(ACTIVE))
def fillout6(event):
    my_entry_6.delete(0, END)
    my_entry_6.insert(0,my_list_6.get(ACTIVE))
def check7(event):
    #what is typed#
    typed=my_entry_7.get()
    if typed == '':
        data = regions
    else:
        data=[]
        for item in regions:
            if typed.lower() in item.lower():
                data.append(item)
    update7(data)

def check0(event):
    #what is typed#
    typed=my_entry_0.get()
    if typed == '':
        data = regions
        choices = eval(str(my_entry_0.get))
        checklist = ChecklistBox(root, choices, bd=1, relief="sunken", background="white")
        checklist.grid(row=2, column=3)
    else:
        data=[]
        for item in regions:
            if typed.lower() in item.lower():
                data.append(item)
    update0(data)
def check(event):
    #what is typed#
    typed=my_entry.get()
    if typed == '':
        data = nations
    else:
        data=[]
        for item in nations:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)
def check1(event):
    #what is typed#
    typed=my_entry_1.get()
    if typed == '':
        data = period
    else:
        data=[]
        for item in period:
            if typed.lower() in item.lower():
                data.append(item)
    update1(data)
def check2(event):
    #what is typed#
    typed=my_entry_2.get()
    if typed == '':
        data = models
    else:
        data=[]
        for item in period:
            if typed.lower() in item.lower():
                data.append(item)
    update2(data)
def check3(event):
    #what is typed#
    typed=my_entry_3.get()
    if typed == '':
        data = models
    else:
        data=[]
        for item in period:
            if typed.lower() in item.lower():
                data.append(item)
    update3(data)
def check4(event):
    #what is typed#
    typed = my_entry_4.get()
    if typed == '':
        data = nations
    else:
        data=[]
        for item in nations:
            if typed.lower() in item.lower():
                data.append(item)
    update4(data)
def check5(event):
    #what is typed#
    typed = my_entry_5.get()
    if typed == '':
        data = models
    else:
        data=[]
        for item in period:
            if typed.lower() in item.lower():
                data.append(item)
    update5(data)
def check15(event):
    #what is typed#
    typed = my_entry_0.get()
    if typed == '':
        data = "Select region"
    else:
        data=[]
        for item in eval(regions):
            if typed.lower() in item.lower():
                data.append(item)
    update15(data)
def check6(event):
    #what is typed#
    typed = my_entry_6.get()
    if typed == '':
        data = models
    else:
        data=[]
        for item in period:
            if typed.lower() in item.lower():
                data.append(item)
    update6(data)

    ##########################################

def nation_in_region(event):
    if my_list_0.get(ANCHOR) == "Ref_country":
        var=0
        for item in Ref_country:
            exec("group" + str(item) + "= self.getGroup(selected, header + i)")
            l=Checkbutton(root, text=str(item), variable=exec("group" + str(item) + "= self.getGroup(selected, header + i)"), onvalue=1, offvalue=0)
            l.grid(row=var,column=5)
            var = var + 1

box_list=[]
totale_ref=IntVar()

### functions to create the dictionaries used in program
def liste(event):
    if my_list_0.get(ANCHOR) == "Ref. country":
        var = 0
        for item in Ref_country:
            dict_ref_country[item] = IntVar()
        for item in dict_ref_country:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_ref_country[item])
            l.place(x=360,y=2+var*20)
            var = var + 1
            check_box_list.append(l)

    if my_list_0.get(ANCHOR) == "Asia":
        print("Asia")
        cont=0
        var = 0
        var_30=0
        for item in Asia:
            dict_asia[item] = IntVar()
        for item in dict_asia:
            cont = cont + 1
            if cont > 20:
                print("entrato")
                l = Checkbutton(root, text=item, variable=dict_asia[item])
                l.place(x=460, y=2 + var_30 * 20)
                var_30 = var_30 + 1
                check_box_list.append(l)
            else:
                print("non ancora")
                l = Checkbutton(root, text=item, variable=dict_asia[item])
                l.place(x=360, y=2 + var * 20)
                var = var + 1
                check_box_list.append(l)
        print(dict_asia)
    if my_list_0.get(ANCHOR) == "Africa":
        var = 0
        var_30 = 0
        cont=0
        for item in Africa:
            dict_africa[item] = IntVar()
        for item in dict_africa:
            cont=cont+1
            if cont > 28:
                print("entrato")
                l = Checkbutton(root, text=item, variable=dict_africa[item])
                l.place(x=460, y=2 + var_30 * 18)
                var_30 = var_30 + 1
                check_box_list.append(l)
            else:
                # print(item)
                l = Checkbutton(root, text=item, variable=dict_africa[item])
                l.place(x=360,y=2+var*18)
                var = var + 1
                check_box_list.append(l)

    if my_list_0.get(ANCHOR) == "Central America":
        var = 0
        for item in Central_America:
            dict_central_america[item] = IntVar()
        for item in dict_central_america:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_central_america[item])
            l.place(x=360,y=2+var*20)
            var = var + 1
            check_box_list.append(l)

    if my_list_0.get(ANCHOR) == "Eurasia":
        var = 0
        for item in Eurasia:
            dict_eurasia[item] = IntVar()
        for item in dict_eurasia:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_eurasia[item])
            l.place(x=360,y=2+var*20)
            var = var + 1
            check_box_list.append(l)

    if my_list_0.get(ANCHOR) == "Europe":
        var = 0
        var_30 = 0
        cont=0
        for item in Europe:
            dict_europe[item] = IntVar()
        for item in dict_europe:
            cont = cont + 1
            if cont > 24:

                # print(item)
                l = Checkbutton(root, text=item, variable=dict_europe[item])
                l.place(x=460,y=2+var_30*18)
                var_30 = var_30 + 1
                check_box_list.append(l)
            else:
                # print(item)
                l = Checkbutton(root, text=item, variable=dict_europe[item])
                l.place(x=360, y=2 + var * 20)
                var = var + 1
                check_box_list.append(l)


    if my_list_0.get(ANCHOR) == "Middle East":
        var = 0
        for item in Middle_East:
            dict_middle_east[item] = IntVar()
        for item in dict_middle_east:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_middle_east[item])
            l.place(x=360,y=2+var*20)
            var = var + 1
            check_box_list.append(l)

    if my_list_0.get(ANCHOR) == "North America":
        var = 0
        for item in North_America:
            dict_north_america[item] = IntVar()
        for item in dict_north_america:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_north_america[item])
            l.place(x=360, y=2 + var * 20)
            var = var + 1
            check_box_list.append(l)


    if my_list_0.get(ANCHOR) == "Oceania":
        var = 0
        for item in Oceania:
            dict_oceania[item] = IntVar()
        for item in dict_oceania:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_oceania[item])
            l.place(x=360, y=2 + var * 20)
            var = var + 1
            check_box_list.append(l)

    if my_list_0.get(ANCHOR) == "South America":
        var = 0
        for item in South_America:
            dict_south_america[item] = IntVar()
        for item in dict_south_america:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_south_america[item])
            l.place(x=360, y=2 + var * 20)
            var = var + 1
            check_box_list.append(l)

    my_list_0.bind("<<ListboxSelect>>", fillout0)


def liste2(event):
    if my_list_7.get(ANCHOR) == "Ref. country":
        var = 0
        for item in Ref_country:
            dict_ref_country[item] = IntVar()
        for item in dict_ref_country:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_ref_country[item])
            l.place(x=900,y=2+var*20)
            var = var + 1
            check_box_list2.append(l)

    if my_list_7.get(ANCHOR) == "Asia":
        print("Asia")
        cont=0
        var = 0
        var_30=0
        for item in Asia:
            dict_asia[item] = IntVar()
        for item in dict_asia:
            cont = cont + 1
            if cont > 20:
                print("entrato")
                l = Checkbutton(root, text=item, variable=dict_asia[item])
                l.place(x=1000, y=2 + var_30 * 20)
                var_30 = var_30 + 1
                check_box_list2.append(l)
            else:
                print("non ancora")
                l = Checkbutton(root, text=item, variable=dict_asia[item])
                l.place(x=900, y=2 + var * 20)
                var = var + 1
                check_box_list2.append(l)
    if my_list_7.get(ANCHOR) == "Africa":
        cont = 0
        var = 0
        var_30 = 0
        for item in Africa:
            dict_africa[item] = IntVar()
        for item in dict_africa:
            cont = cont + 1
            if cont > 28:
                print("entrato")
                l = Checkbutton(root, text=item, variable=dict_africa[item])
                l.place(x=1000, y=2 + var_30 * 18)
                var_30 = var_30 + 1
                check_box_list2.append(l)
            else:
            # print(item)
                l = Checkbutton(root, text=item, variable=dict_africa[item])
                l.place(x=900,y=2+var*18)
                var = var + 1
                check_box_list2.append(l)

    if my_list_7.get(ANCHOR) == "Central America":
        var = 0
        for item in Central_America:
            dict_central_america[item] = IntVar()
        for item in dict_central_america:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_central_america[item])
            l.place(x=900,y=2+var*20)
            var = var + 1
            check_box_list2.append(l)
    if my_list_7.get(ANCHOR) == "Eurasia":
        var = 0
        for item in Eurasia:
            dict_eurasia[item] = IntVar()
        for item in dict_eurasia:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_eurasia[item])
            l.place(x=900,y=2+var*20)
            var = var + 1
            check_box_list2.append(l)
    if my_list_7.get(ANCHOR) == "Europe":
        cont = 0
        var = 0
        var_30 = 0
        for item in Europe:
            dict_europe[item] = IntVar()
        for item in dict_europe:
            cont = cont + 1
            if cont > 24:
                print("entrato")
                l = Checkbutton(root, text=item, variable=dict_europe[item])
                l.place(x=1000, y=2 + var_30 * 20)
                var_30 = var_30 + 1
                check_box_list2.append(l)
            else:
                # print(item)
                l = Checkbutton(root, text=item, variable=dict_europe[item])
                l.place(x=900,y=2+var*20)
                var = var + 1
                check_box_list2.append(l)

    if my_list_7.get(ANCHOR) == "Middle East":
        var = 0
        for item in Middle_East:
            dict_middle_east[item] = IntVar()
        for item in dict_middle_east:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_middle_east[item])
            l.place(x=900,y=2+var*20)
            var = var + 1
            check_box_list2.append(l)
    if my_list_7.get(ANCHOR) == "North America":
        var = 0
        for item in North_America:
            dict_north_america[item] = IntVar()
        for item in dict_north_america:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_north_america[item])
            l.place(x=900, y=2 + var * 20)
            var = var + 1
            check_box_list2.append(l)

    if my_list_7.get(ANCHOR) == "Oceania":
        var = 0
        for item in Oceania:
            dict_oceania[item] = IntVar()
        for item in dict_oceania:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_oceania[item])
            l.place(x=900, y=2 + var * 20)
            var = var + 1
            check_box_list2.append(l)
    if my_list_7.get(ANCHOR) == "South America":
        var = 0
        dict_south_america = {}
        for item in South_America:
            dict_south_america[item] = IntVar()
        for item in dict_south_america:
            # print(item)
            l = Checkbutton(root, text=item, variable=dict_south_america[item])
            l.place(x=900, y=2 + var * 20)
            var = var + 1
            check_box_list2.append(l)
    my_list_7.bind("<<ListboxSelect>>", fillout7)
##########################################3

### Select all, remove all, refresh buttons funtions
def sel_all():
    for trust in check_box_list:
        trust.select()
def des_all():
    for i in check_box_list:
        i.deselect()
def sel_all2():
    for trust in check_box_list2:
        trust.select()
def des_all2():
    for i in check_box_list2:
        i.deselect()
def refresh():
    for pain in check_box_list:
        pain.forget()
        pain.place(x=-100,y=-100)
def refresh_2():
    #print(dict_ref_country)
    for pain in check_box_list2:
        pain.forget()
        pain.place(x=-100,y=-100)
###################################################


### buttons configuration and setting in the GUI
#models=["Combined","Price","Price_MF","Price_max","Price_MF_max","Weight","Weight_max"]
nation_list = pd.read_excel("Weight_model_results.xlsx", index_col=0)
z = nation_list.index
nations = li = [x.split('.')[0] for x in z]
my_label = Label(root, text="Nation", font=("Helvetica", 14), fg="green")
my_label.grid(row=0, column=1,  pady=2)
my_entry = Entry(root, font=("Helvetica", 20))
my_entry.grid(row=1, column=1,  pady=2)
my_list = Listbox(root, width=50, height=5)
my_list.grid(row=2, column=1,  pady=2)
update(nations)
##Create a binding on the list box ###
my_list.bind("<<ListboxSelect>>", fillout)
##Create a binding on the entry box ###
my_entry.bind("<KeyRelease>", check)
valore_comma = IntVar()
show_ref = Checkbutton(root, variable=valore_comma, text="Show best Ref.", font=("Helvetica", 8), fg="gray")
show_ref.grid(row=13, column=1)
my_entry.bind("<KeyRelease>", check)
valore_comma_irena = IntVar()
show_ref_2 = Checkbutton(root, variable=valore_comma_irena, text="Show Irena Ref.", font=("Helvetica", 8), fg="gray")
show_ref_2.place(x=60, y=531)
valore_comma_pvps = IntVar()
show_ref_3 = Checkbutton(root, variable=valore_comma_pvps, text="Show PVPS Ref.", font=("Helvetica", 8), fg="gray")
show_ref_3.place(x=60,y=555)
valore_comma_other = IntVar()
show_ref_4 = Checkbutton(root, variable=valore_comma_other, text="Show Other Ref.",font=("Helvetica",8),fg="gray")
show_ref_4.place(x=220,y=531)
valore_comma_IM = IntVar()
#show_ref_4 = Checkbutton(root, variable=valore_comma_IM, text="Show Imagery Ref. (only for 2018)",font=("Helvetica",8),fg="gray")
#show_ref_4.place(x=220,y=555)
# 1 = clicked
# 0 = not clicked
refresh_button = Button(root, text="Refresh", command=refresh)
refresh_button.place(x=440,y=560)
sel_all_button = Button(root, text="Selelct all", command=sel_all)
sel_all_button.place(x=440,y=500)
refresh_button_2 = Button(root, text="Deselect all", command=des_all)
refresh_button_2.place(x=440,y=530)
refresh_button_2 = Button(root, text="Refresh", command=refresh_2)
refresh_button_2.place(x=1040,y=560)
sel_all_button = Button(root, text="Selelct all", command=sel_all2)
sel_all_button.place(x=1040,y=500)
refresh_button_2 = Button(root, text="Deselect all", command=des_all2)
refresh_button_2.place(x=1040,y=530)
my_label_2=Label(root, text="Model 1",font=("Helvetica",14),fg="blue")
my_label_2.grid(row = 6, column = 1,  pady = 2)
my_entry_2=Entry(root,font=("Helvetica",20))
my_entry_2.grid(row = 7, column = 1,  pady = 2,padx=20)
my_list_2=Listbox(root,width=50,height=5)
my_list_2.grid(row = 8, column = 1,  pady = 2)
my_list_2.bind("<<ListboxSelect>>",fillout2)
update2(models)
my_entry_2.bind("<KeyRelease>",check2)
enter_button = Button(root, text="Single region/nation", command=single_models)
enter_button.grid(row = 12, column = 1, pady = 2)
### start two models
info=Label(root)
info.grid(row = 17, column = 1,  pady = 2)

info=Label(root, text="\nDescription of the Models:",font=("Helvetica",12,'bold'),fg="Red")
info.grid(row = 18, column = 1,  pady = 2)
info_expl=info0="Price: use the price data without taking into account the Market factor (MF) of the nation.\nPrice_MF: uses the price data and takes into account the market factor (MF) size.           \nWeight: use the weight data                                                                                                \nThe modelS withouth the label _max use mainly direct data and fill gaps with Mirror data.\nThe models with _max label use always a Mirror and Direct data combination if possible."
info0=Label(root, text=info_expl,font=("Helvetica",8),fg="black",justify="left")
info0.grid(row = 19, column = 1,  pady = 2)
my_label_0=Label(root, text="Region",font=("Helvetica",14),fg="purple")
my_label_0.grid(row = 0, column = 2,  pady = 2,columnspan = 1)
my_entry_0=Entry(root,font=("Helvetica",20))
my_entry_0.grid(row = 1, column = 2,  pady = 2,columnspan = 1)
my_list_0=Listbox(root,width=50,height=5)
my_list_0.grid(row = 2, column = 2,  pady = 2,columnspan = 1)
update0(regions)
my_list_0.bind("<<ListboxSelect>>",fillout0)
my_entry_0.bind("<KeyRelease>",check0)
my_label_4=Label(root, text="Nation 2 ",font=("Helvetica",14),fg="green")
my_label_4.grid(row = 3, column = 1,  pady = 2)
my_entry_4=Entry(root,font=("Helvetica",20))
my_entry_4.grid(row = 4, column = 1,  pady = 2)
my_list_4=Listbox(root,width=50,height=5)
my_list_4.grid(row = 5, column = 1,  pady = 2)
update4(nations)
##Create a binding on the list box ###
my_list_4.bind("<<ListboxSelect>>",fillout4)
##Create a binding on the entry box ###
my_entry_4.bind("<KeyRelease>",check4)
my_label_7=Label(root, text="Region 2 ",font=("Helvetica",14),fg="Purple")
my_label_7.grid(row =3 , column = 2,  pady = 2,columnspan = 1)
my_entry_7=Entry(root,font=("Helvetica",20))
my_entry_7.grid(row = 4, column = 2,  pady = 2,columnspan = 1)
my_list_7=Listbox(root,width=50,height=5)
my_list_7.grid(row = 5, column = 2,  pady = 2,columnspan = 1)
regions=["Africa","Asia","Central America","Eurasia","Europe","Middle East","North America","Oceania","Ref. country","South America","World"]
update7(regions)
my_list_7.bind("<<ListboxSelect>>",fillout7)
my_entry_7.bind("<KeyRelease>",check7)
my_label_5=Label(root, text="Model 2 for comparison",font=("Helvetica",14),fg="blue")
my_label_5.grid(row = 6, column = 2,  pady = 2)
my_entry_5=Entry(root,font=("Helvetica",20))
my_entry_5.grid(row = 7, column = 2,  pady = 2)
my_list_5=Listbox(root,width=50,height=5)
my_list_5.grid(row = 8, column = 2,  pady = 2)
my_list_5.bind("<<ListboxSelect>>",fillout5)
#models=["NJORD-Weight","NJORD-Price","NJORD-Combined","Price","Price_MF","Price_max","Weight"]
my_entry_5.bind("<KeyRelease>",check5)
update5(models)
enter_button_2 = Button(root, text="Comparison of 2 models", command=model_comparison)
enter_button_2.grid(row = 12, column = 2, pady = 0,columnspan = 1)
enter_button_3 = Button(root, text="Comparison of 2 regions/nations ", command=nations_comparison)
enter_button_3.grid(row = 13, column = 2, pady = 0,columnspan = 1)
model_explaination="Single region/nation: show the predicted installed capacity [MW] with the model selected in Single model.\nTo display the data for a nation, the region space has to be empty.\nComparison of two models: compare the result obtained with two models (Model 1 and 2) for the same region/nation\n\n"
info1=Label(root, text="\nDescription of the Functions:",font=("Helvetica",12,'bold'),fg="red")
info1.grid(row = 17, column = 2,  pady = 2)
info2=Label(root, text=model_explaination,font=("Helvetica",8),fg="black",justify="left",textvariable=True,relief="flat")
info2.grid(row = 18, column = 2,  pady = 2)

root.mainloop()