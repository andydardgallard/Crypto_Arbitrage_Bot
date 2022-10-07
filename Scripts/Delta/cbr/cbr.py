import datetime
import requests
from bs4 import BeautifulSoup as bs
import csv
import codecs

def write_csv(new_line):
    with open("cbr.csv", "a" ) as fout:
        writer=csv.writer(fout)
        writer.writerow((new_line))

count = 1
base_url='https://www.cbr.ru/statistics/UDStat.aspx?'
Year=range(2009, 2014)
Month=range(1,13)

a=[0,7,8,15,40,47,72,79,96,103,120,135,144,159]

for i in Year:
    for j in Month:
        qyery_part='Month='+str(j)+'&Year='+str(i)+'&TblID=4-8'
        url=base_url+qyery_part
        html=requests.get(url).text
        soup=bs(html, 'lxml')
        try:            
            for k in a:
                new_line=[count, i, j, codecs.encode(soup.find_all('td')[k].text.strip(), "Windows-1251")]
                write_csv(new_line)
                print new_line
                count = count+1
        except:
            pass        
"_________________________________________________________________________________________________"
        
Year=range(2014, datetime.datetime.now().year+1)

a=[0,7,8,15,32,39,56,63,80,87,104,119,128,143]

for i in Year:
    for j in Month:
        qyery_part='Month='+str(j)+'&Year='+str(i)+'&TblID=4-8'
        url=base_url+qyery_part
        html=requests.get(url).text
        soup=bs(html, 'lxml')
        try:            
            for k in a:
                new_line=[count, i, j, codecs.encode(soup.find_all('td')[k].text.strip(), "Windows-1251")]
                write_csv(new_line)
                print new_line
                count = count+1
        except:
            pass