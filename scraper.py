import requests, csv
from bs4 import BeautifulSoup
from lxml import html

with open('side-effects.tsv','r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    ids = []
    for row in reader:
        ids.append(row['drugbank_id'])
    db_id = set(ids)
    print(db_id)
medicines = open("medicines.tsv","w")
names = open("names.tsv", "w")
symptoms = open("categories.tsv","w")
comman_brands = open("brands.tsv","w")
for each_id in db_id:
    print(each_id)
    r = requests.get("https://drugbank.ca/drugs/"+each_id)
    page = r.text
    tree = html.fromstring(page)
    soup = BeautifulSoup(page, "lxml")
    try:
        
        name = 'Null'
        n = soup.find("h1" , class_ = "align-self-center mr-4")
        if n is not None:
            name = soup.find("h1" , class_ = "align-self-center mr-4").text
        
        syns = soup.find("ul", class_ = "list-unstyled table-list-break")
        synonyms = 'Null'
        if syns is not None:
            synonyms = syns.text
        
    
        uses = 'Null'
        description = 'Null'
        des = tree.xpath("/html/body/main/div/div[4]/dl[1]/dd[5]/p/text()")
        if des[0] is not None:
            print(des[0])
        description = des[0]
        
        des2 = tree.xpath("/html/body/main/div/div[4]/dl[2]/dd[3]/p/text()")
        if des2[0] is not None:
            description = description +" "+des2[0]
        description = description.replace("\n"," ")
        ind = soup.find("ul", class_ = "list-unstyled table-list")
        if ind is not None:
            uses = ind.text
        brands = tree.xpath("/html/body/main/div/div[4]/dl[1]/dd[14]/span/span/span[@class = 'separated-list-item']/text()")
        print(brands)
    except Exception:
        pass
    medicines_row = each_id+"\t"+name+"\t"+description
    medicines.write(medicines_row)
    medicines.write("\n")

    for brand in brands:
        comman_brands.write(brand+"\t"+each_id)
        comman_brands.write("\n")
    
    all_synonyms = synonyms.split("\n")
    for synonym in all_synonyms:
        names.write(synonym+"\t"+each_id)
        names.write("\n")
        
    all_symptoms = uses.split("\n")
    for symptom in all_symptoms:
        symptoms.write(symptom+"\t"+each_id)
        symptoms.write("\n")
symptoms.close()
medicines.close()
names.close()
    #print(row)
    
