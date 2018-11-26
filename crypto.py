
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

from cryptography.fernet import Fernet

ENCRYPTED = True

def generate_key():
    return Fernet(Fernet.generate_key())

if ENCRYPTED: #_____________________________________________________________

  # secure AES based encryption
    
    def encrypt(secret, key1, key2=None):
        secret = bytes([secret])
        if key2==None:
            return key1.encrypt(secret)
        return key1.encrypt(key2.encrypt(secret))
    
    def decrypt(unknown, key1, key2=None):
        if key2==None:
            secret = key1.decrypt(unknown)
        else:
            secret = key2.decrypt(key1.decrypt(unknown))
        return int.from_bytes(secret, byteorder='big')

else: # ____________________________________________________________________

  # totally insecure keyless implementation 

    def encrypt(secret, key1, key2=None):
        return secret
    
    def decrypt(unknown, key1, key2=None):
        return unknown

# __________________________________________________________________________


