#steps
#formula C = K * P
# C = cypher
# K = matrix of data from the image info (RGB matrix)
# P = original text to encrypt in ascci format
import numpy as np
from random import randint

def encrypt(word):
    res = ""
    while len(res) < len(word):
        C = _obtainC(word)
        for i in C:
            res = res + chr(i) 

    return str(res)


def _obtainC (word):
    P = _obtainP(word)
    K = _obtainK(len(P))
    C = np.array(np.matmul(K,P))
    for i in range (len(C)):
        C[i]= (C[i]% 122)

    return C


def _obtainK(n):
    """Generate the K matrix, the number of cols must be equal to n which is the number of letters in P."

    Args:
        n (int): number of cols to generate
    
    Returns:
        K matrix.
    """
    K = []
    nums = np.random.randint(0,255,(2000, n))
    for i in range(n):
        temp = nums[randint(0,len(nums))]
        temp = temp.tolist()
        K.append(temp)
    
    return np.array(K)


def _obtainP(word):
    """Convert a word into ASCII value

    Args:
        word (string): Word to convert

    Returns:
        list: Converted values.
    """
    word = [word]
    P = [ord(ele) for sub in word for ele in sub]
    return P


results = []
for i in range(20):
    results.append(encrypt("password"))

print(results)
print("\n")