import tqdm
from Tools import md5_hash, all_passwords

hash = md5_hash("hello")

for password in tqdm.tqdm(all_passwords()):
    if hash == md5_hash(password):
        print(f"\nPassword cracked: {password}")
        break
