from flask import Blueprint, jsonify, request, current_app as app
from models import db, Patient, Doctor, Review
from datetime import datetime
from flask import redirect, url_for


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


main = Blueprint('main', __name__)

from flask import jsonify, url_for

@main.route('/', methods=['GET'])
def list_endpoints():
    """List all available endpoints."""
    endpoints = {
        'GET /': url_for('main.list_endpoints', _external=True),
        'GET /patients/<int:patient_id>': url_for('main.get_patient', patient_id=1, _external=True),
        'POST /create_patient': url_for('main.create_patient', _external=True),
        'PUT /patients/<int:patient_id>': url_for('main.update_patient', patient_id=1, _external=True)
    }

    return jsonify({'endpoints': endpoints})




######################################## REVIEWS ################################


@main.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_list = []

    for review in reviews:

        patient_name = review.patient.name if review.patient else "Unknown Patient"

        review_info = {
            'rating': review.rating,
            'comment': review.comment,
            'patient_name': patient_name
        }
        review_list.append(review_info)

    return jsonify({'reviews': review_list})


@main.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get(review_id)

    if review:
        patient_name = review.patient.name if review.patient else "Unknown Patient"

        review_info = {
            'rating': review.rating,
            'comment': review.comment,
            'patient_name': patient_name
        }
        return jsonify({'review': review_info}), 200
    else:
        return 'Review not found', 404




@main.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    patient_id = data.get('patient_id') 

    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found with the provided ID"}), 404

    new_review = Review(rating=rating, comment=comment)

    new_review.patient = patient

    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add review", "error": str(e)}), 500

################################ DOCTORS #################################

@main.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    doctor_list = []
    for doctor in doctors:
        doctor_info = {
            'id': doctor.id,
            'name': doctor.name,
            'username': doctor.username,
            'email': doctor.email
        }
        doctor_list.append(doctor_info)
    return jsonify({'doctors': doctor_list})


@main.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)

    if doctor:
        doctor_info = {
            'id': doctor.id,
            'name': doctor.name,
            'username': doctor.username,
            'email': doctor.email
        }
        return jsonify({'doctor': doctor_info}), 200
    else:
        return 'Doctor not found', 404


@main.route('/add_doctor', methods=['POST'])
def add_doctor():
    data = request.get_json()
    new_doctor = Doctor(name=data['name'], username=data['username'], email=data['email'], password=data['password'])
    new_doctor.role = 'doctor'  
    db.session.add(new_doctor)
    db.session.commit()
    return "Doctor added successfully", 201


@main.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return f'Doctor with ID {doctor_id} deleted successfully', 200
    else:
        return 'Doctor not found', 404

@main.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    data = request.get_json()
    doctor = Doctor.query.get(doctor_id)

    if doctor:
        doctor.name = data.get('name', doctor.name)
        doctor.username = data.get('username', doctor.username)
        doctor.email = data.get('email', doctor.email)
        doctor.password = data.get('password', doctor.password)
        
        db.session.commit()
        return f'Doctor with ID {doctor_id} updated successfully', 200
    else:
        return 'Doctor not found', 404


################################PATIENTS #################################

@main.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    patient_list = []
    
    for patient in patients:
        patient_info = {
            'id': patient.id,
            'name': patient.name,
            'username': patient.username,
            'email': patient.email,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),  # format datess as YYYY-MM-DD
            'phone_numbers': patient.phone_numbers,
            'address': patient.address,
            'medical_history': patient.medical_history,
            'emergency_contact_name': patient.emergency_contact_name,
            'emergency_contact_relationship': patient.emergency_contact_relationship,
            'emergency_contact_phone': patient.emergency_contact_phone,
            'insurance_provider': patient.insurance_provider,
            'policy_number': patient.policy_number,
            'appointment_history': patient.appointment_history,
            'notes_comments': patient.notes_comments,
            'health_goals': patient.health_goals,
            'preferences': patient.preferences,
            'allergies': patient.allergies,
            'current_medications': patient.current_medications
        }
        patient_list.append(patient_info)

    return jsonify({'patients': patient_list})


