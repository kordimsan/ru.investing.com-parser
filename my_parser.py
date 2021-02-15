import locale
import sqlite3
import time
from pprint import pprint
from typing import Mapping

from selenium import webdriver

def float_de_de(str: str) -> float:
  return float(str.replace('.','').replace(',','.'))

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
        return [(a,float_de_de(b)) for a,b in rows]
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

class InvestingParse():
  _option = webdriver.ChromeOptions()
  _option.add_experimental_option('prefs', {'profile.default_content_setting_values': {'images':2, 'javascript':2}})

  def __init__(self, url) -> None:
    self.browser = webdriver.Safari()
    self.browser.get(url)

  def _get_menu(self, text: str):
    menu = self.browser.find_element_by_xpath(f"//a[contains(text(),'{text}')]")
    link = menu.get_attribute('href')
    self.browser.get(link)

  def _is_target(self, name: str):
    elements = self.browser.find_elements_by_xpath("//section[@id='leftColumn']//h1")
    if not elements[0].get_attribute('innerText') == name:
        raise TextNotFound("Не найден заголовок '{name}'")
    return True

  def get_report(self):
    self._get_menu('Акции')
    self._get_menu('Россия')
    if self._is_target('Россия - акции'):
      elements = self.browser.find_elements_by_xpath("//table[@id='cross_rate_markets_stocks_1']//tbody//tr")
      data = []
      for tr in elements:
          tds = tr.find_elements_by_tag_name('td')
          if tds: 
              data.append((tds[1].text,tds[2].text))
      return [(a,float_de_de(b)) for a,b in data]