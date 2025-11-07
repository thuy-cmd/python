import threading
import time
def greet(name):
    for i in range(3):
        print(f"Xin chao {name} - lan {i + 1}")
        time.sleep(1)

t1 = threading.Thread(target=greet, args=("A",))
t2 = threading.Thread(target=greet, args=("B",))
t3 = threading.Thread(target=greet, args=("C",))
t4 = threading.Thread(target=greet, args=("D",))

print("Start")
t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print("Finished")
