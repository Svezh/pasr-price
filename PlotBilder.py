# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 08:31:33 2022

@author: 79252
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None


def PlotBilder(ref):
    if ref == "5E 650i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5E_650i_ref.csv', sep=','))
    elif ref == "5E 850i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5E_850i_ref.csv', sep=','))
    elif ref == "5E 1000i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5E_1000i_ref.csv', sep=','))
    elif ref == "5E 1500i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5E_1500i_ref.csv', sep=','))
    elif ref == "5P 650IR":
        df_ref = pd.DataFrame(pd.read_csv('refs/5P_650IR_ref.csv', sep=','))
    elif ref == "5P 850IR":
        df_ref = pd.DataFrame(pd.read_csv('refs/5P_850IR_ref.csv', sep=','))
    elif ref == "5P 1150I":
        df_ref = pd.DataFrame(pd.read_csv('refs/5P_1150i_ref.csv', sep=','))
    elif ref == "5SC 500i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5SC_500i_ref.csv', sep=','))
    elif ref == "5SC 750i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5SC_750i_ref.csv', sep=','))
    elif ref == "5SC 1000i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5SC_1000i_ref.csv', sep=','))
    elif ref == "5E 500i":
        df_ref = pd.DataFrame(pd.read_csv('refs/5SC_500i_ref.csv', sep=','))

    df_xcm = pd.DataFrame(pd.read_csv('database_xcom_make.csv'))
    df_stl = pd.DataFrame(pd.read_csv('database_stl_make.csv'))

 

    def converter(converting_df,df_ref):
        for i in range(int(len(converting_df['Model']))):
            converting_df['Model'][i] = converting_df['Model'][i].replace('-', '')
            converting_df['Model'][i] = converting_df['Model'][i].replace(' ', '')
            converting_df['Model'][i] = converting_df['Model'][i].upper()

        converting_df = converting_df.replace(np.nan, '0', regex=True)
        converting_df = converting_df.fillna('0')
        df_comp = converting_df.loc[(converting_df['Model'].isin(df_ref['ART_Model'])) | (converting_df['Model'].isin(df_ref['Name_Model']))]

        mask = df_comp.duplicated(subset=['Model', 'Date', 'Time'])
        df_comp = df_comp.loc[~mask]
        df_comp.reset_index(drop=True, inplace=True)
        df_comp['Current_Price'] = df_comp['Current_Price'].astype(int)
        return df_comp



    def checker_rule(df_for_check):

        checker_1 = []
        checker_min = []
        checker_max = []
        date=[]
        del_date=[]
        del_time = []
        a=[]


        dict_group=df_for_check.groupby(by=['Time', 'Date']).groups

        date=[*dict_group]


        for i in range(int(len(date))):
            if date[i][0] == date[i - 1][0]:
                checker_min.append(date[i])
                checker_max.append(date[i - 1])

        checker = list(set(checker_min + checker_max))

        for i in range(int(len(checker))):
            if checker[i] != max(checker):
                checker_1.append(checker[i])


        for i in range(int(len(checker_1))):
            del_time.append(checker_1[i][1])
            del_date.append(checker_1[i][0])
            a.append(dict_group.get(checker[i]))


        for i in range(len(a)):
            df_res = df_for_check.drop(index=a[i])

        return df_res





    df_comp=converter(df_xcm,df_ref)
    df_comp_cit=converter(df_stl,df_ref)

    df_comp = checker_rule(df_comp)
    df_comp_cit = checker_rule(df_comp_cit)
    df_comp_cit.reset_index(drop=True, inplace=True)
    df_comp.reset_index(drop=True, inplace=True)








    df_ref_xcm = df_ref.loc[
        (df_ref['ART_Model'].isin(df_comp['Model'])) | (df_ref['Name_Model'].isin(df_comp['Model']))]
    df_ref_xcm.reset_index(drop=True, inplace=True)
    df_ref_cit = df_ref.loc[
        (df_ref['ART_Model'].isin(df_comp_cit['Model'])) | (df_ref['Name_Model'].isin(df_comp_cit['Model']))]
    df_ref_cit.reset_index(drop=True, inplace=True)

    fig, ax = plt.subplots(2, 1)
    ###Проверка на заполненность датафрема проверки
    if df_comp_cit.empty:
        ax[1].plot(0, 0, label="нет совпадений по референсам")
    else:

        annotate_mass_x_cit = []
        annotate_mass_y_cit = []

        ###Создается массив для аннотаций annotatr_mass_x(y)_cit для магазина citilink.ru
        ###Представляет собой координаты для графика надо точками, чтобы указывать цены в точке
        for i in range(int(len(df_comp_cit['Current_Price']))):
            for j in range(int(len(df_ref_cit))):
                if (df_comp_cit['Model'][i] == df_ref_cit['ART_Model'][j]) or (
                        df_comp_cit['Model'][i] == df_ref_cit['Name_Model'][j]):
                    annotate_mass_x_cit.append(df_comp_cit['Time'][i])

                    annotate_mass_y_cit.append(df_comp_cit['Current_Price'][i])

        for j in range(int(len(df_ref_cit['ART_Model']))):
            label = df_comp_cit['Model'][j] + " " + df_comp_cit['Vendor'][j]
            lebelno = df_comp_cit['Model'][j] + " " + df_comp_cit['Vendor'][j] + "Eaton no"
            data_x = df_comp_cit['Time'].loc[(df_comp_cit['Model'] == df_ref_cit['Name_Model'][j]) | (
                        df_comp_cit['Model'] == df_ref_cit['ART_Model'][j])]
            data_y = df_comp_cit['Current_Price'].loc[(df_comp_cit['Model'] == df_ref_cit['Name_Model'][j]) | (
                        df_comp_cit['Model'] == df_ref_cit['ART_Model'][j])]
            ax[1].plot(data_x, data_y, '.-', label=label, linewidth=2)

            data_label_cit = {'x': annotate_mass_x_cit, 'y': annotate_mass_y_cit}
            df_label_cit = pd.DataFrame(data_label_cit)
            df_label_cit.reset_index(drop=True, inplace=True)

        for i in range(int(len(df_label_cit['x']))):
            ax[1].text(df_label_cit['x'][i], df_label_cit['y'][i], str(df_label_cit['y'][i]), fontsize=7)

            ax[1].set_title("Динамика цен Citilink.ru", fontsize=15)
            ax[1].set_ylabel("Цена (₽)", fontsize=15)
            plt.xticks(rotation=35)

            ax[1].grid(which='major', color='k',
                       linewidth=0.5
                       )

            ax[1].minorticks_on()

            ax[1].grid(which='minor', color='grey',
                       linewidth=0.5,
                       linestyle=':')

    if df_comp.empty:
        ax[0].plot(0, 0, label="нет совпадений по референсам")
    else:

        annotate_mass_x = []
        annotate_mass_y = []

        for i in range(int(len(df_comp['Current_Price']))):
            for j in range(int(len(df_ref_xcm))):
                if df_comp['Model'][i] == df_ref_xcm['ART_Model'][j]:
                    annotate_mass_x.append(df_comp['Time'][i])
                    annotate_mass_y.append(df_comp['Current_Price'][i])

        for i in range(int(len(df_ref_xcm['ART_Model']))):
            label = df_comp['Model'][i] + " " + df_comp['Vendor'][i]

            ax[0].plot(df_comp['Time'].loc[df_comp['Model'] == df_ref_xcm['ART_Model'][i]],
                       df_comp['Current_Price'].loc[df_comp['Model'] == df_ref_xcm['ART_Model'][i]], '.-', label=label,
                       linewidth=2)

            data_label = {'x': annotate_mass_x, 'y': annotate_mass_y}
            df_label = pd.DataFrame(data_label)
            df_label.reset_index(drop=True, inplace=True)

        for i in range(int(len(df_label['x']))):
            ax[0].text(df_label['x'][i], df_label['y'][i], str(df_label['y'][i]), fontsize=7)
            ax[0].set_title("Динамика цен Xcom-shop.ru", fontsize=15)
            ax[0].set_ylabel("Цена (₽)", fontsize=15)
            plt.xticks(rotation=35)

            ax[0].grid(which='major', color='k',
                       linewidth=0.5
                       )

            ax[0].minorticks_on()

            ax[0].grid(which='minor', color='grey',
                       linewidth=0.5,
                       linestyle=':')

    ax[0].legend()
    ax[1].legend()

    plt.show()
