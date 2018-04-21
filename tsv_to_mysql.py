import mysql.connector as ms
import csv
conn = ms.connect(host = 'localhost', database = 'MediSearch', user = 'root', password = '')
if conn.is_connected():
    print("Connected")
with open('side-effects.tsv') as f:
    reader = csv.reader(f,delimiter = '\t')
    cursor = conn.cursor()
    for row in reader:
        query = "INSERT INTO SideEffect (Side_effect, ID) VALUES (%s,%s)"
        vals = (row[3],row[0])
        cursor.execute(query,vals)
        conn.commit()
cursor.close()
conn.close()
