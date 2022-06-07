from html.parser import HTMLParser
import re


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
