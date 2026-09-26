import time


def start(task, interval=60):

    print("CollegeOS started.")

    while True:

        task()

        time.sleep(interval)