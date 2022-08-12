#модуль для сопоставления названия вендорра и предложеного названия во взятых данных
#убтрает название вендора из названия модели


import pandas as pd

def create_csv_PQ ():
	list_vendor=['ИБП Eaton','ИБП APC','ИБП Ippon','ИБП HIPER',
				'ИБП PowerCom','ИБП SUNWIND','ИБП Tripp Lite']# список значений для названия вендора на сайте sitilink.ru

	list_vendor_xcom=['APC','CyberPower','Defender','Dell','Delta',
					'DKC','Eaton','Energenie',
					'Hyperline','Ippon',
					'Most','Powercom','Power Cube',
					'Rexant','Sven','VCOM']# список значений для названия вендора на сайте x-com.ru
	list_model_xcom = []
	list_model=[]

	for i in range(int(len(list_vendor_xcom))):
		list_model_xcom.append(int(len(list_vendor_xcom[i])+1))# список значений количества символов, которые необходимо удалить из названия модели взятой с сайта x-com.ru

	for i in range(int(len(list_vendor))):
		list_model.append(int(len(list_vendor[i]) + 1))# список значений количества символов,которые необходимо удалить из названия модели на сайте x-com.ru

#датафрейм данных для сайта Sitilink.ru
	_data_PQ_={'Vendor':list_vendor,
				'Model':list_model
				}


#датафрейм данных для сайта x-com.ru
	_data_PQ_XCOM_={'Vendor':list_vendor_xcom,
					'Model':list_model_xcom
					}

					
	df_database_xcom=pd.DataFrame(_data_PQ_XCOM_)
	df_database=pd.DataFrame(_data_PQ_)
	df_database.to_csv('database',index=False,sep=',')
	df_ex=pd.read_csv('database',sep=',')

	df_database_xcom.to_csv('database_xcom',index=False,sep=',')
	df_ex_xcom=pd.read_csv('database_xcom',sep=',')

	return df_ex,df_ex_xcom,list_vendor_xcom,list_model_xcom




