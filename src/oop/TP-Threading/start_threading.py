import threading
import time

exit_flag = 0

class MyThread(threading.Thread):

    def __init__(self, thread_id, name, counter):

        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):

        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + self.name)

def print_time(thread_name:str, delay:int, counter:int):

    while counter:
        if exit_flag:
            thread_name.exit()
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1

# Create new threads
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(1, "Thread-2", 2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()