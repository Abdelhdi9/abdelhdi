from flask import Flask, request, render_template, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# الاتصال بقاعدة البيانات
conn = psycopg2.connect(
    "postgresql://myuser:GhqaE0hRm8rM2fL026X8QEu0wQi599F2@dpg-d3eigqogjchc738p4mqg-a.frankfurt-postgres.render.com/mydb_zpih"
)
cur = conn.cursor()

# الصفحة الرئيسية
@app.route('/')
def home():
    # تسجيل الزيارة
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    cur.execute(
        "INSERT INTO visits (ip_address, user_agent) VALUES (%s, %s);",
        (ip_address, user_agent)
    )
    conn.commit()
    
    return render_template('index.html')

# API للمستخدمين
users = []

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(user)
    return jsonify(user), 201

# API للزيارات
@app.route('/visits', methods=['GET'])
def get_visits():
    cur.execute("SELECT id, ip_address, user_agent, visit_time FROM visits ORDER BY visit_time DESC;")
    rows = cur.fetchall()
    visits_list = []
    for visit in rows:
        visits_list.append({
            "id": visit[0],
            "ip_address": visit[1],
            "user_agent": visit[2],
            "visit_time": str(visit[3])
        })
    return jsonify(visits_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

