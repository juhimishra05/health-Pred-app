from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import joblib
import re
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load ML Model
try:
    model = joblib.load("model.pkl")
except Exception:
    model = None


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    haemoglobin = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.String(500))


# Email Validation
def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)


# DOB Validation
def is_valid_dob(dob):
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")

        if dob_date > datetime.now():
            return False

        return True

    except:
        return False


# ML Prediction
def predict_health(glucose, haemoglobin, cholesterol):

    if model is None:
        return "Prediction Unavailable"

    try:
        prediction = model.predict(
            [[glucose, haemoglobin, cholesterol]]
        )

        return prediction[0]

    except:
        return "Prediction Unavailable"


# READ
@app.route('/')
def index():

    patients = Patient.query.all()

    return render_template(
        'index.html',
        patients=patients
    )


# CREATE
@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

        # Validation
        if not is_valid_email(email):
            return render_template(
                'add_patient.html',
                error="Invalid Email Format"
            )

        if not is_valid_dob(dob):
            return render_template(
                'add_patient.html',
                error="Invalid Date of Birth"
            )

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        patient = Patient(
            full_name=full_name,
            dob=dob,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/')

    return render_template('add_patient.html')


# UPDATE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':

        patient.full_name = request.form['full_name']
        patient.dob = request.form['dob']
        patient.email = request.form['email']

        # Validation
        if not is_valid_email(patient.email):
            return render_template(
                'edit_patient.html',
                patient=patient,
                error="Invalid Email Format"
            )

        if not is_valid_dob(patient.dob):
            return render_template(
                'edit_patient.html',
                patient=patient,
                error="Invalid Date of Birth"
            )

        patient.glucose = float(request.form['glucose'])
        patient.haemoglobin = float(request.form['haemoglobin'])
        patient.cholesterol = float(request.form['cholesterol'])

        patient.remarks = predict_health(
            patient.glucose,
            patient.haemoglobin,
            patient.cholesterol
        )

        db.session.commit()

        return redirect('/')

    return render_template(
        'edit_patient.html',
        patient=patient
    )


# DELETE
@app.route('/delete/<int:id>')
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)