@main.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)

    if patient:
        patient_info = {
            'id': patient.id,
            'name': patient.name,
            'username': patient.username,
            'email': patient.email,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),  # format  YYYY-MM-DD
            'phone_numbers': patient.phone_numbers,
            'address': patient.address,
            'medical_history': patient.medical_history,
            'emergency_contact_name': patient.emergency_contact_name,
            'emergency_contact_relationship': patient.emergency_contact_relationship,
            'emergency_contact_phone': patient.emergency_contact_phone,
            'insurance_provider': patient.insurance_provider,
            'policy_number': patient.policy_number,
            'appointment_history': patient.appointment_history,
            'notes_comments': patient.notes_comments,
            'health_goals': patient.health_goals,
            'preferences': patient.preferences,
            'allergies': patient.allergies,
            'current_medications': patient.current_medications
        }
        return jsonify({'patient': patient_info}), 200
    else:
        return 'Patient not found', 404



@main.route('/create_patient', methods=['POST'])
def create_patient():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone_numbers = data.get('phone_numbers')
    
    new_patient = Patient(
        name=name,
        email=email,
        phone_numbers=phone_numbers,
        
        
    )

    db.session.add(new_patient)
    db.session.commit()

    return f"New patient added successfully with ID: {new_patient.id}", 201


@main.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.get(patient_id)

    if patient:
        patient.name = data.get('name', patient.name)
        patient.username = data.get('username', patient.username)
        patient.email = data.get('email', patient.email)
        patient.date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()

        db.session.commit()
        return f'Patient with ID {patient_id} updated successfully', 200
    else:
        return 'Patient not found', 404


# raegan
from flask import Blueprint, jsonify, request
from models import Hospital, Medicine, Diagnosis, db

hospital_routes = Blueprint('hospital_routes', __name__)


# ---- Hospitals ----

