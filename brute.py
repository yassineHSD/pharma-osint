import requests
import os,time
import sys
url_base="https://www.circl.lu/services/"
'''
s=requests.session()
#r=s.get(url_base)
#print(r.status_code)
wordlist=["toto","tata","dynamic-malware-analysis","cve-search","nathan"]
for word in wordlist:
    r=s.get(url_base+word)
    if (str(r.status_code)=="200"):
        print(url_base+word)
    time.sleep(int(sys.argv[1]))
'''
#os.system(sys.argv[1])
