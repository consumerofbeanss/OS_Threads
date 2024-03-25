import threading
import random
import os

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = [None] * BUFFER_SIZE
buffer_index = 0

mutex = threading.Lock()
condition = threading.Condition(mutex)
threads_generated = 0

def producer():
    global buffer, buffer_index, MAX_COUNT, threads_generated
    for _ in range(MAX_COUNT):
        number = random.randint(LOWER_NUM, UPPER_NUM)

        with mutex:
            while buffer_index == BUFFER_SIZE:
                condition.wait()

            buffer[buffer_index] = number
            buffer_index += 1

            condition.notify_all()
            with open("all.txt", "a") as f:
                f.write(str(number) + "\n")

        with mutex:
            threads_generated += 1
            if threads_generated >= MAX_COUNT:
                print("Program finished!")
                os._exit(0)


def customer_even():
    global buffer, buffer_index
    count = 0
    while count < MAX_COUNT:
        with mutex:
            while buffer_index == 0:
                condition.wait()

            if buffer[buffer_index - 1] % 2 == 0:
                number = buffer[buffer_index - 1]
                buffer[buffer_index - 1] = None
                buffer_index -= 1
                count += 1

                condition.notify()
                with open("even.txt", "a") as f:
                    f.write(str(number) + "\n")


def customer_odd():
    global buffer, buffer_index
    count = 0
    while count < MAX_COUNT:
        with mutex:
            while buffer_index == 0:
                condition.wait()

            if buffer[buffer_index - 1] % 2 != 0:
                number = buffer[buffer_index - 1]
                buffer[buffer_index - 1] = None
                buffer_index -= 1
                count += 1

                condition.notify()
                with open("odd.txt", "a") as f:
                    f.write(str(number) + "\n")


if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer)
    customer_even_thread = threading.Thread(target=customer_even)
    customer_odd_thread = threading.Thread(target=customer_odd)

    producer_thread.start()
    customer_even_thread.start()
    customer_odd_thread.start()

    producer_thread.join()
    customer_even_thread.join()
    customer_odd_thread.join()
