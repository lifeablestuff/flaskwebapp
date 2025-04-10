from flask import Blueprint, request, jsonify
from flaskr.dbmodel import db, User, ConferenceSlot, Booking

bp = Blueprint('booking', __name__, url_prefix='/booking')

@bp.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    parent_id = data.get('parent_id')
    slot_id = data.get('slot_id')
    slot = ConferenceSlot.query.get(slot_id)

    if slot is None or not slot.available:
        return jsonify({'message': 'Slot not available'}), 400

    try:
        booking = Booking(parent_id=parent_id, slot_id=slot_id)
        db.session.add(booking)
        slot.available = False
        db.session.commit()
        return jsonify({'message': 'Booking created'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/cancel', methods=['POST'])
def cancel():
    data = request.get_json()
    if data.get('role') != 'parent':
        return jsonify({'message': 'Only for parents'}), 401
        
    parent_id = data.get('parent_id')
    slot_id = data.get('slot_id')
    
    slot = ConferenceSlot.query.get(slot_id)
    booking = Booking.query.filter_by(parent_id=parent_id, slot_id=slot_id).first()

    if slot is None or booking is None:
        return jsonify({'message': 'Booking not found'}), 404

    try:
        slot.available = True
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking canceled'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/reschedule', methods=['POST'])
def reschedule():
    data = request.get_json()
    if data.get('role') != 'parent':
        return jsonify({'message': 'Only for parents'}), 401

    parent_id = data.get('parent_id')
    slot_id = data.get('slot_id')
    new_slot_id = data.get('new_slot_id')

    booking = Booking.query.filter_by(parent_id=parent_id, slot_id=slot_id).first()
    new_slot = ConferenceSlot.query.get(new_slot_id)

    if booking is None:
        return jsonify({'message': 'Booking not found'}), 404
    if new_slot is None or not new_slot.available:
        return jsonify({'message': 'New slot not available'}), 400

    try:
        booking.slot_id = new_slot_id
        new_slot.available = False  # Mark new slot as booked
        old_slot = ConferenceSlot.query.get(slot_id)
        if old_slot:
            old_slot.available = True  # Free old slot
        db.session.commit()
        return jsonify({'message': 'Booking rescheduled'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/view', methods=['POST','GET'])
def view():
    data = request.get_json()
    parent_id = data.get('parent_id')
    slot_id = data.get('slot_id')

    booking = Booking.query.filter_by(parent_id=parent_id, slot_id=slot_id).first()
    
    if booking is None:
        return jsonify({'message': 'Booking not found'}), 404

    return jsonify({'booking': booking.serialize()})
