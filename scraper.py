import requests, csv
from bs4 import BeautifulSoup
import mysql.connector

with open('side-effects.tsv','r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    ids = []
    for row in reader:
        ids.append(row['drugbank_id'])
    db_id = set(ids)
    print(db_id)
cf = open("medicines.tsv","w")
for each_id in db_id:
    print(each_id)
    r = requests.get("https://drugbank.ca/drugs/"+each_id)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    name = soup.find("h1" , class_ = "align-self-center mr-4").text
    syns = soup.find("ul", class_ = "list-unstyled table-list-break")
    synonyms = 'null'
    if syns is not None:
        synonyms = syns.text
    synonyms = synonyms.replace("\n","|")
    print(synonyms)
    ind = soup.find("ul", class_ = "list-unstyled table-list")
    uses = 'null'
    if ind is not None:
        uses = ind.text
    uses = uses.replace("\n","|")
    row = each_id+"\t"+name+"\t"+synonyms+"\t"+uses
    print(row)
    cf.write(row)
    cf.write("\n")
