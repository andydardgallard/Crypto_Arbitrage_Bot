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
#start=1303593128
end=int(time.mktime(datetime.datetime.utcnow().timetuple()))
period = 900

for i in pairs:
    filename=i+".txt"
    
    file_obj = open(filename, 'r')
    w=file_obj.readlines()
    YYYYs = int(w[len(w)-1][:4])
    MMs = int(w[len(w)-1][4:6])
    DDs = int(w[len(w)-1][6:8])
    HHs = int(w[len(w)-1][9:11])
    Mins = int(w[len(w)-1][11:13])+1
    Secs = 0
    file_obj.close()
    start = int(time.mktime(datetime.datetime(YYYYs, MMs, DDs, HHs, Mins, Secs).timetuple()))
    
    
    ticker_url=base_url+i+"&start="+str(start)+"&end="+str(end)+"&period="+str(period)
    html_ticker=requests.get(ticker_url).text
    ticker_data=json.loads(html_ticker)    
    
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

    print i