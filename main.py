import re
from site_parser import MyHTMLParser
import requests
import json
import schedule
import time
import telegram_bot

id_list = [106]  # , 101, 149, 128, 142, 145, 146, 134]
fuels = {}


def get_fuel_info(azs_list_json: dict):
    for azs in azs_list_json["data"]:
        if azs["id"] in id_list:
            print("=" * 22)
            print(azs["FullName"])
            print(azs["Address"])
            print("-" * 22)
            for fuel in azs["FuelsAsArray"]:
                print("{:<16} {}".format(fuel["Title"], fuel["Price"]))
            print("=" * 22)


def check_fuel():
    url = 'https://upg.ua/merezha_azs/'
    r = requests.get(url)
    content = r.content.decode()
    parser = MyHTMLParser()
    parser.feed(content)
    parsed_content = parser.get_content()
    azs_list = re.sub(r';$', '', parsed_content[0].strip().replace("var objmap = ", ""))
    azs_list_json = json.loads(azs_list)

    for azs in azs_list_json["data"]:
        if azs["id"] in id_list:
            for fuel in azs["FuelsAsArray"]:
                if fuel["id"] == 9:
                    if fuels.get(azs["id"]) != fuel["Price"]:
                        telegram_bot.send_msg(msg=f'UPG changed fuel on '
                                                  f'{azs["FullName"]}\n'
                                                  f'{azs["Address"]}\n'
                                                  f'{fuel["Title"]} -- {fuel["Price"]}')
                        get_fuel_info(azs_list_json=azs_list_json)
                    fuels[azs["id"]] = fuel["Price"]


telegram_bot.start_bot()

schedule.every(5).minutes.do(check_fuel)
while True:
    schedule.run_pending()
    time.sleep(1)
