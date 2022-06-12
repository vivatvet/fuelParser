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


def is_fuel_changed(saved: dict, current: dict) -> bool:
    for saved_fuel in saved:
        for current_fuel in current:
            if current_fuel["id"] == saved_fuel["id"]:
                if current_fuel["Price"] != saved_fuel["Price"]:
                    return True
    return False


def check_fuel():
    orm = Orm()
    azs_list_json = MyHTMLParser().get_azs()
    users = orm.get_users()
    azs_changed = {}
    for azs in azs_list_json["data"]:
        if not fuels.get(azs["id"]):
            fuels[azs["id"]] = azs["FuelsAsArray"]
            continue
        fuel_was_changed = is_fuel_changed(fuels.get(azs["id"]), azs.get("FuelsAsArray"))

        if fuel_was_changed:
            azs_changed[azs["id"]] = azs

        fuels[azs["id"]] = azs["FuelsAsArray"]

    for user in users:
        azs_list = [au[0] for au in orm.get_subscribed_azs(user_id=user[0])]
        for azs_id, azs in azs_changed.items():
            if azs_id in azs_list:
                prices = "\n".join([a["Title"] + " ---- " + a["Price"] for a in azs["FuelsAsArray"]])
                telegram_bot.send_msg(user_id=user[0], msg=f'{azs["FullName"]}\n{azs["Address"]}\n{prices}')


telegram_bot.start_bot()

schedule.every(5).minutes.do(check_fuel)
while True:
    schedule.run_pending()
    time.sleep(1)
