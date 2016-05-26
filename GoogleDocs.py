# coding=utf-8

import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import datetime
import pytz
from netaddr import *
from sys import stdout

json_key = json.load(open('input.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gclient = gspread.authorize(credentials)
gspread = gclient.open('Logs de Transferencia 2.3.2.18')
sheet = gspread.sheet1
f = stdout
f.write("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8' /> <style text='text/css'>#tickets{padding:10px;margin:10px 0;background-color:#f7f7f7;border-radius:5px;float:left;}#tickets table{border:none;margin:0;padding:0;}#tickets table td {font-family:'Arial', 'Helvetica', Sans-serif;font-weight:normal;font-size:12px;line-height:14px;padding:5px 10px;margin:0;color:#222;border-bottom:1px solid #e6e6e6;text-align:left;}#tickets table td:last-child{border:none;}#tickets table th {font-family:'Arial', 'Helvetica', Sans-serif;font-weight:bold;font-size:12px;line-height:14px;padding:5px 10px;margin:0;color:#fff;background-color:#222;border:none;text-align:left;} </style></head><body><div id='tickets'>")
f.write("<table width='600' cellpadding='0' cellspacing='0' border='0'><tr><th>Fecha</th><th>Organizacion oferente</th><th>Organizacion receptora</th><th>Bloque transferido</th></tr>")
ips = 0
prod_date = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).isoformat()
st = {
    "version" :
  {
    "stats_version" : "3.0" ,
    "producer" : "LACNIC",
    "UTC_offset" : -3 ,
    "production_date" : str(prod_date) ,
    "records_interval" : {
      "start_date" : "2016-05-23T00:00:00-03:00" ,
      "end_date" : str(prod_date)
    } ,
    "remarks" :
    [
      "Copyright (c) 2016 Latin America and Caribbean Registry for Internet Numbers.",
      "LACNIC Terms of Service for this transfers log can be found at http://www.lacnic.net/web/lacnic/manual-2 point 2.3.2.18.4"
    ]
  }
}
transfer = {"transfers" : []}
indice = 0

for i in sheet.get_all_records(head=2):
    if str(i["Estado"])=="Finalizado":
        ticket = str(i["Nro. ticket"])
        oferente = str(i["Organizacion oferente"])
        receptora = str(i["Organizacion receptora"])
        id_ofe = str(i["OwnerID oferente"])
        id_rec = str(i["OwnerID receptor"])
        cc_ofe = str(i["OwnerID oferente"]).split("-")[0]
        cc_rec = str(i["OwnerID receptor"]).split("-")[0]
        fecha_fin = (datetime.strptime(str(i["Fecha fin transferencia"]), '%d/%m/%Y')).replace(tzinfo=pytz.timezone('America/Argentina/Buenos_Aires')).isoformat()
        bloques = str(i["Bloque transferido"]).split(",")
        bloque_padre = str(i["Bloque original (bloque padre)"]).split(",")
        if len(bloques)>1:
            f.write("<tr>")
            f.write("<td rowspan="+str(len(bloques))+">"+str(i["Fecha fin transferencia"])+"</td>")
            f.write("<td rowspan="+str(len(bloques))+">"+str(i["Organizacion oferente"])+"</td>")
            f.write("<td rowspan="+str(len(bloques))+">"+str(i["Organizacion receptora"])+"</td>")
            f.write("<td>"+bloques[0]+"</td></tr>")
            for j in range(1,len(bloques)):
                f.write("<tr><td>"+bloques[j]+"</td></tr>")

            transfer["transfers"].append({"ipv4nets":{ "original_set": [], "transfer_set": []}, "source_organization": {"registration_id": str(id_ofe), "log_id": str(ticket), "name": str(oferente), "country_code": str(cc_ofe)}, "recipient_organization": {"registration_id": str(id_rec), "log_id": str(ticket), "name": str(receptora), "country_code": str(cc_rec)}, "source_rir": "LACNIC", "recipient_rir": "LACNIC", "completion_date": str(fecha_fin), "description": [""], "type": {"signifier": "2.3.2.18", "description": "Policy 2.3.2.18 Intra-RIR Transfer"}})
            for k in range(0,len(bloques)):
                b = IPNetwork(bloques[k])
                p = IPNetwork(bloque_padre[k])
                start = b.network
                start_padre = p.network
                end_padre = p.broadcast
                end = b.broadcast
                transfer["transfers"][indice]["ipv4nets"]["transfer_set"].append({"start": str(start), "end": str(end)})
                transfer["transfers"][indice]["ipv4nets"]["original_set"].append({"start": str(start_padre), "end": str(end_padre)})
        else:
            bloque = str(i["Bloque transferido"])
            padre = str(i["Bloque original (bloque padre)"])
            b = IPNetwork(bloque)
            p = IPNetwork(padre)
            start_padre = p.network
            end_padre = p.broadcast
            start = b.network
            end = b.broadcast
            transfer["transfers"].append({"ipv4nets":{ "original_set": [{"start": str(start_padre), "end": str(end_padre)}], "transfer_set": [{"start": str(start), "end": str(end)}]}, "source_organization": {"registration_id": str(id_ofe), "log_id": str(ticket), "name": str(oferente), "country_code": str(cc_ofe)}, "recipient_organization": {"registration_id": str(id_rec), "log_id": str(ticket), "name": str(receptora), "country_code": str(cc_rec)}, "source_rir": "LACNIC", "recipient_rir": "LACNIC", "completion_date": str(fecha_fin), "description": [""], "type": {"signifier": "2.3.2.18", "description": "Policy 2.3.2.18 Intra-RIR Transfer"}})

            f.write("<tr>")
            f.write("<td>"+str(i["Fecha fin transferencia"])+"</td>")
            f.write("<td>"+str(i["Organizacion oferente"])+"</td>")
            f.write("<td>"+str(i["Organizacion receptora"])+"</td>")
            f.write("<td>"+str(i["Bloque transferido"])+"</td>")
            f.write("</tr>")

        indice = indice + 1


f.write("</table>")
f.write("</div></body></html>")
f.close()

st.update(transfer)
dump = json.dumps(st)
t = open("transfers.json", "w")
t.write(dump)
t.close()