from flask import Flask, render_template, request, redirect
import mysql.connector
import random
import os
from urllib.parse import urlparse
 
app = Flask(__name__)
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:forhxRTvzgLtDTsvCegVXnSkvLkGTVYE@hopper.proxy.rlwy.net:50033/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:forhxRTvzgLtDTsvCegVXnSkvLkGTVYE@hopper.proxy.rlwy.net:50033/railway"
 
url = urlparse(db_url)
 
# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)
 
cursor = db.cursor()
app = Flask(__name__)



@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    return render_template("index.html", customers=data)


# CREATE
@app.route('/add', methods=['POST'])
def add_customer():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

   
    cursor = db.cursor()
    query = "INSERT INTO customer (name, mobile, amount, location) VALUES (%s,%s,%s,%s)"
    values = (name,mobile,amount,location)
    cursor.execute(query, values)
    db.commit()

    return redirect('/')


# DELETE
@app.route('/delete/<mobile>')
def delete_customer(mobile):
    cursor = db.cursor()
    cursor.execute("DELETE FROM customer WHERE mobile=%s", (mobile,))
    db.commit()
    return redirect('/')


# UPDATE PAGE
@app.route('/edit/<mobile>')
def edit_customer(mobile):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customer WHERE mobile=%s", (mobile,))
    data = cursor.fetchone()
    return render_template("edit.html", customer=data)


# UPDATE
@app.route('/update/<mobile>', methods=['POST'])
def update_customer(mobile):
    name = request.form['name']
    new_mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    cursor = db.cursor()
    query = """
        UPDATE customer 
        SET name=%s, mobile=%s, amount=%s, location=%s
        WHERE mobile=%s
    """
    values = (name, new_mobile, amount, location, mobile)
    cursor.execute(query, values)
    db.commit()

    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
