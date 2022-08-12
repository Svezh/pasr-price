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
from _NPM_ import main_pars
import datetime
from Frame_input_data import create_csv_PQ

def main_sit():
    list_name, list_price, list_current_price, list_raiting, list_review = main_pars('https://www.citilink.ru/', '5')


    dt_obj =datetime.datetime.now()
   # dt_now = dt_obj.strftime("%d.%m.%Y %H:%M:%S")   # переменная определяющая время обработки парсером
    date_now = dt_obj.strftime("%d.%m.%Y")
    time_now = dt_obj.strftime("%H:%M:%S")
    data_input_new = {
        'Name': list_name,
        'Current_Price': list_price,
        'Old_price': list_current_price,
        'Time': date_now,
        'Date': time_now}




    df_raw = pd.DataFrame(data_input_new)

# формирование csv файла представляющего общую, обновляемую базу данных
    df_raw.to_csv('database_raw_stl', mode='a', index=False, sep=":")


# датафрейм с обновленной информацией по базе сформирванной базе данных
    df_upd = pd.read_csv('database_raw_stl', sep=':')
    df_input_data, df_input_data_xcom, xcom_list_vendor_check, xcom_list_model_check = create_csv_PQ()

# Функция обновления базы данных
    def create_data_base():
        list_vendor = []
        list_model = []


        length, wigth = df_upd.shape


        for i in range(length):

            if df_input_data['Vendor'][0] in df_upd['Name'][i]:
                list_vendor.append('Eaton')
                list_model.append(df_upd['Name'][i][10:])

            elif df_input_data['Vendor'][1] in df_upd['Name'][i]:
                list_vendor.append('APC')
                list_model.append(df_upd['Name'][i][8:])

            elif df_input_data['Vendor'][2] in df_upd['Name'][i]:
                list_vendor.append('Ippon')
                list_model.append(df_upd['Name'][i][10:])

            elif df_input_data['Vendor'][3] in df_upd['Name'][i]:
                list_vendor.append('HIPER')
                list_model.append(df_upd['Name'][i][10:])

            elif df_input_data['Vendor'][4] in df_upd['Name'][i]:
                list_vendor.append('PowerCom')
                list_model.append(df_upd['Name'][i][13:])

            elif df_input_data['Vendor'][5] in df_upd['Name'][i]:
                list_vendor.append('SUNWIND')
                list_model.append(df_upd['Name'][i][12:])
            elif df_input_data['Vendor'][6] in df_upd['Name'][i]:
                list_vendor.append('Tripp Lite')
                list_model.append(df_upd['Name'][i][15:])
            else:
                list_vendor.append(df_upd['Name'][i])
                list_model.append('None')


        data_input_final = {
            'Vendor': list_vendor,
            'Model': list_model
        }
        df_raw2 = pd.DataFrame(data_input_final)
        df_final = df_raw2.join(df_upd.drop(columns=('Name'), axis=1))
        df_final.to_csv('database_stl_make.csv',sep=',')
    create_data_base()
