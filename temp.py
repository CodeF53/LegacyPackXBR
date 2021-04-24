from concurrent.futures import ProcessPoolExecutor
import os
from time import sleep
from multiprocessing import freeze_support


def task(i):
    print("start {}".format(i))
    sleep(2)
    print("stop {}".format(i))


def main():
    with ProcessPoolExecutor(max_workers=2) as executor:
        for i in range(20):
            aaa = i * 2
            executor.submit(task, aaa)

    input("aa")


if __name__ == '__main__':
    freeze_support()
    main()