from html.parser import HTMLParser
import re
import requests
import json


class MyHTMLParser(HTMLParser):
    content = []

    def handle_data(self, data):
        if re.search(r'var objmap', data):
            finded_all = data.split("\n")
            for finded in finded_all:
                if re.search(r'var objmap', finded):
                    self.content.append(finded)

    def get_content(self) -> list:
        return self.content

    def get_azs(self) -> dict:
        url = 'https://upg.ua/merezha_azs/'
        r = requests.get(url)
        content = r.content.decode()
        parser = MyHTMLParser()
        parser.feed(content)
        parsed_content = parser.get_content()
        azs_list = re.sub(r';$', '', parsed_content[0].strip().replace("var objmap = ", ""))
        azs_list_json = json.loads(azs_list)
        return azs_list_json
