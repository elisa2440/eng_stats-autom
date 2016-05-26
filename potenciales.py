#!/usr/bin/env python

import requests
from datetime import date
from datetime import datetime

r = requests.get('http://stats.labs.lacnic.net/BGP/rawdata/report-missing-ipv4-global-routing-table_latest.txt', auth=('lacnic', 'lacnic!!123'))
static_part = "https://stat.ripe.net/data/routing-status/data.json?resource="
hoy = date.today()
limite = 365*5
data = r.text.split("\n")
f = open("potenciales-"+str(hoy)+".txt", "w")

inicio = datetime.today()
for i in range(1,len(data)):
    temp = data[i].split("|")
    asig = temp[3][1:5]
    bloque = temp[0].split(" ")[0]
    url = static_part+bloque
    if(asig < "2011"):
        s = requests.get(url)
        output = s.json()['data']['last_seen'].get('time')
        if(output is None):
            date = datetime.strptime('1970-01-01', "%Y-%m-%d").date()
        else:
            fecha = s.json()['data']['last_seen']['time'].split("T")
            date = datetime.strptime(str(fecha[0]), "%Y-%m-%d").date()
    else:
            date = hoy
    if((hoy-date).days >= limite):
        f.write(temp[4] + "|" + temp[2] + "|" + temp[3] +"\n")
    print i

f.close()

fin = datetime.today()
print (fin-inicio).seconds/60/60