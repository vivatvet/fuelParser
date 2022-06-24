import json
import requests
from site_parser import get_azs
import schedule
import time
import telegram_bot
from orm import Orm

fuels = {}
fuels_wog = {}

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
    if not saved:
        saved = {}
    if not current:
        current = {}
    if len(saved) != len(current):
        return True
    for saved_fuel in saved:
        for current_fuel in current:
            if current_fuel["id"] == saved_fuel["id"]:
                if current_fuel["Price"] != saved_fuel["Price"]:
                    return True
    return False


def check_fuel():
    orm = Orm()
    try:
        azs_list_json = get_azs()
    except Exception as e:
        print(e, flush=True)
        return True
    users = orm.get_users()
    azs_changed = {}
    for azs in azs_list_json["data"]:
        if not fuels.get(azs["id"]):
            fuels[azs["id"]] = azs["FuelsAsArray"]
            continue
        try:
            fuel_was_changed = is_fuel_changed(fuels.get(azs["id"]), azs.get("FuelsAsArray"))
        except Exception as e:
            print(e, flush=True)
            fuel_was_changed = True

        if fuel_was_changed:
            azs_changed[azs["id"]] = azs

        fuels[azs["id"]] = azs["FuelsAsArray"]

    for user in users:
        azs_list = [au[0] for au in orm.get_subscribed_azs(user_id=user[0])]
        for azs_id, azs in azs_changed.items():
            if azs_id in azs_list:
                prices = "\n".join([a["Title"] + " ---- " + a["Price"] for a in azs["FuelsAsArray"]])
                telegram_bot.send_msg(user_id=user[0], msg=f'{azs["FullName"]}\n{azs["Address"]}\n{prices}')


def check_fuel_wog():
    orm = Orm()
    subscribed = orm.get_wog_subscribed()
    for subscribe in subscribed:
        user = subscribe[0]
        azs_id = subscribe[1]
        try:
            res = requests.get("https://api.wog.ua/fuel_stations/" + str(azs_id))
        except Exception as e:
            print(e, flush=True)
            return True
        try:
            res_json = json.loads(res.text)
        except Exception as e:
            print(e, flush=True)
            return True
        try:
            name_azs = res_json["data"]["name"]
        except Exception as e:
            print(e, flush=True)
            return True
        try:
            fuels_desc = res_json["data"]["workDescription"]
        except Exception as e:
            print(e, flush=True)
            return True
        if not fuels_wog.get(user):
            fuels_wog[user] = {}
        if fuels_wog[user].get(azs_id) != fuels_desc:
            telegram_bot.send_msg(user_id=user, msg=f"WOG: {name_azs} Changed:\n {fuels_desc}")

        fuels_wog[user][azs_id] = fuels_desc


telegram_bot.start_bot()

schedule.every(5).minutes.do(check_fuel)
schedule.every(5).minutes.do(check_fuel_wog)
while True:
    schedule.run_pending()
    time.sleep(1)
