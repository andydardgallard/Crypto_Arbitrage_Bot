import requests
import json
import csv
import datetime
import time

def write_csv(filename,new_line):
    with open(filename, "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

base_url="https://poloniex.com/public?command=returnChartData&currencyPair="
pairs=open('pairs_poloniex.txt').read().split("\n")
start=1303593128
end=int(time.mktime(datetime.datetime.utcnow().timetuple()))
period = 900

for i in pairs:
    ticker_url=base_url+i+"&start="+str(start)+"&end="+str(end)+"&period="+str(period)
    html_ticker=requests.get(ticker_url).text
    ticker_data=json.loads(html_ticker)
    filename=i+".txt"
    
    for j in range(len(ticker_data)):
        YYYY=str(datetime.datetime.fromtimestamp(ticker_data[j]["date"]))[:4]
        MM=str(datetime.datetime.fromtimestamp(ticker_data[j]["date"]))[5:7]
        DD=str(datetime.datetime.fromtimestamp(ticker_data[j]["date"]))[8:10]
        Date=YYYY+MM+DD
            
        HH=str(datetime.datetime.fromtimestamp(ticker_data[j]["date"]))[11:13]
        Min=str(datetime.datetime.fromtimestamp(ticker_data[j]["date"]))[14:16]
        Sec="00"
        Time=HH+Min+Sec
            
        Open = ticker_data[j]["open"]
        High = ticker_data[j]["high"]
        Low = ticker_data[j]["low"]
        Close = ticker_data[j]["close"]
        Vol =  ticker_data[j]["volume"]
            
        new_line=[Date, Time, Open, High, Low, Close, Vol]
        write_csv(filename, new_line)