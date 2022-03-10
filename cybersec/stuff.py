
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

def caesar(enc: str) -> list:
    return [''.join([chr(((ord(x) - 97 + i) % 26) + 97) for x in enc]) for i in range(26)]

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
