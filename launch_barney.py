import os
from multiprocessing import Process

def script1():
    os.system("barney.py")     
def script2():
    os.system("zinger_bot.py")
# def script3():
    # os.system("jarod-bot.py") 

if __name__ == '__main__':
    p = Process(target=script1)
    q = Process(target=script2)
    # r = Process(target=script3)
    p.start()
    q.start()
    # r.start()
    p.join()
    q.join()
    # r.join()