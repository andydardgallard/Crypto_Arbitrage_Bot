import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://cex.io/api/"

ticker_url=base_url+"tickers/USD/RUB/BTC"
html_ticker=requests.get(ticker_url).text
ticker_data=json.loads(html_ticker)

for i in ticker_data["data"]:
    depth_url=base_url+"order_book/"+i["pair"].replace(":","/")+"/?depth=10"
    html_depth=requests.get(depth_url).text
    depth_data=json.loads(html_depth)
    
    q=0
    w=[]
    e=[]
    for j in depth_data['bids']:    
        q=q+float(j[1])
        if q>pos:
            w.append(j)
        if q<pos:
            e.append(j)  
    r=0
    t=0
    for j in e:
        r=float(j[0])*j[1]+r
        t=j[1]+t    
    r=float(w[0][0])*(pos-t)+r
    bids=r/pos
    
    q=0
    w=[]
    e=[]
    for j in depth_data['asks']:    
        q=q+float(j[1])
        if q>pos:
            w.append(j)
        if q<pos:
            e.append(j)  
    r=0
    t=0
    for j in e:
        r=float(j[0])*j[1]+r
        t=j[1]+t    
    r=float(w[0][0])*(pos-t)+r
    asks=r/pos
    
    new_line=["cexio", i["pair"].replace(":",""), str(i["ask"]).replace(".",","), str(i["bid"]).replace(".",","), 
              str(asks).replace(".",","), str(bids).replace(".",",")]
    
    print new_line
    
    write_csv(new_line)