# -*- coding: utf-8 -*-
from behave import *
from selenium import webdriver
import time

option = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'images':2, 'javascript':2}}
option.add_experimental_option('prefs', prefs)

class TextNotFound(Exception):
    pass

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