import requests
import json
import codecs
import csv
import numpy as np

def write_csv(new_line):
    with open("common.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

pos=0.25
base_url="https://btc-e.nz/api/3/"
pairs="btc_rur-btc_usd-dsh_btc-dsh_eth-dsh_ltc-dsh_usd-eth_btc-eth_ltc-eth_usd-ltc_btc-ltc_usd-nmc_btc-nmc_usd-nvc_btc-nvc_usd-ppc_btc-ppc_usd"

ticker_url=base_url+"ticker/"+pairs
depth_url=base_url+"depth/"+pairs

html_ticker=requests.get(ticker_url).text
html_depth=requests.get(depth_url).text

ticker_data=json.loads(html_ticker)
depth_data=json.loads(html_depth)

#print "Start"

for i in ticker_data:
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
    
    new_line=["btc-e", str(i).replace("_","").upper(), str(ticker_data[i]["buy"]).replace(".",","), 
              str(ticker_data[i]["sell"]).replace(".",","), str(asks).replace(".",","), str(bids).replace(".",",")]
    #new_line=[str(i), str(ticker_data[i]["buy"]), str(ticker_data[i]["sell"]), str(asks), str(bids)]
    
    print new_line                  
    write_csv(new_line)
    #print i, ticker_data[i]["buy"], ticker_data[i]["sell"], asks, bids

    #print "Processing"