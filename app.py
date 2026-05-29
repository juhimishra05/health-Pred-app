from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import joblib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load trained ML model
model = joblib.load("model.pkl")


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100))
    glucose = db.Column(db.Float)
    haemoglobin = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    remarks = db.Column(db.String(500))


def predict_health(glucose, haemoglobin, cholesterol):

    prediction = model.predict([
        [glucose, haemoglobin, cholesterol]
    ])

    return prediction[0]


@app.route('/')
def index():

    patients = Patient.query.all()

    return render_template(
        'index.html',
        patients=patients
    )


@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

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


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':

        patient.full_name = request.form['full_name']
        patient.dob = request.form['dob']
        patient.email = request.form['email']

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