from my_parser import read_sqlite_table, InvestingParse
from pprint import pprint
import json

if __name__ == '__main__':
  stock_price = read_sqlite_table('stocks')
  browser = InvestingParse()
  browser._request_get('https://ru.investing.com/')
  data = browser.get_first_report()
  per = 50
  result = [(a,b,dict(stock_price).get(a)) for a, b in data if (b/dict(stock_price).get(a,b)-1)*100 >= int(per)]
  with open('report.json', 'w', encoding='utf8') as f:
    json.dump(result, f, ensure_ascii=False,indent=2)
