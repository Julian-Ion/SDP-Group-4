import threading
from time import sleep


def test():
    while True:
        print("Hi")
        sleep(1)


threading.Thread(target=test, daemon=False).start()
sleep(5)