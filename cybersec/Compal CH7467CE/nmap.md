Nmap scan report for _gateway (192.168.166.1)
Host is up (0.0023s latency).
Not shown: 65532 closed ports
PORT    STATE SERVICE  VERSION
53/tcp  open  domain   dnsmasq 2.78
| dns-nsid: 
|   NSID: nsrcustl1-l1-02 (6e7372637573746c312d6c312d3032)
|   id.server: nsrcustl1-l1-02
|_  bind.version: dnsmasq-2.78
80/tcp  open  http     lighttpd
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: 400 - Bad Request
443/tcp open  ssl/http lighttpd
| ssl-cert: Subject: commonName=68:02:B8:46:89:3C/organizationName=Compal Broadband Networks/countryName=TW
| Issuer: commonName=Compal Broadband Networks Cable Modem Root Certificate Authority/organizationName=Compal Broadband Networks/countryName=TW
| Public Key type: rsa
| Public Key bits: 1024
| Signature Algorithm: sha1WithRSAEncryption
| Not valid before: 2020-06-23T11:44:36
| Not valid after:  2040-06-23T11:44:36
| MD5:   9e04 7913 3f40 299d 1317 f6db 35a8 c06d
|_SHA-1: a317 a75e 3853 8930 350d 33ab a0c5 50ce aa74 48b4
|_ssl-date: TLS randomness does not represent time

NSE: Script Post-scanning.
Initiating NSE at 14:59
Completed NSE at 14:59, 0.00s elapsed
Initiating NSE at 14:59
Completed NSE at 14:59, 0.00s elapsed
Initiating NSE at 14:59
Completed NSE at 14:59, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 2654.25 seconds
