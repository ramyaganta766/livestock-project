from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import pickle

app = Flask(__name__)
app.secret_key = "secret123"

# LOAD MODEL
model = pickle.load(open("model.pkl", "rb"))

# DATABASE
def get_db():
    return sqlite3.connect('users.db')

def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
''')
    conn.commit()
    conn.close()
create_table()

# ================= HOME =================
@app.route('/')
def home():
    return render_template('login.html')



# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
      email = request.form['email']
password = request.form['password']

        # 🔥 ADMIN LOGIN
        if username == "admin" and password == "admin123":
            session['admin'] = True
            return redirect('/admin-dashboard')

        # NORMAL USER LOGIN
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['user'] = email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Login")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
      
       email = request.form['email']
       password = request.form['password']


        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

# ================= ADMIN DASHBOARD =================

@app.route('/admin-dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template('admin_dashboard.html', users=users)

# ================= ABOUT =================
@app.route('/about')
def about():
    return render_template('about.html')

# ================= CONTACT =================
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ================= PREDICT PAGE =================
@app.route('/predict')
def predict():
    if 'user' not in session:
        return redirect('/')
    return render_template('predict.html')

# ================= PREDICTION =================
@app.route('/predict-image', methods=['POST'])
def predict_image():

    animal = request.form['animal']

    # ✅ ANIMAL MAP
    animal_map = {"Cow":0,"Goat":1,"Sheep":2,"Buffalo":3,"Hen":4}
    animal_val = animal_map.get(animal, 0)

    # ✅ SYMPTOM MAPPING (IMPORTANT)
    fever = 1 if request.form.get('fever') else 0
    appetite = 1 if request.form.get('appetite') else 0
    weakness = 1 if request.form.get('weakness') else 0

    # ignore others (cough, diarrhea, etc. not in dataset)

    # ✅ INPUTS
    age = float(request.form.get('age', 2))
    vaccine = 1 if request.form.get('vaccine') == "Yes" else 0

    # ✅ MODEL INPUT (MATCH YOUR DATASET)
    input_data = [[animal_val, age, fever, appetite, weakness, vaccine]]

    # ✅ PREDICT
    prediction = model.predict(input_data)[0]

    # ✅ CONFIDENCE (if model supports)
    try:
        confidence = max(model.predict_proba(input_data)[0]) * 100
    except:
        confidence = 85

    # ✅ ADVICE LOGIC
    if prediction.lower() == "healthy":
        advice = "No disease detected. Keep monitoring."
    else:
        advice = "Consult veterinarian immediately."

    return jsonify({
        "disease": prediction,
        "advice": advice,
        "confidence": round(confidence, 2)
    })

# ================= STATISTICS =================
@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)