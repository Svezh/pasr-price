# -*- coding: utf-8 -*-
"""
@author: /Svezh
"""
# Net parsing module (NPM) performs site parsing by UPS category

# Модуль веб парсинга осуществляет парсинг сайта по категории ИБП

import requests
from bs4 import BeautifulSoup

list_name_xcom = []
list_price_xcom = []

def xcom_categories(url):
    response = requests.get(url)
    exit_soup = BeautifulSoup(response.text, 'html.parser')
    return exit_soup


def token_take_xcom(tag_el1, tag_el2, soup):
    exit_list = []
    token_soup = soup.find_all('div',
                                    class_='catalog_item__inner catalog_item__inner--tiles')
    for elements in token_soup:
        check_data = elements.find('div',
                                        class_='catalog_item__type catalog_item__type--tiles').text

        if check_data == "Источник бесперебойного питания":
            simbol_data = elements.find(tag_el1, class_=tag_el2)

            if simbol_data != None:
                exit_list.append(simbol_data.get_text(strip=True))
            else:
                exit_list.append('NaN')
    return exit_list


def parsing_xcom(soup):
    list_name_xcom.extend(token_take_xcom('a',
                                                'catalog_item__name catalog_item__name--tiles', soup))
    list_price_xcom.extend(token_take_xcom('div', 
                                                'catalog_item__new_price', soup))
    return list_name_xcom, list_price_xcom


def main_pars_xcom(url, pages):
    for i in range(int(pages)):
        if i == 0:
            soup = xcom_categories(url)
            list_name_xcom, list_price_xcom = parsing_xcom(soup)
            print("Страница", i + 1, "на сайте xcom-shop.ru обработана")
        else:
            soup = xcom_categories(url + '/?list_page=' + str(i + 1))
            list_name_xcom, list_price_xcom = parsing_xcom(soup)
            print("Страница", i + 1, "на сайте xcom-shop.ru обработана")
    return list_name_xcom, list_price_xcom


