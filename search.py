from flask import Flask, request, render_template
import mysql.connector
app = Flask(__name__, static_url_path='/static')

conn = mysql.connector.connect(host = "localhost", database = "MediSearch", user = "root", password = "")


@app.route('/search',methods=['GET', 'POST'])
def search_name():
    name = ""
    if request.args.get('query', None):
        name = request.args['query']
    cursor = conn.cursor(buffered = True)
    query = "SELECT Name,ID FROM Medicine WHERE ID IN (SELECT ID FROM Name WHERE Name LIKE "+"'%"+name+"%') OR Name LIKE "+"'%"+name+"%'"
    cursor.execute(query)
    row = cursor.fetchone()

    while row is not None:
        row = "<a href=\"http://localhost:5000/page/"+row[1]+"\">"+row[0]+"</a>"
        return row
        row = cursor.fetchone()
    if row is None:
        return "No results found."
    cursor.close()

@app.route('/page/<medi>')
def page(medi):
    cursor = conn.cursor(buffered = True)
    query = "SELECT Name,Description FROM Medicine WHERE ID='"+medi+"'"
    side_effects = "SELECT Side_effect from SideEffect WHERE ID='"+medi+"'"
    comman_names = "SELECT Name from Brand WHERE ID ='"+medi+"'"
    categories = "SELECT Name from Name WHERE ID ='"+medi+"'"
    url = "http://drugbank.ca/"+medi
    cursor.execute(query)
    row = cursor.fetchone()
    
    if row is None:
        return "No results found."
    else:
        #Fetch side effects
        cursor.execute(side_effects)
        effects = cursor.fetchone()
        all_effects = ""
        
        while effects is not None:
            all_effects = all_effects + effects[0] + ", "
            effects = cursor.fetchone()

        #Remove the last comma
        all_effects = all_effects[:len(all_effects)-2]

        #Fetch comman names
        cursor.execute(comman_names)
        brand = cursor.fetchone()
        all_brands = ""
        while brand is not None:
            all_brands = all_brands + brand[0] + ", "
            brand = cursor.fetchone()

        results = {"Name":row[0],"Description":row[1],"Side Effects":all_effects,"Source":url}

        if len(all_brands) > 0:
            results["Comman Name"] = all_brands

        #Fetch categories
        cursor.execute(categories)
        cate = cursor.fetchone()
        all_categories = ""
        while cate is not None:
            all_categories = all_categories + cate[0] + ", "
            cate = cursor.fetchone()

        if len(all_categories) > 0:
            results["Synonyms"] = all_categories
            
        return render_template('page.html',result=results)
        #return "<h2>"+row[0]+"</h2><br>"+"<h2>Description: </h2>"+row[1]+"<br> <h2>Side Effects</h2>"+all_effects
    cursor.close()

if __name__ == '__main__':
   app.run()
