# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:25:22 2022

@author: 79252
"""
# Data processor module (DPM) creates and supplements the database
# based on the results of site parsing

# Модуль обработки данных созадет базу данных
# и добавляет в нее резельтаты парсинга сайта

import pandas as pd
from _NPM_XC import main_pars_xcom
import datetime
from Frame_input_data import create_csv_PQ
import openpyxl as opn

# from Frame_input_data import create_csv_PQ
def main_xcom():

    list_name_xcom, list_price_xcom = main_pars_xcom('https://www.xcom-shop.ru/catalog/ibp/istochniki_bespereboynogo_pitaniya/', 77)
    
    dt_obj =datetime.datetime.now()
    date_now = dt_obj.strftime("%d.%m.%Y")  # переменная определяющая время обработки парсером
    time_now= dt_obj.strftime("%H:%M:%S")  # переменная определяющая время обработки парсером
    data_input_new_xcom = {
        'Name': list_name_xcom,
        'Current_Price': list_price_xcom,
        'Time': date_now,
        'Date':time_now}


    df_raw_xcom = pd.DataFrame(data_input_new_xcom)
    df_raw_xcom['Current_Price']= df_raw_xcom['Current_Price'].replace('₽','',regex=True)
    df_raw_xcom['Current_Price']= df_raw_xcom['Current_Price'].replace(' ','',regex=True)
    #df_raw_xcom['Current_Price']=pd.to_numeric(df_raw_xcom['Current_Price'])
# формирование csv файла представляющего общую, обновляемую базу данных

    df_raw_xcom.to_csv('database_raw_xcom', mode='a', index=False, sep=",")

# датафрейм с обновленной информацией по базе сформирванной базе данных

    df_upd_xcom = pd.read_csv('database_raw_xcom', sep=',')
    df_input_data, df_input_data_xcom, xcom_list_vendor_check, xcom_list_model_check = create_csv_PQ()
    check_xcom_df = pd.read_csv('database_xcom',sep=',')
    #сheck_xcom_df = pd.read_csv('database_xcom', sep=',')




# Функция обновления базы данных
    def create_data_base():

        list_model_xcom = []
        list_vendor_xcom = []
        price_list = []
        time_list=[]
        date_list=[]

        lengh_xcom = int(len(df_upd_xcom['Name']))

        for j in range(int(lengh_xcom)):
            for k in range(int(len(check_xcom_df['Vendor']))):
                if check_xcom_df['Vendor'][k] in df_upd_xcom['Name'][j]:
                    list_vendor_xcom.append(check_xcom_df['Vendor'][k])
                    list_model_xcom.append(df_upd_xcom['Name'][j][xcom_list_model_check[k]:])
                    price_list.append(df_upd_xcom['Current_Price'][j])
                    time_list.append(df_upd_xcom['Time'][j])
                    date_list.append(df_upd_xcom['Date'][j])
                

        data_input_final_xcom = {
            'Vendor':list_vendor_xcom,
            'Model':list_model_xcom,
            'Current_Price': price_list,
            'Time': time_list,
            'Date':date_list
        }

        df_raw_2_xcom = pd.DataFrame(data_input_final_xcom)
       # df_final = df_raw_2_xcom.join(df_upd_xcom.drop(columns=('Name'),axis=1))
        df_raw_2_xcom.to_csv('database_xcom_make.csv',sep=',')
        #df_raw_2_xcom.to_excel('test_database.xlsx')



    create_data_base()
