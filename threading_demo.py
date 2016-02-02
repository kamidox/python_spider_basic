import threading
from threading import Thread
import time
import random


def worker_func():
    print('worker thread started in %s' % (threading.current_thread()))
    random.seed()
    time.sleep(random.random())
    print('worker thread finished in %s' % (threading.current_thread()))


def simple_thread_demo(tn=5):
    for i in range(tn):
        t = Thread(target=worker_func)
        t.start()


gLock = threading.Lock()
gRLock = threading.RLock()
gSemaphore = threading.Semaphore(3)
gPool = 1000
gCondition = threading.Condition()


def worker_func_lock(lock):
    lock.acquire()
    worker_func()
    lock.release()


def thread_lock_demo(tn=5):
    for i in range(tn):
        t = Thread(target=worker_func_lock, args=[gSemaphore])
        t.start()


class Consumer(Thread):
    def run(self):
        print('%s started' % threading.current_thread())
        while True:
            global gPool
            global gCondition

            gCondition.acquire()
            random.seed()
            c = random.randint(500, 1000)
            print('%s: Trying to consume %d. Left %d' % (threading.current_thread(), c, gPool))
            while gPool < c:
                gCondition.wait()
            gPool -= c
            time.sleep(random.random())
            print('%s: Consumed %d. Left %d' % (threading.current_thread(), c, gPool))
            gCondition.release()


class Producer(Thread):
    def run(self):
        print('%s started' % threading.current_thread())
        while True:
            global gPool
            global gCondition

            gCondition.acquire()
            random.seed()
            p = random.randint(100, 200)
            gPool += p
            print('%s: Produced %d. Left %d' % (threading.current_thread(), p, gPool))
            time.sleep(random.random())
            gCondition.notify_all()
            gCondition.release()


def consumer_producer_demo():
    for i in range(1):
        Consumer().start()

    for i in range(1):
        Producer().start()


if __name__ == '__main__':
    # simple_thread_demo()
    # thread_lock_demo()
    consumer_producer_demo()
