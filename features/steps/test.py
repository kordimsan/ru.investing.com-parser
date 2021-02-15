# -*- coding: utf-8 -*-
import locale
import sqlite3
import time
from pprint import pprint

from behave import *
from selenium import webdriver

locale.setlocale(locale.LC_ALL, 'nl_NL')

option = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images':2, 'javascript':2}}
option.add_experimental_option('prefs', prefs)

class TextNotFound(Exception):
    pass

def read_sqlite_table(base_path):
    try:
        sqlite_connection= sqlite3.connect(base_path, timeout=20)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * from stock_price"""
        cursor.execute(sqlite_select_query)
        rows = cursor.fetchall()
        return rows
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


@given('Запущен драйвер chromedriver')
def step(context):
    context.browser = webdriver.Chrome("C:\\chromedriver.exe", options=option)

@then("Переходим по адресу '{url}'")
def step(context, url):
    context.browser.get(url)

@then("Переходим в меню '{text}'")
def step(context, text):
    menu = context.browser.find_element_by_xpath(f"//a[contains(text(),'{text}')]")
    link = menu.get_attribute('href')
    context.browser.get(link)

@then("Проверяем заголовок по имени '{name}'")
def step(context, name):
    elements = context.browser.find_elements_by_xpath("//section[@id='leftColumn']//h1")
    if not elements[0].get_attribute('innerText') == name:
        raise TextNotFound("Не найден заголовок '{name}'")

@then("Получаем таблицу с котировками с сайта")
def step(context):
    elements = context.browser.find_elements_by_xpath("//table[@id='cross_rate_markets_stocks_1']//tbody//tr")
    data = []
    for tr in elements:
        tds = tr.find_elements_by_tag_name('td')
        if tds: 
            data.append((tds[1].text,tds[2].text))
    context.data = [(a,locale.atof(b)) for a,b in data]

@then("Получаем таблицу с котировками из базы '{base_path}'")
def step(context, base_path):
    stock_price = read_sqlite_table(base_path)
    context.stock_price = [(a,locale.atof(b)) for a,b in stock_price]

@then("Получаем таблицу котировок цена которых изменилась на {per}%")
def step(context, per):
    result = [(a,b,dict(context.stock_price).get(a)) for a, b in context.data if (b/dict(context.stock_price).get(a,b)-1)*100 >= int(per)]
    pprint(result)
