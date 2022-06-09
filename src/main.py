from site_parser import MyHTMLParser
import schedule
import time
import telegram_bot
from orm import Orm

fuels = {}

# id_list = [106]  # , 101, 149, 128, 142, 145, 146, 134]
#
# def get_fuel_info(azs_list_json: dict):
#     for azs in azs_list_json["data"]:
#         if azs["id"] in id_list:
#             print("=" * 22)
#             print(azs["FullName"])
#             print(azs["Address"])
#             print("-" * 22)
#             for fuel in azs["FuelsAsArray"]:
#                 print("{:<16} {}".format(fuel["Title"], fuel["Price"]))
#             print("=" * 22)


def check_fuel():
    orm = Orm()
    azs_list_json = MyHTMLParser().get_azs()
    users = orm.get_users()
    notify = {}
    for azs in azs_list_json["data"]:
        notify_users = []
        for user in users:
            azs_list = orm.get_subscribed_azs(user_id=user[0])
            for a in azs_list:
                if a[0] == azs["id"]:
                    if not fuels.get(azs["id"]):
                        fuels[azs["id"]] = azs["FuelsAsArray"]
                        continue
                    for fuel in fuels[azs["id"]]:
                        for f in azs["FuelsAsArray"]:
                            if f["id"] == fuel["id"]:
                                if fuel["Price"] != f["Price"]:
                                    if user[0] not in notify_users:
                                        notify_users.append(user[0])
                                        notify[a[0]] = notify_users
                    fuels[azs["id"]] = azs["FuelsAsArray"]
    for azs in azs_list_json["data"]:
        for azs_id, users in notify.items():
            if azs["id"] == azs_id:
                prices = "\n".join([a["Title"] + " ---- " + a["Price"] for a in azs["FuelsAsArray"]])
                telegram_bot.send_msg(msg=f'{azs["FullName"]}\n{azs["Address"]}\n{prices}')


telegram_bot.start_bot()

schedule.every(5).minutes.do(check_fuel)
while True:
    schedule.run_pending()
    time.sleep(1)
