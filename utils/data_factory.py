#data_factory.py
import time
import random
import string

def unique_code(prefix):
    return f"{prefix}-{int(time.time())}-{random.randint(100,999)}"

def unique_name(prefix):
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"{prefix}-{letters}"
