import time
import hashlib
import urllib.request
import json
from datetime import datetime
from dateutil import parser





def parse_group_today(group):
    group_md5 = hashlib.md5(group.encode(encoding='utf_8')).hexdigest()
    link = "https://public.mai.ru/schedule/data/{0}.json".format(group_md5)
    rasp = urllib.request.urlopen(link).read()
    rasp = json.loads(rasp)

    rasp.pop("group")

    group_rasp = []

# В ЭТОТ МАССИВ НУЖНО ЗАПИХНУТЬ АЙДИШНИКИ ПОЛЬЗОВАТЕЛЕН ИЗ ГРУППЫ group ИЗ БД
    group_id_list = [1, 2 ,3 ]

    group_notify_status = []

    for data in group_id_list:
        group_notify_status.append({'user': data, 'notify_status': 0})


    for day in rasp.items():
        date = datetime.fromisoformat(str(parser.parse(day[0], dayfirst=True)))
        # print(date.date())
        pary = day[1]["pairs"]
        
        for _para in pary.items():
            para = _para[1]
            
            time_start = datetime.fromisoformat(
                str(parser.parse(para["time_start"])))
            time_start = datetime.combine(date.date(), time_start.time())
            time_end = datetime.fromisoformat(str(parser.parse(para["time_end"])))
            time_end = datetime.combine(date.date(), time_end.time())

            name = []
            for _name in para["class"].items():
                name.append(_name[0])
            name = ' / '.join(name)

            lector = []
            for _lector in para["lector"].items():
                lector.append(_lector[1])
            lector = ', '.join(lector)

            type = []
            for _type in para["type"].items():
                type = _type[0]

            room = []
            for _room in para["room"].items():
                room.append(_room[1])
            room = ', '.join(room)
            
            if time.localtime().tm_mday == time_start.day and time.localtime().tm_mon == time_start.month and time_start.year == time.localtime().tm_year:
            
                group_rasp.append({"time_start_hour": time_start.hour, "time_start_minutes": time_start.minute, "time_end": time_end.hour, "time_end_minutes": time_end.minute, "name": name, "type": type, "lector": lector, "room": room, "group": group, "notify": group_notify_status})
    return group_rasp

for data in (parse_group_today('М3О-221Б-20')):
    print(str(data))

