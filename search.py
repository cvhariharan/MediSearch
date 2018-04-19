from flask import Flask, request
import mysql.connector
app = Flask(__name__)

conn = mysql.connector.connect(host = "localhost", database = "MediSearch", user = "root", password = "")


@app.route('/<name>')
def search_name(name):
    cursor = conn.cursor()
    query = "SELECT Name,ID FROM Medicine WHERE ID IN (SELECT ID FROM Name WHERE Name LIKE "+"'%"+name+"%') OR Name LIKE "+"'%"+name+"%'"
    cursor.execute(query)
    row = cursor.fetchone()

    while row is not None:
        row = "<a href=\"http://localhost:5000/page/"+row[1]+"\">"+row[0]+"</a>"
        return row
        row = cursor.fetchone()
    if row is None:
        return "No results found."
    conn.close()

@app.route('/page/<medi>')
def page(medi):
    cursor = conn.cursor()
    query = "SELECT Name,Description FROM Medicine WHERE ID='"+medi+"'"
    side_effects = "SELECT Side_effect from SideEffect WHERE ID='"+medi+"'"
    cursor.execute(query)
    row = cursor.fetchone()
    
    if row is None:
        return "No results found."
    else:
        cursor.execute(side_effects)
        effects = cursor.fetchone()
        all_effects = ""
        
        while effects is not None:
            all_effects = all_effects + "<br>" + effects[0]
            effects = cursor.fetchone()
            
        return "<h2>"+row[0]+"</h2><br>"+"<h2>Description: </h2>"+row[1]+"<br> <h2>Side Effects</h2>"+all_effects
    conn.close()

if __name__ == '__main__':
   app.run()
