from ctypes import c_bool
from multiprocessing import Queue, Value

optimizer_queue = Queue()

is_optimizing = Value(c_bool, False)
