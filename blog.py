from flask import Flask, render_template, request
import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    sozluk = dict()
    sozluk["elma"]="apple"
    sozluk["su"]="water"
    sozluk["siyah"]="black"
    return render_template("layout.html",sozluk=sozluk)

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
    

if __name__ == "__main__":
    app.run(debug=True)