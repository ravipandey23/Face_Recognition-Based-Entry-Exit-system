import os
import secrets
from flask import render_template, url_for, flash, redirect, request, session
from face_recognition import app, db, bcrypt
from face_recognition.forms import student_registration, LoginForm, Hostel_entry, New_Room, New_Contact, Parent_new_contact,Single_student,Batch, Input_enrol,Input_date
from face_recognition.models import Student_details, Leaving_details, History,Campus_exit, Admin_details
from flask_login import login_user, current_user, logout_user, login_required
from face_recognition import orm
import datetime
import shutil


@app.route("/")
@app.route("/main")
def main_page():
    if current_user.is_authenticated:
        return render_template('admin_options.html')
    else:
        return render_template('main.html')
    

@app.route("/registration", methods=['GET', 'POST'])
@login_required
def registration():
    form = student_registration()
    if form.validate_on_submit():
        roll_no=(form.enrol_number.data).upper()
        if orm.check_unique(roll_no,form.contact.data)==1:
            flash(f'Enrolment number already registered', "danger")
            return redirect(url_for('registration'))
        if orm.check_unique(roll_no,form.contact.data)==2:
            flash(f'Contact number already taken', "danger")
            return redirect(url_for('registration'))
        if orm.check_unique(roll_no,form.contact.data)==3:
            flash(f'Enrolment number and Contact number already taken', "danger")
            return redirect(url_for('registration'))
        if(orm.register_face(roll_no)):            
            student = Student_details(enrol=roll_no, name=form.name.data, contact=form.contact.data, parent_contact=form.parent_contact.data, room_num=form.room_number.data)
            db.session.add(student)
            db.session.commit()
            student = orm.show_details(roll_no)
            flash(f'{form.enrol_number.data}, Registered successfully', "success")
            return render_template('show_details.html', name=student[1],enrol=student[0],room_number=student[4],contact=student[2],parent_contact=student[3])
        else:
            flash(f'Face Could not be Captured', "danger")
            return redirect(url_for('registration'))
    return render_template('register.html', form=form)





    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_options'))    
    form = LoginForm()
    if form.validate_on_submit():
        user=Admin_details.query.filter_by(admin_name=form.username.data).first()                                        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page=request.args.get("next")
            flash(f'ADMIN logged in Successfully!', "success")
            return redirect(url_for('admin_options'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')           
    return render_template('login.html', form=form)

@app.route("/admin_options")
@login_required
def admin_options():
    return render_template('admin_options.html')


@app.route("/hostel_entry", methods=['GET', 'POST'])
def hostel_entry():
    form=Hostel_entry()
    if form.validate_on_submit():
        destination=form.destination.data
        # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/temp.py')
        # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm1.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm.py')
        # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/temp.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm1.py')
        
        roll_no=(orm.recognize_face())
        if roll_no==False:
            flash(f'Face not recognized', "danger")
            return redirect(url_for('hostel_entry'))
        roll_no=roll_no.upper()
        if(orm.check(roll_no)):
            flash(f'{roll_no} already outside', "danger")
            return redirect(url_for('hostel_entry'))
        if roll_no=="UNKNOWN":
            flash(f'Face not recognized', "danger")
            return redirect(url_for('hostel_entry'))
        # print(roll_no)     
        student=Leaving_details(enrol_num=str(roll_no), destination=destination , dep_date_time = datetime.datetime.now())
        db.session.add(student)
        db.session.commit()
        flash(f'{roll_no}, hostel_entry successfull', "success")
        return redirect(url_for('main_page'))
    # else:
    #     flash(f'Face Could not be Captured', "danger")
    #     return redirect(url_for('hostel_entry')) 
    else:
        return render_template('hostel_entry.html', form=form)


@app.route("/update_query")
@login_required
def update_query():
    return render_template('update_query.html')

@app.route("/update_room", methods=['GET', 'POST'])
@login_required
def update_room():
    form=New_Room()
    if form.validate_on_submit():
        enrol=(form.enrol.data).upper()
        new_room=form.new_room.data
        if orm.update_room(enrol, new_room):
            student = orm.show_details(enrol)
            flash(f'Room Number updated Successfully for {enrol}!', "success")
            return render_template('show_details.html', name=student[1],enrol=student[0],room_number=student[4],contact=student[2],parent_contact=student[3])
            # return redirect(url_for('admin_options'))
        else:
            flash(f'Enrolment not found', "danger")
    return render_template('update_room.html', form=form)

@app.route("/update_contact", methods=['GET', 'POST'])
@login_required
def update_contact():
    form=New_Contact()
    if form.validate_on_submit():
        enrol=(form.enrol.data).upper()
        new_contact=form.new_contact.data
        if orm.update_contact(enrol, new_contact):
            student = orm.show_details(enrol)
            flash(f'Contact Number updated Successfully for {enrol}!', "success")
            return render_template('show_details.html', name=student[1],enrol=student[0],room_number=student[4],contact=student[2],parent_contact=student[3])
        else:
            flash(f'Enrolment not found', "danger")
    return render_template('update_contact.html', form=form)


@app.route("/update_parent_contact", methods=['GET', 'POST'])
@login_required
def update_parent_contact():
    form=Parent_new_contact()
    if form.validate_on_submit():
        enrol=(form.enrol.data).upper()
        parent_new_contact=form.parent_new_contact.data
        if orm.update_parent_contact(enrol, parent_new_contact):
            student = orm.show_details(enrol)
            flash(f"Parents's Contact Number updated Successfully for {enrol}!", "success")
            return render_template('show_details.html', name=student[1],enrol=student[0],room_number=student[4],contact=student[2],parent_contact=student[3])
        else:
            flash(f'Enrolment not found', "danger")
    return render_template('update_parent_contact.html', form=form)


@app.route("/single_student", methods=['GET', 'POST'])
@login_required
def single_student():
    form=Single_student()
    if form.validate_on_submit():
        enrol=(form.enrol.data).upper()
        if orm.delete_single(enrol):
            flash(f"Student details for {enrol} deleted Sccessfully!", "success")
            return redirect(url_for('admin_options'))
    return render_template('single_student.html', form=form)


@app.route("/batch_year", methods=['GET', 'POST'])
@login_required
def batch_year():
    form=Batch()
    if form.validate_on_submit():
        batch=form.batch.data
        if orm.delete_batch(batch):
            flash(f"{batch} Batch deleted Sccessfully!", "success")
            return redirect(url_for('admin_options'))
    return render_template('batch_year.html', form=form)


@app.route("/delete_query")
@login_required
def delete_query():
    return render_template('delete_query.html')

@app.route("/student_details", methods=['GET', 'POST'])
@login_required
def student_details():
    form=Input_enrol()
    if form.validate_on_submit():
        enrol=(form.enrol.data).upper()
        if orm.show_details(enrol):
            student = orm.show_details(enrol)
            return render_template('show_details.html', name=student[1],enrol=student[0],room_number=student[4],contact=student[2],parent_contact=student[3])
        else:
            flash(f"{enrol} Not Found !", "danger")
    return render_template('student_details.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route("/history")
@login_required
def history():
    return render_template('history.html')


@app.route("/search_by_enrol", methods=['GET', 'POST'])
@login_required
def search_by_enrol():
    form=Input_enrol()
    if form.validate_on_submit():
        enrol=(form.enrol.data).upper()
        if orm.search_by_enrol(enrol):
            search_details=orm.search_by_enrol(enrol)
            return render_template('show_searched_details.html', search_details=search_details)
        else:
            flash(f"Details of {enrol} Not Found !", "danger")
    return render_template('search_by_enrol.html', form=form)

@app.route("/search_by_date", methods=['GET', 'POST'])
@login_required
def search_by_date():
    form=Input_date()

    if form.validate_on_submit():
        date=form.date.data
        if orm.search_by_date(date):
            search_details=orm.search_by_date(date)
            return render_template('show_searched_details.html', search_details=search_details)
        else:
            flash(f"No Entry Found for {date} !", "danger")
    return render_template('search_by_date.html', form=form)

@app.route("/students_outside", methods=['GET', 'POST'])
@login_required
def students_outside():
    
    if(orm.search_outside()):
        search_details=orm.search_outside()
        return render_template('show_searched_details.html', search_details=search_details)
    else:
        flash(f"No student outside !", "success")
        return redirect(url_for('history'))


@app.route("/campus_exit")
def campus_exit():
    # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/temp.py')
    # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm1.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm.py')
    # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/temp.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm1.py')
    enroll=(orm.recognize_face())
    if enroll==False:
        flash(f'Face not recognized', "danger")
        return redirect(url_for('main_page'))
    enroll=enroll.upper()
    if(orm.check(enroll)):
        # destination, time , date = get_temp_details()
        if not(orm.already(enroll)):
            flash(f'{enroll} already outside', 'danger')
            return redirect(url_for('main_page'))
        entry = Campus_exit(enrol_num=enroll);
        db.session.add(entry)
        db.session.commit()
        flash(f'Access Granted for {enroll}', 'success')
        return redirect(url_for('main_page'))
    else:
        flash(f'Access Denied', 'danger')
        return redirect(url_for('main_page'))

@app.route("/main_entry")
def main_entry():
    # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/temp.py')
    # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm1.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm.py')
    # shutil.copyfile('/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/temp.py','/home/ravi/Desktop/Mini/face_recognition-master/face_recognition/orm1.py')
    enroll=(orm.recognize_face())
    if enroll==False:
        flash(f'Face not recognized', "danger")
        return redirect(url_for('main_page'))
    enroll=enroll.upper()
    if(orm.check(enroll)):
        if(orm.main_exit(enroll)==False):
            flash(f'{enroll} is already inside the campus', 'danger')
            return redirect(url_for('main_page'))
        orm.make_history(enroll)
        flash(f'Access Granted for {enroll}', 'success')
        return redirect(url_for('main_page'))
    else:
        flash(f'Face not recognised', 'danger')
    return render_template('main.html')
     


    # enroll=(orm.recognize_face())
    # if enroll==False:
    #     flash(f'Face not recognized', "danger")
    #     return redirect(url_for('main_page'))
    # enroll=enroll.upper()
    # if(orm.check(enroll)):
    #     if(orm.main_exit(enroll)==False):
    #         flash(f'{enroll} is already inside the campus', 'danger')
    #         return redirect(url_for('main_page'))
    #     orm.make_history(enroll)
    #     flash(f'Access Granted for {enroll}', 'success')
    #     return redirect(url_for('main_page'))
    # else:
    #     flash(f'Face not recognised', 'danger')
    # return render_template('main.html'