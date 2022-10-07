import requests
import json
import csv

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://bittrex.com/api/v1.1/public/"
pairs=open('pairs.txt').read()
pairs=pairs.replace("_","-").split("\n")

symbol_url=base_url+"getmarkets"
html_symbol=requests.get(symbol_url).text
symbol_data=json.loads(html_symbol)

for i in symbol_data['result']:
    if i['MarketName'] in pairs:
        ticker_url=base_url+"getticker?market="+i['MarketName']
        html_ticker=requests.get(ticker_url).text
        ticker_data=json.loads(html_ticker)
    
        depth_url=base_url+"getorderbook?market="+i['MarketName']+"&type=both&depth=10"   
        html_depth=requests.get(depth_url).text
        depth_data=json.loads(html_depth)
    
        try:
            q=0
            w=[]
            e=[]
            for j in depth_data['result']['buy']:
                q=q+j['Quantity']
                if q>pos:
                    w.append(j)
                if q<pos:
                    e.append(j) 
            r=0
            t=0
            for j in e:
                r=j["Rate"]*j['Quantity']+r
                t=j['Quantity']+t    
            r=w[0]["Rate"]*(pos-t)+r
            bids=r/pos
        except:
            bids=ticker_data['result']["Bid"]
        
        try:
            q=0
            w=[]
            e=[]
            for j in depth_data['result']['sell']:
                q=q+j['Quantity']
                if q>pos:
                    w.append(j)
                if q<pos:
                    e.append(j) 
            r=0
            t=0
            for j in e:
                r=j["Rate"]*j['Quantity']+r
                t=j['Quantity']+t    
            r=w[0]["Rate"]*(pos-t)+r
            asks=r/pos
        except:
            asks=ticker_data['result']["Ask"]
        
        new_line = ['bittrex', i['MarketName'].replace("-",""), str(ticker_data['result']["Ask"]).replace(".",","), 
                    str(ticker_data['result']["Bid"]).replace(".",","), str(asks).replace(".",","), str(bids).replace(".",",")]
        print new_line
        write_csv(new_line)