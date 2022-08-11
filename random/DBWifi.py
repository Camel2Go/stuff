import re
import requests

header = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "de,en-US;q=0.7,en;q=0.3",
	"Connection": "keep-alive",
	"DNT": "1",
	"Host": "www.hotsplots.de",
	"Sec-Fetch-Dest": "document",
	"Sec-Fetch-Mode": "navigate",
	"Sec-Fetch-Site": "none",
	"Sec-Fetch-User": "?1",
	"Sec-GPC": "1",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
}
# GET /auth/login.php?res=notyet&uamip=192.168.44.1&uamport=80&challenge=064553dff95859a0718dc4d1f7dc3732&called=00-C0-3A-C9-15-A5&mac=68-17-29-63-C5-D1&ip=192.168.44.154&nasid=colibri-00c03ac995a5&sessionid=62c7044d00000047&userurl=http%3a%2f%2f192.168.44.1%2f HTTP/1.1
# Location: https://www.hotsplots.de/auth/login.php?res=notyet&uamip=192.168.44.1&uamport=80&challenge=064553dff95859a0718dc4d1f7dc3732&called=00-C0-3A-C9-15-A5&mac=68-17-29-63-C5-D1&ip=192.168.44.154&nasid=colibri-00c03ac995a5&sessionid=62c7044d00000047&userurl=http%3a%2f%2f192.168.44.1%2f
# <input type="checkbox" size="20" id="termsChkbx" name="termsOK">
# <input type="hidden" name="challenge" value="064553dff95859a0718dc4d1f7dc3732">
# https://www.hotsplots.de/auth/login.php?res=notyet&challenge=064553dff95859a0718dc4d1f7dc3732&mac=68-17-29-63-C5-D1&ip=192.168.44.154&nasid=colibri-00c03ac995a5&sessionid=62c7044d00000047&userurl=http%3a%2f%2f192.168.44.1%2f

url_login = "http://www.hotsplots.de/auth/login.php"
url_challenge = "http://192.168.44.1"
url_logout = "http://192.168.44.1/logoff"

req_challenge = requests.get(url = url_challenge)
challenge = re.search(r"[0-9a-f]{32}", req_challenge.text).group()

print("challenge: " + challenge)

post = {
	"haveTerms": "1",
	"termsOK": "on",
	"button": "Jetzt+kostenlos+surfen",
	"challenge": challenge,
	"uamip": "192.168.44.1",
	"uamport": "80",
	"userurl": "",
	"myLogin": "agb",
	"ll": "de",
	"nasid": "colibri-00c03ac995a5",
	"custom": "1"
}

url_login += "*res=notyet&uamip=192.168.44.1&uamport=80&nasid=colibri-00c03ac995a5"
requests.post(url = url_login)