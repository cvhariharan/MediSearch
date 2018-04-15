import mysql.connector as ms
import csv
conn = ms.connect(host = 'localhost', database = 'MediSearch', user = 'root', password = '')
if conn.is_connected():
    print("Connected")
with open('brands.tsv') as f:
    reader = csv.reader(f,delimiter = '\t')
    cursor = conn.cursor()
    for row in reader:
        query = "INSERT INTO Brand (Name,ID) VALUES (%s,%s)"
        vals = (row[0],row[1])
        cursor.execute(query,vals)
        conn.commit()
cursor.close()
conn.close()
