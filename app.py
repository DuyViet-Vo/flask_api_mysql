from flask import Flask,request, jsonify
import json
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'book_api'

mysql = MySQL(app)

@app.route('/books' , methods=['GET', 'POST'])
def books():
    cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn = mysql.connection
    if request.method == "GET":
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        return jsonify(books)
    
    if request.method == "POST":
        new_author = request.form['author']
        new_language = request.form['language']
        new_title = request.form['title']
        sql = """ INSERT INTO books (author,language,title) VALUES (%s,%s,%s)"""
        cur.execute(sql,(new_author,new_language,new_title))
        conn.commit()
        return f"Book with the id : {cur.lastrowid} created successfully"
    
@app.route('/books/<int:id>', methods=['GET','PUT', 'DELETE'])
def book(id):
    cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn = mysql.connection
    if request.method == 'GET':
        cur.execute("SELECT * FROM books WHERE id= %s",(id,))
        books = cur.fetchall()
        return jsonify(books),200

    if request.method == 'PUT':
        sql = """ UPDATE books SET author = %s,language = %s ,title = %s WHERE id= %s"""
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        
        update_book= {
            'id': id,
            'author': author,
            'language': language,
            'title': title,
        }
        cur.execute(sql,(author,language,title,id))
        conn.commit()
        return jsonify(update_book)
        
    if request.method == 'DELETE':
        sql = """
            DELETE FROM books WHERE id= %s
        """  
        cur.execute(sql,(id,))
        conn.commit()
        return "The book with id: {} has been deleted".format(id),200
        
if __name__ == '__main__':
    app.run(debug=True)
    
