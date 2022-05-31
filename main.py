import re
from html.parser import HTMLParser
import requests
import json

url = 'https://upg.ua/merezha_azs/'
r = requests.get(url)
content = r.content.decode()


class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        if re.search(r'var objmap', data):
            finded_all = data.split("\n")
            for finded in finded_all:
                if re.search(r'var objmap', finded):
                    all.append(finded)


parser = MyHTMLParser()
all = []
parser.feed(content)

azs_list = re.sub(r';$', '', all[0].strip().replace("var objmap = ", ""))

azs_list_json = json.loads(azs_list)

for azs in azs_list_json["data"]:
    if azs["id"] == 106:
        print("=" * 22)
        print(azs["FullName"])
        print(azs["Address"])
        print("-" * 22)
        for fuel in azs["FuelsAsArray"]:
            print("{:<16} {}".format(fuel["Title"], fuel["Price"]))
        print("=" * 22)
