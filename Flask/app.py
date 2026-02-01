from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import requests 
import sqlite3
import json
from serpapi import GoogleSearch
from flask import jsonify
from math import radians, cos, sin, asin, sqrt



app = Flask(__name__)
app.secret_key = 'Mashu'
admin_password="admin123"

# Loading saved models
heart_disease_model = pickle.load(open('tuned_logistic_regression_model.pkl', 'rb'))
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))
def distance_km(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))

@app.route('/')
def start():
    return render_template('start.html')

def get_db_connection():
    conn = sqlite3.connect('health_compass.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        mail = request.form['mail']
        location = request.form['location']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()

        # Inserting new user into users table
        try:
            c.execute("INSERT INTO users (name, age, gender, mail, location, password) VALUES (?, ?, ?, ?, ?, ?)",
                      (name, age, gender, mail, location, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('User with this email already exists.', 'danger')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid name or password. Please try again.', 'danger')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    print(flash('You have been logged out.', 'info'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/heart-disease', methods=['GET', 'POST'])
def heart_disease():
    if request.method == 'POST':
        # Extract features from form input
        features = [float(request.form.get(key)) for key in request.form.keys()]
        final_features = np.array([features])
        
        # Make prediction
        prediction = heart_disease_model.predict(final_features)[0]

        # prediction result
        if prediction == 1:
            result = "You are likely to have heart disease. Consult specialist doctors (cardiologists)."
            alert=True
        else:
            result = "You are not likely to have heart disease. However, follow tips and tricks to maintain your health."
            alert=False

        health_parameters = str(request.form.to_dict())

        # Store health parameters in the database for the logged-in user
        if 'user_id' in session:
            user_id = session['user_id']
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO health_data (user_id, health_parameters, result, type) VALUES (?, ?, ?, ?)",
                      (user_id, health_parameters, result, "Heart Disease"))
            conn.commit()
            conn.close()
        else:
            flash('Please log in to save your results.', 'warning')
            return redirect(url_for('login'))

        return render_template('heart_disease.html', result=result, alert=alert)
    return render_template('heart_disease.html')

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'POST':
        # Extract features from form input
        features = [float(request.form.get(key)) for key in request.form.keys()]
        final_features = np.array([features])

        # Make prediction
        prediction = diabetes_model.predict(final_features)[0]

        # Handling prediction result
        if prediction == 1:
            result = "You are likely to have diabetes. Consult specialist doctors."  
            alert=True
        else:
            result = "You are not likely to have diabetes. However, follow tips and tricks to maintain your health."
            alert=False

        health_parameters = str(request.form.to_dict())

        # Store health parameters in the database for the logged-in user
        if 'user_id' in session:
            user_id = session['user_id']
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO health_data (user_id, health_parameters, result, type) VALUES (?, ?, ?, ?)",
                      (user_id, health_parameters, result, "Diabetes"))
            conn.commit()
            conn.close()
        else:
            flash('Please log in to save your results.', 'warning')
            return redirect(url_for('login'))

        return render_template('diabetes.html', result=result, alert=alert)
    return render_template('diabetes.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/stat_doctors')
def stat_doctors():
    return render_template('stat_doctors.html')

@app.route('/find_doctors')
def find_doctors():
    return render_template('find_doctors.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nearby_doctors', methods=['GET', 'POST'])
def nearby_doctors():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        api_key = '99130af515e2f1bb573265b393eacd91' 
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Doctors+{search_term}&key={api_key}"

        try:
            response = requests.get(url)
            data = response.json()
            if data.get('status') == 'OK':
                doctors = data.get('results', [])
                return render_template('find_doctors.html', doctors=doctors)
            else:
                return render_template('find_doctors.html', error="Failed to retrieve data. Please try again.")
        except Exception as e:
            return render_template('find_doctors.html', error=f"An error occurred: {e}")
    return render_template('find_doctors.html')


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Route to delete a user by ID"""
    conn = get_db_connection()
    c = conn.cursor()

    # Delete related health data first to avoid foreign key constraint issues
    c.execute("DELETE FROM health_data WHERE user_id = ?", (user_id,))
    flash('User deleted successfully.', 'success')
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    
    conn.commit()
    conn.close()

    
    return redirect(url_for('admin'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()

    c.execute("SELECT * FROM health_data WHERE user_id = ?", (user_id,))
    health_data = c.fetchall()

    parsed_health_data = []
    for health in health_data:
        try:
            health_parameters = json.loads(health['health_parameters'])
        except json.JSONDecodeError:
            health_parameters = json.loads(health['health_parameters'].replace("'", '"'))

        parsed_health_data.append({
            'type': health['type'],
            'health_parameters': health_parameters,
            'result': health['result']
        })

    conn.close()

    return render_template('profile.html', user=user, health_data=parsed_health_data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_password_input = request.form['admin_password']
        if admin_password_input == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin')) 
        else:
            flash('Incorrect password. Please try again.', 'danger')

    if session.get('admin_logged_in'):
        conn = get_db_connection()
        c = conn.cursor()
        
        # Fetch all users
        c.execute("SELECT * FROM users")
        users = c.fetchall()

        # Fetch health data for each user
        c.execute("SELECT * FROM health_data")
        health_data_raw = c.fetchall()

        # Organize and parse health data by user ID
        health_data = {}
        for row in health_data_raw:
            user_id = row['user_id']
            if user_id not in health_data:
                health_data[user_id] = []

            try:
                health_parameters = json.loads(row['health_parameters'])
            except json.JSONDecodeError:
                health_parameters = json.loads(row['health_parameters'].replace("'", '"'))

            health_data[user_id].append({
                'type': row['type'],
                'health_parameters': health_parameters,
                'result': row['result']
            })

        conn.close()
        return render_template('admin.html', users=users, health_data=health_data)

    return render_template('admin.html')


@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_password_input = request.form['admin_password']
    if admin_password_input == admin_password:
        session['admin_logged_in'] = True
        return redirect(url_for('admin')) 
    else:
        flash('Incorrect password. Please try again.', 'danger')
        return redirect(url_for('admin'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out successfully.', 'info')
    return redirect(url_for('admin'))
@app.route("/api/find_doctors")
def api_find_doctors():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    doctor_type = request.args.get("type")

    # Decide query
    if doctor_type == "cardiologist":
        query = "cardiologist"
    else:
        query = "diabetologist"

    params = {
        "engine": "google_maps",
        "q": query,
        "ll": f"@{lat},{lon},14z",
        "type": "search",

        
        "hl": "en",
        "gl": "in",
        "google_domain": "google.co.in",

        "api_key": "7dabb6cb8f08972184d971da3eef7754f7c2e6d95e0c34b70969848e25790baa"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    filtered_results = []

    for place in results.get("local_results", []):
        gps = place.get("gps_coordinates")
        if gps:
            dist = distance_km(
                lat,
                lon,
                gps["latitude"],
                gps["longitude"]
            )

            # ✅ 10 KM RANGE (change to 5 if needed)
            if dist <= 10:
                place["distance_km"] = round(dist, 2)
                filtered_results.append(place)

    return jsonify(filtered_results)


if __name__ == '__main__':
    app.run(debug=True)