from main.app import db

def add_to_db(data):
	db.session.add(data)
	db.session.commit()

def delete_from_db(data):
	db.session.add(data)
	db.session.commit()