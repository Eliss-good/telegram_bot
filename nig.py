import time
from threading import Thread


class Thread1(Thread):
    def run(self):
        for i in range(10000):
            time.sleep(0.01)
            print("1")

class Thread2(Thread):
    def run(self):
        for i in range(10000):
            time.sleep(0.01)
            print("2-----------------------")

t1 = Thread1()
t1.start()
t2 = Thread2()
t2.start() 