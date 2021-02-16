# -*- coding: utf-8 -*-
import time
from pprint import pprint
import my_parser as parser
from behave import *

class TextNotFound(Exception):
    pass

@given("Переходим по адресу '{url}'")
def step(context, url):
    context.browser = parser.InvestingParse()
    context.browser._request_get(url)

@then("Переходим в меню '{text}'")
def step(context, text):
    context.browser._get_menu(text)

@then("Проверяем заголовок по имени '{name}'")
def step(context, name):
    if not context.browser._is_target(name):
        raise TextNotFound("Не найден заголовок '{name}'")

@then("Получаем таблицу с котировками с сайта")
def step(context):
    context.data = context.browser.get_first_report()

@then("Получаем таблицу с котировками из базы '{base_path}'")
def step(context, base_path):
    context.stock_price = parser.read_sqlite_table(base_path)

@then("Получаем таблицу котировок цена которых изменилась на {per}%")
def step(context, per):
    result = [(a,b,dict(context.stock_price).get(a)) for a, b in context.data if (b/dict(context.stock_price).get(a,b)-1)*100 >= int(per)]
    pprint(result)
