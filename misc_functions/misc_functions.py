# Code taken from
# https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer     = None
#         self.interval   = interval
#         self.function   = function
#         self.args       = args
#         self.kwargs     = kwargs
#         self.is_running = False
#         self.start()

#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True

#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False


import time
import datetime
from threading import Event, Thread

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()


def rounded_float(num_txt:str,
                         digits:int=6):
    """
    Return a rounded float from an input string 
    """
    try:
        if num_txt=='':
            return 0
        return round(number=float(num_txt), ndigits=digits)
    except:
        num_txt_2 = num_txt.replace("e", "")
        num_txt_2 = num_txt_2.replace("+", "")
        num_txt_2 = num_txt_2.replace("-", "")
        if num_txt_2=='':
            return 0
        return round(number=float(num_txt_2), ndigits=digits)

def seconds_to_hms_string(time_s:int):
    time_h = time_s // 3600 
    time_m = (time_s - 3600*time_h) // 60
    time_s = (time_s - 3600*time_h - 60*time_m)

    return(f'{time_h}:{time_m}:{time_s}')


def is_numeric(txt:str)->bool:
    """Return true if the input string is a number.
    The input is converted into a float. 
    If an exception is raised then it is not a number. """
    try:
        float(txt)
        return True
    except ValueError:
        return False

def set_in_range(param:float,max:float,min:float):
    """Sets the parameter suh that it is within the set max and min values"""
    if param > max:
        param = max
    elif param < min:
        param = min
    return param

from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        # print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def intlist_to_hex_str(int_list):
    text = "0x"
    for num in int_list:
        text += hex(num)[2:]

    return text


def min_max_int(input, min, max):
    if input<min:
        return min
    if input>max:
        return max
    return input