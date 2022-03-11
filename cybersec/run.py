from pwn import connect
from time import sleep

# ----------------------------------------------

url = ""
port = ""
flag = ""
conn = connect(url, port)

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet += "_{}"
alphabet += "0123456789"
alphabet += "abcdefghijklmnopqrstuvwxyz".upper()

# -----------------------------------------------

oracle = conn.recv
conn.recv()

# -----------------------------------------------

while flag[-1] != "}":

	print(flag)
	sleep(0.5)
	for x in alphabet:
		conn.recv()
		conn.send((flag + x + "\n").encode())
		guess = conn.recv
		if guess in oracle:
			flag += x
			break


# ----------------------------------------------

print("found!")
print(flag)
conn.close()