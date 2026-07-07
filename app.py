from flask import Flask, render_template, request, redirect, session
from database import conn, cursor

app = Flask(__name__)
app.secret_key = "secret"

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        if u == "admin" and p == "admin":
            session['user'] = u
            return redirect('/')

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- DASHBOARD ----------------
@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT COUNT(*) FROM patients")
    p = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM doctors")
    d = cursor.fetchone()[0]

    return render_template('dashboard.html', p=p, d=d)

# ---------------- PATIENTS ----------------
@app.route('/patients')
def patients():
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    return render_template('patients.html', patients=data)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    cursor.execute(
        "INSERT INTO patients (name, age, gender, disease) VALUES (%s,%s,%s,%s)",
        (request.form['name'], request.form['age'], request.form['gender'], request.form['disease'])
    )
    conn.commit()
    return redirect('/patients')

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    conn.commit()
    return redirect('/patients')

# ---------------- DOCTORS ----------------
@app.route('/doctors')
def doctors():
    cursor.execute("SELECT * FROM doctors")
    data = cursor.fetchall()
    return render_template('doctors.html', doctors=data)

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    cursor.execute(
        "INSERT INTO doctors (name, age, gender, specialization) VALUES (%s,%s,%s,%s)",
        (request.form['name'], request.form['age'], request.form['gender'], request.form['specialization'])
    )
    conn.commit()
    return redirect('/doctors')

@app.route('/assign')
def assign():
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()

    return render_template('assign.html', patients=patients, doctors=doctors)

@app.route('/assign_doctor', methods=['POST'])
def assign_doctor():
    pid = request.form['patient_id']
    did = request.form['doctor_id']

    cursor.execute("UPDATE patients SET doctor_id=%s WHERE id=%s", (did, pid))
    conn.commit()
    return redirect('/')

# ---------------- BILL ----------------
@app.route('/bill/<int:id>')
def bill(id):
    cursor.execute("SELECT * FROM patients WHERE id=%s", (id,))
    p = cursor.fetchone()
    return render_template('bill.html', p=p)

if __name__ == '__main__':
    app.run(debug=True)