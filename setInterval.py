# Found in https://gist.github.com/stamat/5371218
import threading


def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.daemon = True
    t.start()
    return t
