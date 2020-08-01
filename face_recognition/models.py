from datetime import datetime
from face_recognition import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import column_property, relationship, backref
from flask import flash
from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@login_manager.user_loader
def load_user(username):
    return Admin_details.query.get(str(username))

class Admin_details(db.Model, UserMixin):
	__tablename__ = 'admin_details'
	id = db.Column(db.Integer,primary_key=True)
	admin_name = db.Column(db.String(20), unique=True)
	password=db.Column(db.String(60))

	def __repr__(self):
		return f"Admin_details('{self.admin_name}', '{self.password}')"

class Student_details(UserMixin,db.Model):
	__tablename__ = 'student_details'
	enrol =  db.Column(db.String(20),primary_key=True)
	name =  db.Column(db.String(20), nullable=False)
	contact = db.Column(db.String(120), unique=True, nullable=False)
	parent_contact = db.Column(db.String(120), nullable=False)
	room_num = db.Column(db.String(20), nullable=False)        

class Leaving_details(db.Model, UserMixin):
	__tablename__ = 'leaving_details'
	enrol_num = db.Column(db.String(20), primary_key=True)
	destination =  db.Column(db.String(20), nullable=False)
	dep_date_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

class History(db.Model, UserMixin):
	__tablename__ = 'history'
	id = db.Column(db.Integer,primary_key=True)
	enrol =  db.Column(db.String(20))
	destination =  db.Column(db.String(20), nullable=False)
	dep_date_time = db.Column(db.String(50), nullable=True)
	arr_date_time = db.Column(db.String(50), nullable=True)

class Campus_exit(db.Model, UserMixin):
	__tablename__ = 'campus_exit'
	enrol_num = db.Column(db.String(20), primary_key=True)



