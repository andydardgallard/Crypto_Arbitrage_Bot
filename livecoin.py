import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://api.livecoin.net/exchange/"

ticker_url=base_url+"ticker"
depth_url=base_url+"all/order_book"

html_ticker=requests.get(ticker_url).text
html_depth=requests.get(depth_url).text

ticker_data=json.loads(html_ticker)
depth_data=json.loads(html_depth)

for i in ticker_data:
    try:
        q=0
        w=[]
        e=[]
        for j in depth_data[i["symbol"]]["bids"]:
            q=q+float(j[1])
            if q>pos:
                w.append(j)
            if q<pos:
                e.append(j)     
            
        r=0
        t=0
        for j in e:
            r=float(j[0])*float(j[1])+r
            t=float(j[1])+t    
        r=float(w[0][0])*(pos-t)+r
        bids=r/pos 
    
    except:
        bids=i["best_bid"]
        
    try:
        q=0
        w=[]
        e=[]
        for j in depth_data[i["symbol"]]["asks"]:
            q=q+float(j[1])
            if q>pos:
                w.append(j)
            if q<pos:
                e.append(j)     
            
        r=0
        t=0
        for j in e:
            r=float(j[0])*float(j[1])+r
            t=float(j[1])+t    
        r=float(w[0][0])*(pos-t)+r
        asks=r/pos      
    
    except:
        asks=i["best_ask"]    
        
        
    new_line = ["livecoin", str(i["symbol"]).replace("/",""), str(i["best_ask"]).replace(".",","), str(i["best_bid"]).replace(".",","), 
                str(asks).replace(".",","), str(bids).replace(".",",")]
    
    print new_line
    write_csv(new_line)