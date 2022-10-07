import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://api.exmo.com/v1/"

ticker_url=base_url+"ticker/"
html_ticker=requests.get(ticker_url).text
ticker_data=json.loads(html_ticker)

for i in ticker_data:
    depth_url=base_url+"order_book/?pair="+i+"&limit=10"
    html_depth=requests.get(depth_url).text
    depth_data=json.loads(html_depth)
    
    try:
        q=0
        w=[]
        e=[]
        for j in depth_data[i]['bid']:    
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
        bids=ticker_data[i]['buy_price']
        
    try:
        q=0
        w=[]
        e=[]
        for j in depth_data[i]['ask']:    
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
        asks=ticker_data[i]['sell_price']
        
    new_line=["exmo", str(i).replace("_",""), str(ticker_data[i]['sell_price']).replace(".",","), 
              str(ticker_data[i]['buy_price']).replace(".",","), str(asks).replace(".",","), str(bids).replace(".",",")]
    
    print new_line
    write_csv(new_line)