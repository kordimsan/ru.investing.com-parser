import json 
from pprint import pprint
import threading
from threading import Thread

from my_parser import read_sqlite_table, InvestingParse

result: list

def resolve_instrument_list(ilst: list):
    print(ilst)
    browser = InvestingParse()
    browser._request_get('https://ru.investing.com/')
    for i in ilst:
        instrument_name = i[0]
        url = browser.get_instrument_url(instrument_name)
        if url:
            browser._request_get(url)
            per = browser.get_div_percent('Дивиденды')
            result.append((instrument_name,per))

def slice_list(lst, n):
    d = len(lst) // n + (len(lst) % n > 0)
    for i in range(0, len(lst), d):
        yield lst[i:i + d]


if __name__ == '__main__':

    with open('report.json', 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    result = []

    gen = slice_list(report, 4)
    
    threads = []
    for ilst in gen:
        th = Thread(target=resolve_instrument_list, args=(ilst,))
        th.start()
        threads.append(th)
    
    for th in threads:
        th.join()

    pprint(result)


