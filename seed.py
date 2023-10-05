from flask import Flask
from models import Patient, Doctor, Review, Hospital, Medicine, Diagnosis, db
from faker import Faker
import random

app = Flask(__name__)

# Initialize your Flask app and database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
fake = Faker()

def seed_data():
    with app.app_context():
        # Generate sample patients
        print("Seeding patients...")
        for _ in range(5):
            patient = Patient(
                name=fake.name(),
                
                email=fake.email(),
                
                
                phone_numbers=fake.phone_number(),
                
                
            )
            db.session.add(patient)
            db.session.commit()

        # Generate sample doctors
        print("Seeding doctors...")
        for _ in range(3):
            doctor = Doctor(
                name=fake.name(),
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
            db.session.add(doctor)
            db.session.commit()

        # Generate sample reviews
        print("Seeding reviews...")
        for patient in Patient.query.all():
            for _ in range(2):
                review = Review(
                    rating=random.uniform(1, 5),
                    comment=fake.text(),
                    patient_id=patient.id
                )
                db.session.add(review)
                db.session.commit()

        # Sample towns in Nairobi, Kisumu, and Mombasa
        towns_nairobi = ['Karen', 'Westlands', 'Kileleshwa', 'Runda', 'CBD']
        towns_kisumu = ['Kisumu Central', 'Nyalenda', 'Mamboleo', 'Nyamasaria', 'Kisian']
        towns_mombasa = ['Nyali', 'Mombasa Island', 'Bamburi', 'Likoni', 'Kiembeni']

        # Generate sample hospitals with related details
        print("Seeding hospitals...")
        for i in range(5):
            # Randomly select a town from Nairobi, Kisumu, or Mombasa
            if i < 2:
                location = random.choice(towns_nairobi)
            elif i < 4:
                location = random.choice(towns_kisumu)
            else:
                location = random.choice(towns_mombasa)
            # Generate the hospital object
            hospital = Hospital(
                name=fake.company(),
                location=location,
                contact=fake.phone_number()
            )
            db.session.add(hospital)
            db.session.commit()

            # Generate sample medicines associated with the hospital
            for _ in range(3):
                medicine = Medicine(
                    name=fake.word(),
                    description=fake.text(),
                    usage=fake.sentence(),
                    dosage=fake.sentence(),
                    hospital_id=hospital.id
                )
                db.session.add(medicine)
                db.session.commit()

               
        print("Data seeding completed.")

if __name__ == '__main__':
    with app.app_context():
        try:
            seed_data()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Rollback the session in case of an error
            db.session.rollback()
