# -*- coding: utf-8 -*-
"""
@author: /Svezh
"""
#Net parsing module (NPM) performs site parsing by UPS category

#Модуль веб парсинга осуществляет парсинг сайта по категории ИБП

import requests
from bs4 import BeautifulSoup


list_name=[]
list_price=[]
list_current_price=[]
list_raiting=[]
list_review=[]
list_of_ref = []



#отладочная функция для сохранения логов
def save_log(data_in):

    file=open('url_log','wb')
    file.write(data_in)
    file.close()
    return print("logged")

#фуция для определения конкретных значений тегов (Имя товара, цена,отзывы,рейтинг и т.д)
def token_take (tag_el1,tag_el2,soup):

    exit_list=[]  # выходной лист значений конкретных тегов
    token_soup= soup.find_all('div',class_ ='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')
    for element in token_soup:
        simbol_data=element.find(tag_el1,class_=tag_el2)
        if simbol_data != None: # проверка на наличие тега в дереве (если такового тега нет, то пишем в выходные данные None)
               
            exit_list.append(simbol_data.get_text(strip=True))
        else:
            exit_list.append("None")
    return exit_list



def token_take_int (tag_el1,tag_el2,soup):

    exit_list=[]  # выходной лист значений конкретных тегов
    token_soup= soup.find_all('div',class_ ='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')
    for element in token_soup:
        simbol_data=element.find(tag_el1,class_=tag_el2)
        if simbol_data != None: # проверка на наличие тега в дереве (если такового тега нет, то пишем в выходные данные None)		     
            exit_list.append(int(simbol_data.get_text(strip=True).replace(" ","")))                     
        else:
            exit_list.append("NaN")
    return exit_list


#функция для проверки на рейтинг и отзывы
def token_take_icons(tag_el1,tag_el2,soup):

    exit_list_raiting=[]
    exit_list_review=[]
    Headliner_soup = soup.find_all('div',class_ ='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')
    for soups in Headliner_soup:
        check_anavabled_soup= soups.find_all('div',class_ ='ProductCardHorizontal__icons')
        check_no_anavable_soup = soups.find('div',class_='ProductCardHorizontal__no-ratings')

        if check_no_anavable_soup != None:
            exit_list_review.append("NaN")
            exit_list_raiting.append("NaN")
        else:
            for elements in check_anavabled_soup:
                simbol_data_raiting=elements.find_all(tag_el1,class_=tag_el2)[0]
                simbol_data_review=elements.find_all(tag_el1,class_=tag_el2)[1]
                if simbol_data_raiting != None: # проверка на наличие тега в дереве (если такового тега нет, то пишем в выходные данные None)
            
                    exit_list_raiting.append(simbol_data_raiting.get_text(strip=True))
                else:
                    exit_list_raiting.append("NaN")

                if simbol_data_review != None: # проверка на наличие тега в дереве (если такового тега нет, то пишем в выходные данные None)
            
                    exit_list_review.append(simbol_data_review.get_text(strip=True))
                else:
                    exit_list_review.append("NaN")

    return exit_list_raiting,exit_list_review


#функция для перехода по категорям товаров в катклоге магазина
def citilink_categories(core_url):
    #взятие ссылки на катклог товаров с главной страницы сайта (link_catalog)
    response_catalog=requests.get(core_url)
    soup_catalog =BeautifulSoup(response_catalog.text,'html.parser')
    link_catalog=soup_catalog.find('div', class_ = 'MainHeader__catalog').find('a',class_='Link js--Link Link_type_icon js--Link_not-drag-and-drop')['href']
    #взятие ссылки на категорию "защита питания" на странице каталога товаров (sublink)
    response_catalog_1 =requests.get(link_catalog)
    soup_catalog = BeautifulSoup(response_catalog_1.text,'html.parser')
    li=soup_catalog.find_all('li',{'class':'CatalogLayout__item-list'})[1]
    children = li.findChildren('a')
    for child in children:
        if child.get_text(strip=True) == "Защита питания":
            sublink=child.get('href')
    #взятие ссылки на категорию "источники бесперебойного питания" (USP_link)        
    response_subcatalog=requests.get(sublink)
    soup_subcatalog=BeautifulSoup(response_subcatalog.text,'html.parser')
    div=soup_subcatalog.find_all('div',class_='CatalogCategoryCardWrapper__item-flex')[3]
    children = div.findChildren('a')
    for child in children:
        if child.get_text(strip=True)=="Источники бесперебойного питания":
            USP_link=child.get('href')
    return USP_link


#Функция для взятия ссылки на следующую страницу в категории товара
def next_page(soup):
    soup_page=soup.find_all('div',class_='PaginationWidget__wrapper-pagination')

    for child in soup_page:
        a_child=child.find('a',class_='PaginationWidget__page js--PaginationWidget__page PaginationWidget__page_next PaginationWidget__page-link')['href']
    return a_child


#Функция парсинга товаров в каталоге.
def parsing (soup):


    list_name.extend(token_take('a','ProductCardHorizontal__title',soup))
    list_price.extend(token_take_int('span','ProductCardHorizontal__price_current-price',soup))
    list_current_price.extend(token_take_int('span','_current-price js--_current-price',soup))
    lits_raiting_raw,list_review_raw=token_take_icons('span','ProductCardHorizontal__count IconWithCount__count js--IconWithCount__count',soup)
    list_raiting.extend(lits_raiting_raw)
    list_review.extend(list_review_raw)
    return list_name,list_price,list_current_price,list_raiting,list_review


###MAIN_FUNC###
def main_pars(url,pages):
    i=0
    for i in range(int(pages)):
        if i==0:
            response=requests.get(citilink_categories(url))
            soup = BeautifulSoup(response.text,'html.parser')
            parsing(soup)
            print("Страница",i+1,"на сайте Sitilink.ru обработана")
            i=i+1
        else:
            new_soup=next_page(soup)
            response=requests.get(new_soup)
            soup= BeautifulSoup(response.text,'html.parser')
            parsing(soup)
            print("Страница",i+1,"на сайте Sitilink.ru обработана")
            i=i+1
    return list_name,list_price,list_current_price,list_raiting,list_review



