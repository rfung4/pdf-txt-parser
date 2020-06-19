import json
import urllib.request
from bs4 import BeautifulSoup
import re
import os

url = 'https://www.apple.com/newsroom/2020/04/apple-reports-second-quarter-results/'

reg_map = {
    'Quarterly revenue': re.compile('quarterly revenue of \\$[0-9]+\\.?[0-9]? billion'),
    'Earnings per share': re.compile('earnings per diluted share of \\$[0-9]+\\.?[0-9]+'),
    'Operating Cashflow': re.compile('operating cash flow of \\$[0-9]+\\.?[0-9]? billion')
}


html_headers = {'User-Agent': 'Mozilla/5.0'
                              'KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive'}


def make_soup(input_url):
    req = urllib.request.Request(input_url, headers=html_headers)
    return BeautifulSoup(urllib.request.urlopen(req).read(), "lxml")


def run():
    print("Initalizing Apple Parser..")
    print(f"Creating page soup from {url}\n")
    soup = make_soup(url)
    full_txt = "\n".join([s.text.strip() for s in soup.findAll('div', class_='pagebody-copy')])
    results = {}

    for label, regex in reg_map.items():
        res = regex.search(full_txt)
        results[label] = " ".join([i for i in res.group(0).split(" ") if "$" in i or i == 'billion'])
        print(f"Parsing {label} : {results[label]}")

    with open('apple_results.json', 'w') as fp:
        json.dump(results, fp)

    output = f'{os.path.dirname(os.path.abspath(__file__))}\{"apple_results.json"}'
    print(f"\nExecution complete, output written to: {output}")


if __name__ == '__main__':
    run()