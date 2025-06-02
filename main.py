import requests

url = "https://allstar.koreabaseball.com/ws/Allstar.asmx/GetKboAll"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie" : "_gid=GA1.2.1301981944.1748866326; _gat_UA-15700655-14=1; _ga=GA1.1.1062412550.1747921971; ASP.NET_SessionId=v3bhwwghxuikkyi1h0bt421u; NCPVPCLBTG=148798b43573fa2d04e0cf9eb61c54a09bc8f9fa08858ccd749f669eff026033; _ga_L70ZGXMJEC=GS2.1.s1748866325$o2$g0$t1748866329$j56$l0$h0; _ga_WH279QZEYD=GS2.1.s1748866329$o1$g0$t1748866329$j60$l0$h0"
}
data = {
    "pos" : "SS"
}
response = requests.post(url, headers=headers, data=data, verify=False)
print(response.text)