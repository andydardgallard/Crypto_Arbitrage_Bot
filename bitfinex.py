import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://api.bitfinex.com/v1/"
pairs=open('pairs.txt').read()
pairs=pairs.lower().replace("_","").split("\n")

symbol_url=base_url+"symbols"
html_symbol=requests.get(symbol_url).text
symbol_data=json.loads(html_symbol)
#print symbol_data

for i in symbol_data:
    if i in pairs:
        ticker_url=base_url+"pubticker/"+i
        html_ticker=requests.get(ticker_url).text
        ticker_data=json.loads(html_ticker)        

        depth_url=base_url+"book/"+i
        html_depth=requests.get(depth_url).text
        depth_data=json.loads(html_depth)

        q=0
        w=[]
        e=[]
        for j in depth_data["bids"]:
            q=q+float(j["amount"])
            if q>pos:
                w.append(j)
            if q<pos:
                e.append(j)      
        r=0
        t=0
        for j in e:
            r=float(j["price"])*float(j["amount"])+r
            t=float(j["amount"])+t    
        r=float(w[0]["price"])*(pos-t)+r
        bids=r/pos
    
        q=0
        w=[]
        e=[]
        for j in depth_data["asks"]:
            q=q+float(j["amount"])
            if q>pos:
                w.append(j)
            if q<pos:
                e.append(j)    
        r=0
        t=0
        for j in e:
            r=float(j["price"])*float(j["amount"])+r
            t=float(j["amount"])+t    
        r=float(w[0]["price"])*(pos-t)+r
        asks=r/pos     
    
        new_line=["bitfinex", i.upper(), str(ticker_data["ask"]).replace(".",","), str(ticker_data["bid"]).replace(".",","), 
                  str(asks).replace(".",","), str(bids).replace(".",",")]
        print new_line
        write_csv(new_line)