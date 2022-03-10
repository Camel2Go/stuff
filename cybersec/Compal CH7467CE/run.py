from requests import post, get
import re
from time import sleep

ip = "http://192.168.166.1"
headers = {"X-Requested-With": "XMLHttpRequest"}
cookies = {}

login = "/common_page/login.html"
setter = "/xml/setter.xml"
getter = "/xml/getter.xml"
index = "/index.html"
menu = "/common_page/menu.html"
status = "/common_page/status.html"
ping = "/gw_page/RgDiagnostics.html"


# request initial session-token
token = get(ip + index).headers.get("Set-Cookie")[13:23]

# set received infos
cookies["sessionToken"] = token
headers["Referer"] = ip + login
data = {
	"token": token,
	"fun": 15,
	"Username": "Username",
	bytes.fromhex("50617373776f7264").decode(): bytes.fromhex("").decode()
}

# request session-id
req = post(ip + setter, data=data, headers=headers, cookies=cookies)
sid = req.text[15:]
token = req.headers.get("Set-Cookie")[13:23]

# set new infos
cookies["sessionToken"] = token
cookies["SID"] = sid

print("sessionToken:", token, "SID:", sid)

# request for ping
headers["Referer"] = ip + ping
data = {
	"token": token,
	"fun": "126",
	"Type": "2",
	"Target_IP": "localhost",
	"Ping_Size": "64",
	"Num_Ping": "1",
	"Ping_Interval": ""
}

req = post(ip + setter, data=data, headers=headers, cookies=cookies)

sleep(2)
print(req.status_code)
print(req.headers)
if req.headers.get('Content-Length') != '0' or req.headers.get("Location") != None: print("Error")
else:
	cookies["sessionToken"] = req.headers.get("Set-Cookie")[13:23]
	for i in range(30):
		req = post(ip + getter, data={"fun": "126"}, cookies=cookies, headers=headers)
		print(req.status_code)
		print(req.text)
		sleep(2)