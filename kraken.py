import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://api.kraken.com/0/public/"

pairs=open('pairs.txt').read()
pairs=pairs.replace("_","").replace("BTC","XBT").split("\n")

symbol_url=base_url+"AssetPairs"
html_symbol=requests.get(symbol_url).text
symbol_data=json.loads(html_symbol)

symbols=[]
z=0
for i in symbol_data['result']:   
    symbols.append(symbol_data['result'][i]["altname"])    

symbols=str(symbols).replace("[","").replace("]",'').replace("u",'').replace(" ","").replace("'","")

ticker_url=base_url+"Ticker?pair="+symbols
html_ticker=requests.get(ticker_url).text
ticker_data=json.loads(html_ticker)

for i in ticker_data['result']:
    if symbol_data['result'][i]["altname"] in pairs:
        depth_url=base_url+"Depth?pair="+symbol_data['result'][i]["altname"]+'&count=10'
        html_depth=requests.get(depth_url).text
        depth_data=json.loads(html_depth)
    
        try:
            q=0
            w=[]
            e=[]
            for j in depth_data['result'][i]['bids']:    
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
        except:
            bids=ticker_data['result'][i]['b'][0]        
        
        try:
            q=0
            w=[]
            e=[]
            for j in depth_data['result'][i]['asks']:    
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
        except:
            asks=ticker_data['result'][i]['a'][0]
        
        new_line=["kraken", symbol_data['result'][i]["altname"].replace("XBT","BTC"), str(ticker_data['result'][i]['a'][0]).replace(".",","), 
                  str(ticker_data['result'][i]['b'][0]).replace(".",","), str(asks).replace(".",","), str(bids).replace(".",",")]
        
        print new_line
        write_csv(new_line)