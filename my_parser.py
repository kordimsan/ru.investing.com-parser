import locale
import sqlite3
import time
from pprint import pprint
from typing import Mapping

from selenium import webdriver

def float_de_de(str: str) -> float:
  return float(str.replace('.','').replace(',','.'))


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

  def __init__(self) -> None:
    self.browser = webdriver.Chrome('C:\chromedriver.exe', options=self._option)
    
  def _request_get(self, url: str):
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

  def _get_reports(self):
    self._get_menu('Акции')
    self._get_menu('Россия')
    if self._is_target('Россия - акции'):
      elements = self.browser.find_elements_by_xpath("//table[@id='cross_rate_markets_stocks_1']//tbody//tr")
      for tr in elements:
        tds = tr.find_elements_by_tag_name('td')
        if tds: 
          yield tds
                
  def get_first_report(self):
    data = []
    for tds in self._get_reports():
      data.append((tds[1].text,tds[2].text))
    return [(a,float_de_de(b)) for a,b in data]

  def get_instrument_url(self, instrument_name: str):
    data = []
    for tds in self._get_reports():
      data.append((tds[1].text,tds[1].find_elements_by_tag_name('a')[0].get_attribute('href')))
    return dict(data).get(instrument_name)

  def get_div_percent(self, indicator: str):
    elements = self.browser.find_elements_by_xpath("//*[@id='leftColumn']//div[@class='inlineblock']")
    for elm in elements:
        spn1 = elm.find_elements_by_class_name('float_lang_base_1')
        spn2 = elm.find_elements_by_class_name('float_lang_base_2')
        if spn1 and spn2:
            if spn1[0].text == indicator: 
                return spn2[0].text.split('(')[1][:-1]