# Chengyi Zhang cz5818
# Rui Jia rj418
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

from cryptography.fernet import Fernet

ENCRYPTED = True

def generate_key():
    return Fernet.generate_key()

if ENCRYPTED: #_____________________________________________________________

  # secure AES based encryption
    
    def encrypt(key, secret, key1, key2=None):
        key1 = Fernet(key1)
        # Combine and then encrypt
        secret = key+bytes([secret])
        if key2==None:
            return key1.encrypt(secret)
        key2 = Fernet(key2)
        return key1.encrypt(key2.encrypt(secret))
    
    def decrypt(unknown, key1, key2=None):
        key1 = Fernet(key1)
        if key2==None:
            secret = key1.decrypt(unknown)
        else:
            key2 = Fernet(key2)
            # Note that the order of decryption matters
            secret = key2.decrypt(key1.decrypt(unknown))
        # Split after decrypt
        return (secret[:-1], secret[-1])
        #return int.from_bytes(secret, byteorder='big')

else: # ____________________________________________________________________

  # totally insecure keyless implementation 

    def encrypt(key, secret, key1, key2=None):
        return secret
    
    def decrypt(unknown, key1, key2=None):
        return unknown

# __________________________________________________________________________