@hospital_routes.route('/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = Hospital.query.all()
    hospital_list = [{'id': hospital.id, 'name': hospital.name, 'location': hospital.location, 'contact': hospital.contact} for hospital in hospitals]
    return jsonify({'hospitals': hospital_list})

@hospital_routes.route('/hospitals/location/<string:location>', methods=['GET'])
def get_hospitals_by_location(location):
    # Query hospitals with the specified location
    hospitals = Hospital.query.filter_by(location=location).all()

    # Check if any hospitals were found
    if hospitals:
        # Create a list of dictionaries with hospital information
        hospital_list = []
        for hospital in hospitals:
            hospital_info = {
                'id': hospital.id,
                'name': hospital.name,
                'location': hospital.location,
                'contact': hospital.contact
            }
            hospital_list.append(hospital_info)
        return jsonify({'hospitals': hospital_list})
    else:
        # Return a 404 error if no hospitals are found with the specified location
        return jsonify({'error': 'No hospitals found for the location'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        hospital_data = {'id': hospital.id, 'name': hospital.name, 'address': hospital.address, 'contact': hospital.contact}
        return jsonify({'hospital': hospital_data})
    return jsonify({'message': 'Hospital not found'}), 404

@hospital_routes.route('/hospitals', methods=['POST'])
def add_hospital():
    data = request.form
    name = data.get('name')
    address = data.get('address')
    contact = data.get('contact')

    if not name or not address or not contact:
        return jsonify({'error': 'Incomplete data. Please provide name, address, and contact for the hospital.'}), 400

    new_hospital = Hospital(name=name, address=address, contact=contact)

    try:
        db.session.add(new_hospital)
        db.session.commit()
        return jsonify({'message': 'Hospital added successfully', 'hospital': {'id': new_hospital.id, 'name': new_hospital.name, 'address': new_hospital.address, 'contact': new_hospital.contact}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while adding the hospital: {str(e)}'}), 500

@hospital_routes.route('/hospitals/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    data = request.form
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        hospital.name = data.get('name', hospital.name)
        hospital.address = data.get('address', hospital.address)
        hospital.contact = data.get('contact', hospital.contact)
        db.session.commit()
        return jsonify({'message': 'Hospital updated successfully'})
    return jsonify({'message': 'Hospital not found'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>', methods=['DELETE'])
def delete_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
        return jsonify({'message': 'Hospital deleted successfully'})
    return jsonify({'message': 'Hospital not found'}), 404

# ---- Medicines ----

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines', methods=['GET'])
def get_medicines(hospital_id):
    medicines = Medicine.query.filter_by(hospital_id=hospital_id).all()
    medicine_list = [{'id': medicine.id, 'name': medicine.name, 'description': medicine.description, 'usage': medicine.usage, 'dosage': medicine.dosage} for medicine in medicines]
    return jsonify({'medicines': medicine_list})

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines', methods=['POST'])
def add_medicine(hospital_id):
    data = request.form
    name = data.get('name')
    description = data.get('description')
    usage = data.get('usage')
    dosage = data.get('dosage')

    if not name or not description or not usage or not dosage:
        return jsonify({'error': 'Incomplete data. Please provide name, description, usage, and dosage for the medicine.'}), 400

    new_medicine = Medicine(name=name, description=description, usage=usage, dosage=dosage, hospital_id=hospital_id)

    try:
        db.session.add(new_medicine)
        db.session.commit()
        return jsonify({'message': 'Medicine added successfully', 'medicine': {'id': new_medicine.id, 'name': new_medicine.name, 'description': new_medicine.description, 'usage': new_medicine.usage, 'dosage': new_medicine.dosage}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while adding the medicine: {str(e)}'}), 500

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines/<int:medicine_id>', methods=['PUT'])
def update_medicine(hospital_id, medicine_id):
    data = request.form
    medicine = Medicine.query.filter_by(id=medicine_id, hospital_id=hospital_id).first()
    if medicine:
        medicine.name = data.get('name', medicine.name)
        medicine.description = data.get('description', medicine.description)
        medicine.usage = data.get('usage', medicine.usage)
        medicine.dosage = data.get('dosage', medicine.dosage)
        db.session.commit()
        return jsonify({'message': 'Medicine updated successfully'})
    return jsonify({'message': 'Medicine not found'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>/medicines/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(hospital_id, medicine_id):
    medicine = Medicine.query.filter_by(id=medicine_id, hospital_id=hospital_id).first()
    if medicine:
        db.session.delete(medicine)
        db.session.commit()
        return jsonify({'message': 'Medicine deleted successfully'})
    return jsonify({'message': 'Medicine not found'}), 404

# ---- Diagnoses ----

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses', methods=['GET'])
def get_diagnoses(hospital_id):
    diagnoses = Diagnosis.query.filter_by(hospital_id=hospital_id).all()
    diagnosis_list = [{'id': diagnosis.id, 'patient_id': diagnosis.patient_id, 'diagnosis': diagnosis.diagnosis} for diagnosis in diagnoses]
    return jsonify({'diagnoses': diagnosis_list})

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses', methods=['POST'])
def add_diagnosis(hospital_id):
    data = request.form
    patient_id = data.get('patient_id')
    diagnosis_text = data.get('diagnosis')

    if not patient_id or not diagnosis_text:
        return jsonify({'error': 'Incomplete data. Please provide patient_id and diagnosis for the diagnosis.'}), 400

    new_diagnosis = Diagnosis(patient_id=patient_id, diagnosis=diagnosis_text, hospital_id=hospital_id)

    try:
        db.session.add(new_diagnosis)
        db.session.commit()
        return jsonify({'message': 'Diagnosis added successfully', 'diagnosis': {'id': new_diagnosis.id, 'patient_id': new_diagnosis.patient_id, 'diagnosis': new_diagnosis.diagnosis}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred while adding the diagnosis: {str(e)}'}), 500

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses/<int:diagnosis_id>', methods=['PUT'])
def update_diagnosis(hospital_id, diagnosis_id):
    data = request.form
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, hospital_id=hospital_id).first()
    if diagnosis:
        diagnosis.patient_id = data.get('patient_id', diagnosis.patient_id)
        diagnosis.diagnosis = data.get('diagnosis', diagnosis.diagnosis)
        db.session.commit()
        return jsonify({'message': 'Diagnosis updated successfully'})
    return jsonify({'message': 'Diagnosis not found'}), 404

@hospital_routes.route('/hospitals/<int:hospital_id>/diagnoses/<int:diagnosis_id>', methods=['DELETE'])
def delete_diagnosis(hospital_id, diagnosis_id):
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, hospital_id=hospital_id).first()
    if diagnosis:
        db.session.delete(diagnosis)
        db.session.commit()
        return jsonify({'message': 'Diagnosis deleted successfully'})
    return jsonify({'message': 'Diagnosis not found'}), 404        
