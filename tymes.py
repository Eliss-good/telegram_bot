
import time

# while True:
#     time.sleep(3)
#     t = time.localtime()
#     print(t.tm_hour, t.tm_min, t.tm_sec)

str = '13 часов 22 минут 0 секунд'
# while True:
#     print(time.time(), time.time()+5)
#     time.sleep(1)


dic1 = {'a': 1, 'b': 2, 'c': 3}

dic2 = {'a': 11, 'b': 12, 'c': 13}

dic3 = {'a': 13, 'b': 79, 'c': 99}
lol = []
lol.append(dic1)
lol.append(dic2)
lol.append(dic3)
print(lol)
lol.remove({'a': 11, 'b': 12, 'c': 13})
print(lol)
