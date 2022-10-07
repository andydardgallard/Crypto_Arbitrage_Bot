import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://poloniex.com/public?command=return"
pairs=open('pairs.txt').read().split("\n")

ticker_url=base_url+"Ticker"
html_ticker=requests.get(ticker_url).text
ticker_data=json.loads(html_ticker)

for i in ticker_data:
    if i in pairs:
        depth_url=base_url+"OrderBook&currencyPair="+i+"&depth=10"    
        html_depth=requests.get(depth_url).text
        depth_data=json.loads(html_depth)
    
        q=0
        w=[]
        e=[]
        for j in depth_data["bids"]:    
            q=q+j[1]
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
        for j in depth_data["asks"]:    
            q=q+j[1]
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
    
        #print i, ticker_data[i]["lowestAsk"], ticker_data[i]["highestBid"], asks, bids
        new_line=["poloniex", i.replace("_",""), str(ticker_data[i]["lowestAsk"]).replace(".",","), 
                  str(ticker_data[i]["highestBid"]).replace(".",","), str(asks).replace(".",","), str(bids).replace(".",",")]
        
        print new_line
        write_csv(new_line)