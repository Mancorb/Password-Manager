from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode


password = 'sekret'
message = 'this is a secret message'
ciphertext = encrypt(password, message)

encoded_cipher = b64encode(ciphertext)

print(encoded_cipher)
print("\nEncripted...\n")

result = encoded_cipher


result = b64decode(result)
result = decrypt(password, result).decode("utf-8")


print (result)