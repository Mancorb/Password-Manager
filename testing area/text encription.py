import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from hashlib import md5
from cryptography.fernet import Fernet
def getHashVal(text):
    """Returns hash value of a string

    Args:
        text (String): text to convert to hash

    Returns:
        String: string of hash object decrypted from byte form
    """
    return md5(bytes(text, 'utf-8')).hexdigest()

def keyCreator(pswd):
    """Creates encription and decription key based on user input

    Args:
        pswd (String): user input of the password
    """
    password = pswd.encode()  # Convert to type bytes
    salt = getHashVal(pswd)
    salt = salt.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))  # variable key will now have the value of a url safe base64 encoded key.
    
def encryptor(key,text):
    f = Fernet(key)
    return f.encrypt(text.encode())
    
def decryptor(key,target):
    f = Fernet(key)
    return f.decrypt(target).decode("utf-8") 

key = keyCreator("pass")


testList = ["a","a","b","c"]

for i in range(len(testList)):
    testList[i]= encryptor(key,testList[i])

print(testList)
print(type(testList[0]))

if testList[0] == testList[1]:
    
    print("same shit")
else:
    print("diferent shit")

for i in range(len(testList)):
    testList[i]= decryptor(key,testList[i])

print(testList)

