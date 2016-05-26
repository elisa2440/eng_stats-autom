#!/usr/bin/env python

from datetime import date,datetime,timedelta
import os
import os.path

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

inicio = datetime.strptime('2016-04-19', "%Y-%m-%d").date()
hoy = date.today()
fin = hoy + timedelta(days = 1)

o = open("dolares.txt", "w")
o.write("minimo,maximo,fecha\n")

for date in daterange(inicio,fin):
    if os.path.isfile("potenciales-"+str(date)+".txt"):
        f = open("potenciales-"+str(date)+".txt", "r")
        ips = 0
        for i in f.readlines():
            bloques = i.split("|")[0].split(",")
            n = len(bloques)
            for j in range(0,n-1):
                prefijo = bloques[j].split("/")[1].split(" ")[0]
                for k in range(11,25):
                    if int(prefijo) == k:
                        ips = ips + 2**(32-k)


        f.close()
        max_dol = ips*15
        min_dol = ips*10
        o.write(str(min_dol)+","+str(max_dol)+","+str(date)+"\n")






