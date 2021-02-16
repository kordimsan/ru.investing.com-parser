from my_parser import read_sqlite_table, InvestingParse
from pprint import pprint
import json

if __name__ == '__main__':
  stock_price = read_sqlite_table('stocks') #метод достающий цены из базы
  browser = InvestingParse() #инициализация браузера
  browser._request_get('https://ru.investing.com/') #переход на сайт
  data = browser.get_first_report() #получение таблицы цен из браузера
  per = 50 #указываем размер процентов роста бумаги которые необходимо включить в отчет
  result = [(a,b,dict(stock_price).get(a)) for a, b in data if (b/dict(stock_price).get(a,b)-1)*100 >= int(per)] #Фильтруем данные полученные из браузера
  with open('report.json', 'w', encoding='utf8') as f: #сохраняем результат
    json.dump(result, f, ensure_ascii=False,indent=2)
