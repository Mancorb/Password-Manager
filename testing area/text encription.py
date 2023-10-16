#steps
#formula C = K * P
# C = cypher
# K = matrix of data from the length of P 
# P = original text to encrypt in ascci format
import numpy as np
from random import randint
options = list("1234567890-=!@#$%^&*()_+qwertyuiop[]asdfghjkl;zxcvbnm,./QWERTYUIOP{|}ASDFGHJKL:ZXCVBNM<>?`~")

def encrypt(word):
    """Encrypts a word with matrix multiplication

    Args:
        word (string): word to encrypt

    Returns:
        string: encryoted result
    """
    res = ""
    while len(res) < len(word):
        C = _obtainC(word,len(options))
        for i in C:
            res +=options[i] 

    return str(res)


def _obtainC (word, n):
    """Returns the encrypted result of a word's character
    Args:
        word (String): letter to encrypt
    Return:
        string: encrypted letter

    """
    P = _obtainP(word)
    K = _obtainK(P)
    C = np.array(np.matmul(K,P))
    for i in range (len(C)):
        C[i]= (C[i]% n)

    return C


def _obtainK(P):
    """Generate the K matrix, the number of cols must be equal to n which is the number of letters in P."

    Args:
        P (string): string value of P
    
    Returns:
        K matrix.
    """
    n = len(P)
    K = [] #store the matrix
    temp = [] # row of matrix
    switch= False

    counter = 2
    for row in range(n):
        for column in range(n):
            temp.append(int((P[row]/counter)*100))

            if switch:
                counter -= 1.5
            else:
                counter += 1.5
        K.append(temp)
        temp = []
        switch = not switch
    
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
wordlist = []


while True:
    print(encrypt(input("Palabra a encriptar: ")))

""" with open("wordList.txt","r") as file :
    for word in file:
        wordlist.append(word[:-1])

for i in wordlist:
    results.append(encrypt(i)) """

""" for i in range(len(results)):
    print(wordlist[i]+" -> "+ results[i]+"\n") """


""" uniques = []

for word in results:
    if word not in uniques:
        uniques.append(word)

print("Example of encryption:"+ wordlist[0]+ " => "+ results[0])
print("original word list length:"+str(len(wordlist)))
print("number of unique encryptions:"+str(len(results)))
 """