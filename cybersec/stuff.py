
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
        sqareroot = isqrt(x2 - n)
        p = (x // 2 + sqareroot)
        q = (x // 2 - sqareroot)
        if p * q == n: 
            return p, q

# https://en.wikipedia.org/wiki/RSA_(cryptosystem)
def rsa_decrypt(c, e, p, q):
    d = pow(e, -1, (p - 1) * (q - 1))
    return bytes.fromhex(hex(pow(c, d, p * q))[2:])