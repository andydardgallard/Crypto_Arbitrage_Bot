import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://yobit.net/api/3/"
pairs=open('pairs_yobit.txt').read().split("\n")

symbol_url=base_url+"info"
html_symbol=requests.get(symbol_url).text
symbol_data=json.loads(html_symbol)

for i in symbol_data['pairs']:
    if i.upper() in pairs:
        ticker_url=base_url+"ticker/"+i
        html_ticker=requests.get(ticker_url).text
        ticker_data=json.loads(html_ticker)
    
        depth_url=base_url+"depth/"+i+"?limit=10"
        html_depth=requests.get(depth_url).text
        depth_data=json.loads(html_depth)
    
        try:
            q=0
            w=[]
            e=[]
            for j in depth_data[i]["bids"]:
                q=q+j[1]
                if q>pos:
                    w.append(j)
                if q<pos:
                    e.append(j)      
            r=0
            t=0
            for j in e:
                r=j[0]*j[1]+r
                t=j[1]+t    
            r=w[0][0]*(pos-t)+r
            bids=r/pos
        except:
            bids=ticker_data[i]['buy']

        try:
            q=0
            w=[]
            e=[]
            for j in depth_data[i]["asks"]:
                q=q+j[1]
                if q>pos:
                    w.append(j)
                if q<pos:
                    e.append(j)    
            r=0
            t=0
            for j in e:
                r=j[0]*j[1]+r
                t=j[1]+t    
            r=w[0][0]*(pos-t)+r
            asks=r/pos
        except:
            asks=ticker_data[i]['sell']
    
        new_line=['yobit', i.upper().replace("_",""), str(ticker_data[i]['sell']).replace(".",","), 
                  str(ticker_data[i]['buy']).replace(".",","), str(asks).replace(".",","), str(bids).replace(".",",")]
        
        print new_line
        write_csv(new_line)