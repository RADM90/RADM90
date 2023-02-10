import hashlib
import random

txt = f"{random.randint(0, 255):04d}".encode('utf-8')
enc = hashlib.md5()
enc.update(txt)
user_id = enc.hexdigest()
