
import sqlite3
from flask_cors import CORS
import os
from flask import Flask, flash, jsonify, request, redirect, send_from_directory, url_for, session, render_template
from werkzeug.utils import secure_filename
import time
import json


app = Flask(__name__,
            static_url_path='', 
            static_folder='/',
            template_folder='/')
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/register", methods = ['POST'])
def register():
    data = request.get_json()
    #password =request.get_json("password")
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    try:
        
        cursor.execute("insert into users values(?,?)",(data["userName"], data["password"]))
        con.commit()
        response = "Kütüphane Sistemine Hoşgeldiniz!"
    except:
        response = "Kullanıcı Adı Kullanılmaktadır!"
    finally:
        return response



@app.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    try:
        cursor.execute("select user_name from users where user_name =? and password=?",(data["userName"], data["password"]))
        login_resp = cursor.fetchall()
        if login_resp:
            response = "True"
        else:
            response = "False"
    except:
        response =" Bir Hata Oluştu"
    
    finally:
        return response
    

@app.route("/addbookresim", methods = ['POST'])
def addBook():
    
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    # if 'file' not in request.files:
    #     return "redirect(request.url)"
      
    
    try:
        file = request.files['file'] 
        filename = (file.filename.split('.')[0] + str(time.time()).replace('.','_')).replace(' ','_') +'.' +file.filename.split('.')[-1]
        destination="/".join(['photos', filename])
        file.save(destination)

        cursor.execute("insert into kitaplar (kitap_adi, yazar, adres, path, kullanici, ucret) values(?,?,?,?,?,?)",(request.form['bookName'],request.form['yazar'], request.form['adress'],'http://127.0.0.1:5000/' + destination,request.form['username'],request.form['ucret']))
        con.commit()
        response="Eklendi"
    except:
        response =" Bir Hata Oluştu"
    
    finally:
        return response
    


@app.route("/getBooks", methods = ['POST'])
def get_books():
    data = request.get_json()
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    kitap_data = []
    cursor.execute(f"select kitap_adi, yazar, adres, path, kullanici, ucret, id from kitaplar where kitap_adi like '%{data['keyword']}%' or yazar like '%{data['keyword']}%'")
    kitap_data = cursor.fetchall()
    
    try:
        
        response =  jsonify(kitap_data)
        
    except:
        response =" Bir Hata Oluştu"
    
    finally:
        return response

@app.route("/getBook", methods = ['POST'])
def get_book():
    data = request.get_json()
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    kitap_data = []
    cursor.execute("select kitap_adi, yazar, adres, path, kullanici, ucret, id from kitaplar where id = ?",(data['id'],))
    kitap_data = cursor.fetchall()
    
    try:
        
        response =  jsonify(kitap_data)
        
    except:
        response =" Bir Hata Oluştu"
    
    finally:
        return response


@app.route("/sendmessage", methods = ['POST'])
def send_message():
    data = request.get_json()
    #password =request.get_json("password")
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    try:
        
        cursor.execute("insert into messages values(?,?,?)",(data["gonderen"], data["alan"],data["icerik"]))
        con.commit()
        response =  "mesaj gonderildi"
    except:
        response = "Mesaj Gonderilemiyor!"
    finally:
        return response
    
@app.route("/getmessages", methods = ['POST'])
def get_messages():
    data = request.get_json()
    #password =request.get_json("password")
    con = sqlite3.connect("flask1db.db")
    cursor = con.cursor()
    try:
        
        cursor.execute("select * from messages where (gonderen = ? and alan = ?) or (gonderen = ? and alan = ?)",(data["gonderen"], data["alan"],data["alan"],data["gonderen"]))
        con.commit()
        response =  cursor.fetchall()
        print(response)
    except:
        response = "error"
    finally:
        return jsonify(response)



@app.route('/reports/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)

if __name__ == "__main__":
    app.run(debug=True)