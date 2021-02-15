from my_parser import read_sqlite_table, InvestingParse
from pprint import pprint

if __name__ == '__main__':
  stock_price = read_sqlite_table('stocks')
  data = InvestingParse('https://ru.investing.com/').get_prices()
  per = 50
  result = [(a,b,dict(stock_price).get(a)) for a, b in data if (b/dict(stock_price).get(a,b)-1)*100 >= int(per)]
  pprint(result)
