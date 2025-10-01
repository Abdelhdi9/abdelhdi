from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# API للمستخدمين (اللي عملناه سابقاً)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

