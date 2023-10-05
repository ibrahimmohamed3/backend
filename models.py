from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Patient(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_numbers = Column(Integer)
    


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
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)  # Correct ForeignKey reference
    diagnosis = Column(String)  # Updated data type to String for simplicity
    medicine_id = Column(Integer, ForeignKey('medicines.id'), nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)

    # Define a relationship with the Patient model
    patient = relationship('Patient', backref='diagnoses')

    def __repr__(self):
        return f'<Diagnosis {self.diagnosis}>'