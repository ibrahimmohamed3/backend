from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Patient(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default='patient')  
    date_of_birth = Column(Date)
    phone_numbers = Column(String)
    address = Column(String)
    medical_history = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_relationship = Column(String)
    emergency_contact_phone = Column(String)
    insurance_provider = Column(String)
    policy_number = Column(String)
    appointment_history = Column(String)
    notes_comments = Column(String)
    health_goals = Column(String)
    preferences = Column(String)
    allergies = Column(String)
    current_medications = Column(String)


class Doctor(db.Model):
    __tablename__ = 'doctor' 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default='doctor')


class Review(db.Model):
    __tablename__ = 'review'  
    id = Column(Integer, primary_key=True)
    rating = Column(Float)
    comment = Column(String)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship('Patient', backref='reviews')


class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    medicines = db.relationship('Medicine', backref='hospital', lazy=True)

    def __repr__(self):
        return f'<Hospital {self.name}>'


class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    usage = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)

    def __repr__(self):
        return f'<Medicine {self.name}>'


class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)

    def __repr__(self):
        return f'<Diagnosis {self.diagnosis}>'
