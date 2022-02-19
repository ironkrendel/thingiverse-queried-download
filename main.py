from multiprocessing.dummy import Process
import requests
import os
import cursor
import re
import json

cfg = json.load(open("./cfg.json", "r"))
key = cfg["key"]
if (cfg["download_directory"][-1] == "/"):
    download_dir = cfg["download_directory"]
else:
    download_dir = cfg["download_directory"] + "/"
data = ""
thing_urls = []

#data input and check
while True:
    thing_urls = input("Enter thing id or url: ").replace(" ", "").split(",")
    check = False
    for i in thing_urls:
        #id check
        if (i.isnumeric() and len(i) == 7):
            pass
            
        #url check
        elif (re.match(r"https://www.thingiverse.com[a-zA-Z/]*", i)):
            pass
            
        else:
            print("enter valid data")
            check = True
    if not check:
        break
cursor.hide()
print("-"*100)

for i in thing_urls:
    #if id is given
    if (i.isnumeric() and len(i) == 7):
        print("Connecting")
        r = requests.get(f"https://api.thingiverse.com/things/{i}/files?access_token={key}")
        if r.status_code == 200:
            print("Connected")
        else:
            print(f"Error on connecting. Error code - {r.status_code}")
        data = r.json()
        print("-"*100)
        #downloading
        for j in data:
            print(f"Downloading {j['name']}")
            file = requests.get(j["download_url"] + f"?access_token={key}", allow_redirects=True)
            while True:
                try:
                    open(download_dir + j["name"], "wb").write(file.content)
                    print(f"Downloaded {j['name']}                        ")
                    break
                except FileNotFoundError:
                    os.makedirs("./things/")
        print("-"*100)
        
    #if url is given
    elif (re.match(r"https://www.thingiverse.com[a-zA-Z/]*", i)):
        print("Connecting")
        r = requests.get(f"https://api.thingiverse.com/things/{i.split(':')[2].split('/')[0]}/files?access_token={key}")
        if r.status_code == 200:
            print("Connected")
        else:
            print(f"Error on connecting. Error code - {r.status_code}")
        data = r.json()
        print("-"*100)
        #downloading
        for j in data:
            print(f"Downloading {j['name']}")
            file = requests.get(j["download_url"] + f"?access_token={key}", allow_redirects=True)
            while True:
                try:
                    open(download_dir + j["name"], "wb").write(file.content)
                    print(f"Downloaded {j['name']}                        ")
                    break
                except FileNotFoundError:
                    os.makedirs("./things/")
        print("-"*100)
#finish
print("Downloading finished")
os.system("pause")