from base64 import b64decode

def base16_decode(enc: str) -> str:
    data = [f"{ord(x) - 97:04b}" for x in enc]
    print(data)
    return ''.join(chr(int(data[i : i + 1], 2)) for i in range(0, len(data), 2))

def rot13(enc: str) -> str:
    if not enc.isascii(): raise ValueError
    dec = ""
    for x in enc:
        if x.isalpha():
            offs = 65 if x.isupper() else 97
            dec += chr((ord(x) - offs + 13) % 26 + offs) 
        else:
            dec += x
    return dec

def caesar_decrypt(cipher: str, key = None, lower = True, upper = True, digit = False):
    if not key: return [caesar_decrypt(cipher, chr(key), lower, upper, digit) for key in range(97, 123)]
    plain = ''
    for x in cipher:
        if lower and x.islower(): plain += chr(((ord(x) - ord(key.lower())) % 26) + 97)
        elif upper and x.isupper(): plain +=  chr(((ord(x) - ord(key.upper())) % 26) + 65)
        elif digit and x.isdigit(): plain += chr(((ord(x) - ord(key)) % 10) + 48)
        else: plain += x
    return plain

def vigenere_decrypt(cipher, key):
    plain = ''
    i = 0
    for x in cipher:
        if x.isalpha():
            plain += caesar_decrypt(x, key[i % len(key)])
            i += 1
        else: plain += x
    return plain

# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def extendedeuclidalgo(x: int, y: int) -> list:
    r = x % y
    out = [(x // y, r)]
    if not r: return out
    out.extend(extendedeuclidalgo(y, r))
    return out

# https://en.wikipedia.org/wiki/Continued_fraction
def continuedfracttions(x: int, y: int) -> list:
    return [x[0] for x in extendedeuclidalgo(x, y)]

# https://en.wikipedia.org/wiki/Continued_fraction#Infinite_continued_fractions_and_convergents
def convergents(fractions: list) -> list:
    convergents = [(fractions[0], 1), (fractions[1] * fractions[0] + 1, fractions[1])]
    for i in range(2, len(fractions)):
        convergents.append((fractions[i] * convergents[i - 1][0] + convergents[i - 2][0], fractions[i] * convergents[i - 1][1] + convergents[i - 2][1]))
    return convergents

# https://en.wikipedia.org/wiki/Wiener's_attack
def rsa_wienersattack(e: int, n: int):
    from math import isqrt
    fractions = continuedfracttions(e, n)
    converg = convergents(fractions)[1:]
    for k, d in converg:
        if not k: continue
        phi = (e * d - 1) // k
        x = n - int(phi) + 1
        x2 = x * x // 4
        if n > x2: continue
        squareroot = isqrt(x2 - n)
        p = (x // 2 + squareroot)
        q = (x // 2 - squareroot)
        if p * q == n: 
            return p, q

def rsa_decrypt(c, e, p, q):
    d = pow(e, -1, (p - 1) * (q - 1))
    return bytes.fromhex(hex(pow(c, d, p * q))[2:])

def rsa_encrypt(m, e, n):
    return pow(int(m.encode().hex(), 16), e, n)

def rsa_chosen_cypher(c, e, n):
    r = int(b"pwned".hex(), 16)
    cr = c * pow(r, e, n) % n
    mr = int(input("Please decrypt:\n" + str(cr) + "\n\n> "))
    return bytes.fromhex(hex(mr * pow(r, -1, n) % n)[2:])


def ddes_meet_in_the_middle(alphabet = "0123456789", keylen = 8) -> tuple:
    '''
    Meet-in-the-Middle-Attack for DoubleDES
    https://de.wikipedia.org/wiki/Meet-in-the-middle-Angriff

    param   alphabet    alphabet to generate keys from
    param   keylen      length of key, must be between 1 and 8
    returns             (key1, key2) as str
    '''

    from Crypto.Cipher import DES
    from itertools import product

    plain = b"pwned   "

    keylist = [(''.join(x) + ' ' * (8 - keylen)).encode() for x in product(alphabet, repeat=keylen)]
    cipher = bytes.fromhex(input("Please encrypt:\n" + plain.rstrip().hex() + "\n\n> "))

    keytable = {}
    for key in keylist:
        keytable[DES.new(key, DES.MODE_ECB).encrypt(plain)] = key

    for key in keylist:
        guess = DES.new(key, DES.MODE_ECB).decrypt(cipher)
        if guess in keytable:
            return (keytable[guess].decode(), key.decode())

def ddes_encrypt(cipher, key1, key2) -> str:
    '''
    Encryption for DoubleDES
    https://en.wikipedia.org/wiki/Data_Encryption_Standard

    param   cipher      the ciphertext encoded as hex
    param   key1        first key
    param   key1        second key
    returns             encoded plaintext
    '''
    from Crypto.Cipher import DES

    return DES.new(key1.encode(), DES.MODE_ECB).decrypt(DES.new(key2.encode(), DES.MODE_ECB).decrypt(bytes.fromhex(cipher))).decode()


def rail_fence_decrypt(cipher, rails):
    '''
    Encryption for Rail-Fence, can deal with unpadded messages
    https://en.wikipedia.org/wiki/Rail_fence_cipher

    param   cipher      ciphertext as string
    param   rails       amount of rails
    returns             encoded plaintext
    '''
    if not rails: return print("brute-force not implemented")
    from math import ceil
    
    diag = ceil((len(cipher) - rails) / (rails - 1)) + 1
    padd = -(len(cipher) - rails) % (rails - 1)
    first = ceil(diag / 2) + (not padd and not diag % 2)
    last = ceil((diag - 1) / 2) + (not padd and diag % 2)
    cipher = [cipher[:first]] + [cipher[i:i + diag - ((len(cipher) - i) / diag < padd)] for i in range(first, len(cipher) - last, diag)] + [cipher[-last:]]
    cipher = list(map(list, cipher))
    plain = ''
    pos = 0
    step = -1
    while cipher[pos]:
        plain += cipher[pos].pop(0)
        if pos == 0 or pos == len(cipher) - 1: step = -step
        pos += step
    return plain

def substitution_decrypt(cipher, alphabet):
    mapping = dict(zip(alphabet.lower(), 'abcdefghijklmnopqrstuvwxyz'))
    mapping.update(dict(zip(alphabet.upper(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')))
    return ''.join([mapping[x] if x.isalpha() else x for x in cipher])

def decode_private_RSA_KEY(file):
    out = {}
    key = open(file).readlines()
    key = b64decode(''.join(key[1:-1]).replace("\n", "")).hex()
    out["key"] = key
    key = [key[x:x+2] for x in range(0, len(key), 2)]
    if not key.pop(0) == '30': return
    if not key.pop(0) == '82': return
    out["length"] = ''.join(key.pop(0) + key.pop(0))
    return out