import pickle
import tqdm
import os
from Tools import md5_hash, all_passwords

if not os.path.exists("all_passwords.pkl"):
    passwords = {}
    for password in tqdm.tqdm(all_passwords()):
        passwords[md5_hash(password)] = password
    pickle.dump(passwords, open("all_passwords.pkl", "wb"))
else:
    passwords = pickle.load(open("all_passwords.pkl", "rb"))

hash = md5_hash("hello")

if hash in passwords:
    print(f"Password cracked: {passwords[hash]}")
else:
    print("Password not found")