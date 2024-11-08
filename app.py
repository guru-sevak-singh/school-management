from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from flask_migrate import Migrate
from flask_login import login_user, current_user, UserMixin, login_required, logout_user, LoginManager
import os
from datetime import datetime
from sqlalchemy import extract
import json
import pandas as pd
import shutil


def write_students(file_name):
    # df = pd.read_excel('SD_SCHOOL_STUDENTS.xlsx', dtype=str, skiprows=2)
    df = pd.read_excel(file_name, dtype=str, skiprows=2)
    # print(df)
    all_students = df.set_index("s no.").T.to_dict('dict')
    print('all students created...')
    with app.app_context():

        session_year = db.get_or_404(SessionYear, 1)
        for student in all_students:
            try:
                class_name = all_students[student]['Class']
                clas = Standared.query.filter_by(class_name=class_name).first()
                if clas == None:
                    pass
                else:

                    section_name = all_students[student]['Section']
                    section = Section.query.filter_by(section_name=section_name).first()



                    running_class_unique_id = f"{session_year.id}-{clas.id}-{section.id}"
                    running_class = RunningClass.query.filter_by(running_class_unique_id=running_class_unique_id).first()
                    if running_class == None:
                        running_class = RunningClass(session_id=session_year.id, class_id=clas.id, section_id=section.id)
                        db.session.add(running_class)
                        db.session.commit()
                    
                  
                    social_category = all_students[student]['Social Category']
                    social_category = social_category.split("-")[1]

                    new_student = StudentDetail(name=all_students[student]['Name'], father_name=all_students[student]['Father Name'], mother_name=all_students[student]['Mother Name'], admision_number=student, phone_number="",
                                                gender=all_students[student]['Gender'])
                    db.session.add(new_student)
                    db.session.commit()

                    running_class.students.append(new_student)
                    db.session.commit()
            except Exception as e:
                class_name = all_students[student]['Class']
                print(class_name)
                print(e)


def write_staff(file_name):
    df = pd.read_excel(file_name, 'Staff Details', dtype=str)
    all_staff = df.values.tolist()
    # print(all_staff[2])
    for staff in all_staff:
        # print(staff)
        try:
            name = staff[0]
            merital_status = staff[1]
            husband_name = staff[2]
            father_name = staff[3]
            mother_name = staff[4]
            phone_number = staff[5]
            secondary_phone_number = staff[6]
            gender = staff[7]
            joining_date = staff[8]
            if str(joining_date) != 'nan':
                joining_date = str(joining_date).split(" ")[0]
                joining_date = datetime.strptime(joining_date, "%Y-%m-%d").date()
                
            else:
                joining_date = None
            birth_date = staff[9]

            if str(birth_date) == 'nan':
                birth_date = None
            else:
                birth_date = str(birth_date).split(" ")[0]
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()

            blood_group = staff[10]
            social_category = staff[11]
            aadhar_number = staff[12]
            pan_number = staff[13]
            subject = staff[14]
            designation = staff[15]
            address = staff[16]
            bank_name = staff[17]
            account_number = staff[18]
            ifsc_code = staff[19]
            basic_salary = staff[20]
            experience = staff[21]
            qualification = staff[25]
            
            if str(experience) != 'nan':
                experience = int(experience)
            
            staff_type = staff[24]
            if staff_type == 'Teaching':
                staff_type = True
            
                NewStaff = Staff(name=name, husband_name=husband_name, father_name=father_name, mother_name=mother_name, phone_number=phone_number, secondary_phone_number=secondary_phone_number,
                            gender=gender, blood_group=blood_group, social_category=social_category, aadhar_number=aadhar_number, pan_number=pan_number, subject=subject, designation=designation,
                            address=address, bank_name=bank_name, account_number=account_number, ifsc_code=ifsc_code, basic_salary=basic_salary, experience=experience,
                            staff_teaching_status=staff_type, qualification=qualification, merital_status=merital_status, joining_date=joining_date, birth_date=birth_date) 

            else:
                staff_type = False
            
                NewStaff = Staff(name=name, husband_name=husband_name, father_name=father_name, mother_name=mother_name, phone_number=phone_number, secondary_phone_number=secondary_phone_number,
                                gender=gender, blood_group=blood_group, social_category=social_category, aadhar_number=aadhar_number, pan_number=pan_number, designation=designation,
                                address=address, bank_name=bank_name, account_number=account_number, ifsc_code=ifsc_code, basic_salary=basic_salary, experience=experience,
                                staff_teaching_status=staff_type, qualification=qualification, merital_status=merital_status, joining_date=joining_date, birth_date=birth_date) 
            print(name)
            db.session.add(NewStaff)
            db.session.commit()
        except Exception as e:
            print(e)
    df = pd.read_excel(file_name, "subjects class", dtype=str)
    
    all_subject_list = df.values.tolist()
    for subject_detail in all_subject_list:
        class_detail = subject_detail[0]
        class_detail = class_detail.split(" ")
        class_name = class_detail[0]
        
        class_id = Standared.query.filter(Standared.class_name == class_name).first()
        last_session = SessionYear.query.count()
        sessoin = db.get_or_404(SessionYear, last_session)

        if class_id == None:
            new_class = Standared(class_name = class_name)
            db.session.add(new_class)
            db.session.commit()
            class_id = new_class
            sessoin.classes.append(new_class)

        section_name = class_detail[1]
        section_id = Section.query.filter(Section.section_name == section_name).first()
        if section_id == None:
            new_section = Section(section_name=section_name)
            db.session.add(new_section)
            db.session.commit()
            section_id = new_section
        running_class = RunningClass.query.filter(RunningClass.class_id == class_id.id, RunningClass.section_id==section_id.id).first()
        if running_class == None:
            
            running_class = RunningClass(session_id=sessoin.id, class_id=class_id.id, section_id=section_id.id)
            db.session.add(running_class)
            db.session.commit()
        
        if new_section in class_id.sections:
            pass
        else:
            class_id.sections.append(new_section)
            db.session.commit()
        
        subjects = subject_detail[1]
        subjects = subjects.split(",")
        for subject_name in subjects:
            subject = Subject.query.filter(Subject.subject_name == subject_name).first()
            if subject == None:
                subject = Subject(subject_name = subject_name)
                db.session.add(subject)
                db.session.commit()
            running_class.subjects.append(subject)
        
        db.session.commit()


    df = pd.read_excel(file_name,"subjects", dtype=str)
    all_subjects = df.values.tolist()
    for subject_detail in all_subjects:
        try:
            print(subject_detail)
            subject_name = subject_detail[0]
            subject = Subject.query.filter(Subject.subject_name==subject_name).first()
            if subject == None:
                subject = Subject(subject_name = subject_name)
                db.session.add(subject)
                db.session.commit()
            
            teachers = subject_detail[1]
            teachers = teachers.split(",")
            for teacher in teachers:
                subject_teacher = Staff.query.filter(Staff.name == teacher).first()
                if subject_teacher == None:
                    print('There is No Teacher With This Name...', teacher)
                else:
                    subject_teacher.subjects.append(subject)
            db.session.commit()
        except Exception as e:
            print(e)
        





Upload_Folder = 'uploads'

app = Flask(__name__)
db_location = f"sqlite:///{os.getcwd()}\\database.sqlite"

print(db_location)


app.config['SQLALCHEMY_DATABASE_URI'] = db_location
app.config['UPLOAD_FOLDER'] = Upload_Folder
app.config["SECRET_KEY"] = "MY SECRET KEY..."

db = SQLAlchemy(app=app)
migration = Migrate(app=app, db=db)

login_manager = LoginManager(app=app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, user_id)
    return user


def AdminUrl(name):
    return '/admin' + name

def DataApi(name):
    return '/data' + name

def admin_access():
    if current_user.user_type == 'admin':
        return True
    else:
        return False

########################################################################################################################################################
################################################################# MODALS ###############################################################################
########################################################################################################################################################

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)
    login_id = db.Column(db.Text, unique=True, index=True)
    password = db.Column(db.Text)
    user_type = db.Column(db.Text) # Admin, Teacher, Student, clerk (Teacher Attendent)
    user_status = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    login_status = db.Column(db.Boolean, default=False)
    
    comments = db.relationship("Comment", backref="user")
    notice_list = db.relationship("Notice", backref="user")
    teacher_id = db.Column(db.Integer, unique=True, index=True)
    exams = db.relationship("Exam", backref="user")

    def IsValidLogin(self):
        last_login = self.last_login
        time_gap = datetime.now() - last_login
        gap_in_hours = time_gap.total_seconds()/(3600 * 24)
        if gap_in_hours <= 1:
            return False
        else:
            return True
        
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    exam_date = db.Column(db.Date)
    exam_name = db.Column(db.Text)
    upload_time = db.Column(db.DateTime)
    subject = db.Column(db.Text)
    max_marks = db.Column(db.Text)
    marks_obtained = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("user.id"))
    student_id = db.Column(db.ForeignKey("student_detail.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("running_class.id"))

    def __init__(self, exam_date, exam_name, subject, max_marks, marks_obtained, user_id, student_id, class_id):
        self.exam_date = datetime.strptime(exam_date, "%Y-%m-%d")
        self.exam_name = exam_name
        self.upload_time = datetime.now()
        self.subject = subject
        self.max_marks = max_marks
        self.marks_obtained = marks_obtained
        self.user_id = user_id
        self.student_id = student_id
        self.class_id = class_id


class SessionYear(db.Model):
    __tablename__ = "session_year"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    session_name = db.Column(db.Text)
    session_year = db.Column(db.Integer, unique=True, index=True)


class StudentDetail(db.Model):
    __tablename__ = "student_detail"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    admision_number = db.Column(db.Integer, unique=True, index=True)
    name = db.Column(db.Text)
    father_name = db.Column(db.Text)
    mother_name = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    secondary_phone_number = db.Column(db.Text)
    gender = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    blood_group = db.Column(db.Text)
    social_category = db.Column(db.Text)
    admision_date = db.Column(db.Date)
    address = db.Column(db.Text)

    is_repeater = db.Column(db.Boolean) 
    bpl_beneficiary = db.Column(db.Boolean) #Taking BPL Benifits
    cwsn = db.Column(db.Boolean) # Children with Sepecial Needs
    imparement_type = db.Column(db.Text) #if cwsn is true then applicable other wise not
    student_pen = db.Column(db.Text) # Student Personal Education Number
    student_state_code = db.Column(db.Text) # student state code
    minority_group = db.Column(db.Text) #is the student comes in minority

    aadhar_number = db.Column(db.Text, unique=True, index=True)
    student_active_status = db.Column(db.Boolean, default=True) # is the student now exist in school or not

    comments = db.relationship("Comment", backref="student")
    attendence = db.relationship("StudentAttendence", backref="student")

    documents = db.relationship('Document', backref="student")
    exams = db.relationship("Exam", backref="student")

    def AdmisionDate(self):
        admision_date = self.admision_date
        if admision_date == None:
            return ""
        indian_date = admision_date.strftime("%d-%b-%Y")
        return indian_date
    
    def BirthDate(self):
        birth_date = self.birth_date
        if birth_date == None:
            return ""
        indian_date = birth_date.strftime("%d-%b-%Y")
        return indian_date
    
    def roll_no(self, running_class_unique_id):
        selected_class = RunningClass.query.filter_by(running_class_unique_id=running_class_unique_id).first()
        all_students = selected_class.students
        roll_number = all_students.index(self)
        roll_number = roll_number + 1
        return roll_number
        
    def last_class(self):
        clases = self.classes
        counts = len(clases)
        last_clas = clases[counts - 1]
        return last_clas.class_name()
    
    def get_last_class(self):
        clases = self.classes
        counts = len(clases)
        last_clas = clases[counts - 1]
        return last_clas
        

    def class_in_year(self, session_year):
        session = SessionYear.query.filter_by(session_year=session_year).first()
        clases = self.classes
        for clas in clases:
            if clas.session == session:
                return clas.class_name()
        
        return self.last_class()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.Text)
    file_name = db.Column(db.Text)
    uploaded_date = db.Column(db.Date)
    student_id = db.Column(db.ForeignKey('student_detail.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    comment_time = db.Column(db.DateTime)
    student_id = db.Column(db.ForeignKey('student_detail.id'))
    user_id = db.Column(db.ForeignKey('user.id'))

    def exect_time(self):
        exect_time = self.comment_time.strftime("%d-%b-%Y %I:%M%p")
        return exect_time


session_classes = db.Table("session_classes",
                           db.Column("session_id", db.ForeignKey("session_year.id")),
                           db.Column("standared_id", db.ForeignKey("standared.id")))

standared_section = db.Table("standared_sections",
                             db.Column("standared_id", db.ForeignKey("standared.id")),
                             db.Column("section_id", db.ForeignKey("section.id")))

class Standared(db.Model):
    __tablename__ = "standared"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    class_name = db.Column(db.Text, unique=True, index=True)
    sessions = db.relationship("SessionYear", secondary=session_classes, backref="classes")
    sections = db.relationship("Section", secondary=standared_section, backref="classes")

class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    section_name = db.Column(db.Text, unique=True, index=True)


running_class_sutdents = db.Table("running_class_student", 
                                  db.Column("running_class_id", db.ForeignKey("running_class.id")),
                                  db.Column("student_id", db.ForeignKey("student_detail.id")))

running_class_subjects = db.Table("running_class_subjects",
                                  db.Column("running_class_id", db.ForeignKey("running_class.id")),
                                  db.Column("subject_id", db.ForeignKey("subject.id")))

running_class_teachers = db.Table("running_classs_table",
                                  db.Column("running_class_id", db.ForeignKey("running_class.id")),
                                  db.Column("staff_id", db.ForeignKey("staff.id")))

subject_teachers = db.Table("subject_teacher",
                            db.Column("subject_id", db.ForeignKey("subject.id")),
                            db.Column("staff_id", db.ForeignKey("staff.id")))

class RunningClass(db.Model):
    __tablename__ = "running_class"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.ForeignKey("session_year.id"), name='session_id')
    class_id = db.Column(db.ForeignKey("standared.id"))
    section_id = db.Column(db.ForeignKey("section.id"))
    running_class_unique_id = db.Column(db.Text, unique=True, index=True)

    students = db.relationship("StudentDetail", secondary=running_class_sutdents, backref="classes")
    session = db.relationship("SessionYear", backref="main_classes")
    standared = db.relationship("Standared", backref="classes")
    section = db.relationship("Section", backref="main_classes")
    subjects = db.relationship("Subject", secondary=running_class_subjects, backref="classes")
    attendence = db.relationship("StudentAttendence", backref="running_class")
    teachers = db.relationship("Staff", secondary=running_class_teachers, backref="running_classes")

    time_table = db.relationship("TimeTable", backref="running_class")

    exams = db.relationship("Exam", backref="running_classes")

    def sections(self):
        sections = RunningClass.query.filter_by(session_id=self.session_id, class_id=self.class_id).all()
        return sections
    
    def class_name(self):
        if self.class_id == None and self.section_id != None:
            str_class_name = f"{self.section.section_name}"
        elif self.class_id != None and self.section == None:
            str_class_name = f"{self.standared.class_name}"
        elif self.class_id == None and self.section == None:
            str_class_name = 'UNDEFINED'
        else:
            str_class_name = f"{self.standared.class_name} - ({self.section.section_name})"

        return str_class_name    
    
    def __init__(self, session_id, class_id, section_id):
        self.session_id = session_id
        self.class_id = class_id
        self.section_id = section_id
        self.running_class_unique_id = f"{session_id}-{class_id}-{section_id}"

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    subject_name = db.Column(db.Text, unique=True, index=True)

    time_table = db.relationship('TimeTable', backref="subject")

    def class_teachers(self, running_class_id):
        subject_teachers = self.teachers
        
        running_class = db.get_or_404(RunningClass, running_class_id)
        class_teachers_query = running_class.teachers

        teachers = [teacher.name for teacher in subject_teachers if teacher in class_teachers_query]
        return teachers

class StudentAttendence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.ForeignKey('running_class.id'))
    student_id = db.Column(db.ForeignKey('student_detail.id'))
    present_status = db.Column(db.Text) # Present/Apsent/Leave
    attendence_date = db.Column(db.Date) # attendence date
    attendence_day = db.Column(db.Text) # attendence day
    taken_by = db.Column(db.Text) # teacher who take the attendence 

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)
    merital_status = db.Column(db.Text)
    husband_name = db.Column(db.Text)
    father_name = db.Column(db.Text)
    mother_name = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    secondary_phone_number = db.Column(db.Text)
    gender = db.Column(db.Text)
    joining_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    blood_group = db.Column(db.Text)
    social_category = db.Column(db.Text)


    aadhar_number = db.Column(db.Text, unique=True, index=True)
    pan_number = db.Column(db.Text, unique=True, index=True)
    subject = db.Column(db.Text)
    designation = db.Column(db.Text)
    pin = db.Column(db.Integer)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    address = db.Column(db.Text)
    bank_name = db.Column(db.Text)
    account_number = db.Column(db.Text)
    ifsc_code = db.Column(db.Text)
    basic_salary = db.Column(db.Integer)
    experience = db.Column(db.Integer) # experience year.

    staff_active_status = db.Column(db.Boolean, default=True) # is The Staff Now Exist in School or Not

    pf = db.Column(db.Integer) #pf.
    tax = db.Column(db.Integer) #tax.

    staff_teaching_status = db.Column(db.Boolean) # Teaching or Non-Teaching Staff.
    qualification = db.Column(db.Text)
    attendence = db.relationship('StaffAttendence', backref="staff")
    documents = db.relationship('StaffDocument', backref='staff')
    subjects = db.relationship("Subject", secondary=subject_teachers, backref="teachers")

    time_table = db.relationship("TimeTable", backref="teacher")



    def JoiningDate(self):
        joining_date = self.joining_date
        if joining_date == None:
            return ""
        indian_date = joining_date.strftime("%d-%b-%Y")
        return indian_date
    
    def BirthDate(self):
        birth_date = self.birth_date
        if birth_date == None:
            return ""
        indian_date = birth_date.strftime("%d-%b-%Y")
        return indian_date

class StaffDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.Text)
    file_name = db.Column(db.Text)
    uploaded_date = db.Column(db.Date)
    staff_id = db.Column(db.ForeignKey('staff.id'))

class StaffAttendence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.ForeignKey('staff.id'))
    present_status = db.Column(db.Text) # Present/Apsent/Leave
    attendence_date = db.Column(db.Date) # attendence date
    attendence_day = db.Column(db.Text) # attendence day
    taken_by = db.Column(db.Text) # teacher who take the attendence 


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notice_time = db.Column(db.DateTime)
    notice = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("user.id"))

class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Text)
    period_name = db.Column(db.Text) # [Period 1, Period 2, Period 3]
    period_starting_time = db.Column(db.Time) # starting time
    period_end_time = db.Column(db.Time) # end time
    teacher_id = db.Column(db.ForeignKey('staff.id'))
    subject_id = db.Column(db.ForeignKey("subject.id"))
    class_id = db.Column(db.ForeignKey("running_class.id"))



########################################################################################################################################################
#################################################################  VIEWS ###############################################################################
########################################################################################################################################################



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return "about page..."

@app.route(AdminUrl(""))
@login_required
def admin_url():
    return redirect(url_for('dashboard'))

@app.route(AdminUrl('/dashboard'))
@login_required
def dashboard():
    # Staff Today's Attendence
    # Student Today's Attendence
    # Calander
    # Current Time (time-table)
    
    # Current Month Total Fee Collect ..
    return render_template('dashboard.html')


##########################################################################################################################
############################################### CLASSES VIEWS ############################################################
##########################################################################################################################


@app.route(AdminUrl('/all_clases'))
@login_required
def all_clases():
    if admin_access():
        clases = Standared.query.all()
        return render_template("all_clases.html", clases=clases)
    else:
        return "User Not Allowed"

@app.route(AdminUrl('/add_class'), methods=['GET', 'POST'])
@login_required
def add_class():
    # add new class to the school
    # admin access
    if admin_access():
        if request.method == 'POST':
            class_name = request.form['class_name']
            try:
                class_name = class_name.upper()
                new_class = Standared(class_name=class_name)
                db.session.add(new_class)
                db.session.commit()
                flash(f"The New Class {class_name} Is Added To Your School")
            except IntegrityError:
                flash('This Class Already in Your School')
            
            return redirect(url_for("all_clases"))

    else:
        return "Method Not Allowed"
    

@app.route(AdminUrl('/delete_class/<class_id>'))
@login_required
def delete_class(class_id):
    # admin access
    if admin_access():
        try:
            clas = db.get_or_404(Standared, class_id)
        
            clas_name = clas.class_name
            db.session.delete(clas)
            db.session.commit()
            flash(f"{clas_name} Has Been Removed from Your School.")
        
        except:    
            flash('This Class Has Already Removed from Your School')
        
        redirect_url = f"{url_for('all_clases')}"
        return redirect(redirect_url)
    return "user not allowed"

@app.route(AdminUrl('/map_clases'), methods=['GET', 'POST'])
@login_required
def map_clases():
    # admin access
    if admin_access():
        session_year = request.args.get('session_year')
        running_session = SessionYear.query.filter_by(session_year = session_year).first()
        
        if session_year == None:
            
            session_id = SessionYear.query.count()
            running_session = db.get_or_404(SessionYear, session_id)
            if running_session == None:
                session_counts = SessionYear.query.count()
                running_session = db.get_or_404(SessionYear, session_counts)

        if request.method == 'POST':
            session_year = request.form['session_year']
            running_session = SessionYear.query.filter_by(session_year=session_year).first()
            class_id = request.form['class_id']
            section_id = request.form['section_id']
            
            selected_section = db.get_or_404(Section, section_id)
            selected_class = db.get_or_404(Standared, class_id)
            if selected_section not in selected_class.sections:
                selected_class.sections.append(selected_section)
            if selected_class not in running_session.classes:
                running_session.classes.append(selected_class)
            
            db.session.commit()
            try:
                new_running_class = RunningClass(class_id=class_id, session_id=running_session.id, section_id=section_id)
                db.session.add(new_running_class)
                db.session.commit()
                flash(f"The Stream or Section ({selected_section.section_name}) is added to the class ({selected_class.class_name})")

            
            except IntegrityError:
                
                flash('This Class & section and Session already map with each other')
            
            return redirect(url_for('map_clases'))


        
        clases = Standared.query.all()
        sections = Section.query.all()
        sessions = SessionYear.query.all()
        return render_template('map_class.html', running_session=running_session, sessions=sessions, session_year=session_year, clases=clases, sections=sections)
    else:
        return 'User Not Allowed'


#####################################################################################################################################################
#################################################################### SESSION AREA ###################################################################
#####################################################################################################################################################

@app.route(AdminUrl('/all_sessions'), methods=['GET', 'POST'])
@login_required
def all_session():
    # admin accesss
    if admin_access():
        current_year = datetime.now().date().year
        session_year_list = []
        for n in range(3):
            session_year = {"session_year": current_year, "visible_value": f"{current_year} - {current_year + 1}"}
            current_year += 1
            session_year_list.append(session_year)
        sessions = SessionYear.query.all()
        return render_template('all_session.html', sessions = sessions, session_year_list=session_year_list)
    return "user not allowed"


@app.route(AdminUrl('/add_session'), methods=['GET', 'POST'])
@login_required
def add_session():
    # admin access
    if admin_access():
        if request.method == 'POST':
            if request.method == 'POST':
                try:
                    session_year = int(request.form['session_year'])
                    session_name = f"{session_year}-{session_year + 1}"
                    new_session = SessionYear(session_year=session_year,session_name=session_name)
                    db.session.add(new_session)
                    db.session.commit()
                    flash(f"{new_session.session_name} Session is Added Successfully To Your School")
                    return redirect(url_for('all_session'))
                except IntegrityError:
                    flash(f"The Session {session_year} is already running in your Schood")
                    return redirect(url_for('all_session'))
            
    else:
        return "user not allowed"


@app.route(AdminUrl('/delete_session/<session_id>'))
@login_required
def delete_session(session_id):
    # admin access
    if admin_access():
        try:
            current_session = db.get_or_404(SessionYear, session_id)
            session_name = current_session.session_name
            db.session.delete(current_session)
            db.session.commit()
            flash(f"{session_name} is Deleted From Your School Successfully !")
        except:
            flash('This Session has already removed from your school')

        return redirect(url_for("all_session"))
    return "user not allowed"


########################################################################################################################################################
################################################### SECTION AND STREAM #################################################################################
########################################################################################################################################################

@app.route(AdminUrl('/all_section'))
@login_required
def all_section():
    if admin_access():
        sections = Section.query.all()
        return render_template('all_sections.html', sections=sections)
    return "user not allowed"


@app.route(AdminUrl('/add_section'), methods=['GET', 'POST'])
@login_required
def add_section():
    # admin access
    if admin_access():
        if request.method == 'POST':
            try:
    
                section_name = request.form['section_name']
                section_name = section_name.title()
                new_section = Section(section_name=section_name)
                db.session.add(new_section)
                db.session.commit()
                flash(f'New Section or Stream ({section_name}) Added To Your School.')
                
            except IntegrityError:
                flash('This Section is Already in Your School')

            return redirect(url_for("all_section"))
                
    else:
        return "user not allowed"

@app.route(AdminUrl('/delete_section/<section_id>'))
@login_required
def delete_section(section_id):
    # admin access
    if admin_access():
        try:
            selected_section = db.get_or_404(Section, section_id)
            section_name = selected_section.section_name
            db.session.delete(selected_section)
            db.session.commit()
            flash(f"The Section or Stream : ( {section_name} ) has been removed from your School")
        except:
            flash('The Stection or Stream is Already Removed From Your School')

        return redirect(url_for("all_section"))
    return "user not allowed"


########################################################################################################################################################
############################################################# SUBJECTS VIEWS ###########################################################################
########################################################################################################################################################

@app.route(AdminUrl('/all_subjects'))
@login_required
def all_subjects():
    if admin_access():
        subjects = Subject.query.all()
        return render_template('all_subject.html', subjects=subjects)

    return "user not allowed"


@app.route(AdminUrl('/add_subject'), methods=['GET', 'POST'])
@login_required
def add_subject():
    # admin access
    if admin_access():
        if request.method == 'POST':
            subject_name = request.form['subject']
            subject_name = subject_name.title()
            try:
                new_subject = Subject(subject_name=subject_name)
                db.session.add(new_subject)
                db.session.commit()
                flash(f"{subject_name} is Added in Your School")

            except IntegrityError:
                flash(f'{subject_name} is already There in Your School')
            return redirect(url_for('all_subjects'))
        else:
            return 'Method Not Available'
    
    return "user not allowed"


@app.route(AdminUrl('/delete_subject/<subject_id>'))
@login_required
def delete_subject(subject_id):
    # admin access
    if admin_access():
        try:
            subject = db.get_or_404(Subject, subject_id)
            subject_name = subject.subject_name
            db.session.delete(subject)
            db.session.commit()
            flash(f"{subject_name} Has Been Removed From Your School !")
        except:
            flash('Subject has Already Removed from Your School !')
        return redirect(url_for('all_subjects'))

    return "user not allowed"


@app.route(AdminUrl('/map_subject'), methods=['GET', 'POST'])
@login_required
def map_subject():
    if admin_access():
        session_year = request.args.get('session_year')
        running_session = SessionYear.query.filter_by(session_year = session_year).first()
        
        if session_year == None:
            
            running_year = str(datetime.now().year)
            running_session = SessionYear.query.filter_by(session_year = running_year).first()
            if running_session == None:
                session_counts = SessionYear.query.count()
                running_session = db.get_or_404(SessionYear, session_counts)

        if request.method == 'POST':
        
            session_year = request.form['session_year']
            class_id = request.form['class_id']
            section_id = request.form['section']
            subject_id = request.form['subject']
            session = SessionYear.query.filter_by(session_year=session_year).first()
            class_unique_id = f"{session.id}-{class_id}-{section_id}"
            
            running_class = RunningClass.query.filter_by(running_class_unique_id=class_unique_id).first()
            selected_subject = db.get_or_404(Subject, subject_id)

            if selected_subject in running_class.subjects:
                flash(f'The Subject: {selected_subject.subject_name} is Already in The Class {running_class.class_name()}')

            else:
                running_class.subjects.append(selected_subject)
                db.session.commit()
                flash(f"The New Subject: ({selected_subject.subject_name}) is Added to The Class ({running_class.class_name()})")
        
            
            return redirect(url_for('map_subject'))


        clases = Standared.query.all()
        sections = Section.query.all()
        sessions = SessionYear.query.all()
        subjects = Subject.query.all()

        return render_template('map_subject.html', running_session=running_session, sessions=sessions, session_year=session_year, clases=clases, sections=sections, subjects=subjects)

    return "user not allowed"

@app.route(AdminUrl('/map_subject_teacher'), methods=['GET', 'POST'])
@login_required
def map_subject_teacher():
    if admin_access():
        if request.method == 'POST':
            subject_id = request.form['subject']
            teacher_id = request.form['teacher']

            if subject_id == "" or teacher_id == "":
                flash('Please Select Proper Subject And Teacher To Join Them...')
            else:
                subject = db.get_or_404(Subject, subject_id)
                teacher = db.get_or_404(Staff, teacher_id)
                if teacher in subject.teachers:

                    flash('Teacher is already Map With  Subject')
                else:
                    subject.teachers.append(teacher)
                    db.session.commit()
                    flash(f'The Subject {subject.subject_name} is Now Tought By Teacher {teacher.name}')
            
            return redirect(url_for('map_subject_teacher'))
                
        else:
            subjects = Subject.query.all()
            teachers = Staff.query.filter(Staff.staff_teaching_status == True, Staff.staff_active_status == True).all()
            return render_template('map_subject_teacher.html', subjects = subjects, teachers=teachers)

    return "user not allowed"


@app.route(AdminUrl('/map_teacher_class'), methods=['GET', 'POST'])
@login_required
def map_teacher_class():
    if admin_access():
        if request.method == 'POST':
            class_id = request.form['class_id']
            teacher_id = request.form['teacher_id']

            if class_id == "" or teacher_id  == "":
                flash('Please Select Proper Class And Teacher To Join Them')
            else:
                running_class = db.get_or_404(RunningClass, class_id)
                teacher = db.get_or_404(Staff, teacher_id)
                if teacher in running_class.teachers:
                    flash('Teacher already in This Class')
                else:
                    running_class.teachers.append(teacher)
                    db.session.commit()
                    flash(f'The Teacher {teacher.name} Added To Class {running_class.class_name()}')

            return redirect(url_for('map_teacher_class'))
        else:
            running_session = SessionYear.query.count()
            running_session = db.get_or_404(SessionYear, running_session)
            classes = running_session.main_classes
            teachers = Staff.query.filter(Staff.staff_teaching_status == True, Staff.staff_active_status == True).all()
            return render_template('map_teacher_class.html', classes = classes, teachers=teachers)

    return "user not allowed"


########################################################################################################################################################
####################################################### Add Profile Page Form ##########################################################################
########################################################################################################################################################

@app.route(AdminUrl('/all_credentials'))
@login_required
def all_credentials():
    if admin_access():
        all_users = User.query.all()
        return render_template('all_users.html', all_users=all_users)
    else:
        "Not Allowed..."

@app.route(AdminUrl('/delete_user/<user_id>'))
@login_required
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route(AdminUrl('/add_user/<staff_id>'), methods=['GET', 'POST'])
@login_required
def add_user(staff_id):
    if admin_access():
        staff = db.get_or_404(Staff, staff_id)
        if staff == None:
            return "This Staff Member Not Exist..."
        else:
            if request.method == 'POST':
                try:
                    login_id = request.form['login_id'] + "@sgdsd.com"
                    password = request.form['password']
                    user_type = request.form['user_type']

                    new_user = User(name=staff.name, login_id=login_id, password=password, user_type=user_type, teacher_id=staff_id)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('New User Has Been Created Successfully')

                except IntegrityError:
                    flash('This User Already in Exist')
                return redirect(url_for('add_user', staff_id=staff_id))
            
            user = User.query.filter(User.teacher_id == staff_id).first()
            if user == None:
                user = {"user_name": "", "password": ""}
            else:
                login_id = user.login_id
                login_id = login_id.split("@")[0]
                user = {"user_name": login_id, "password": user.password}
            return render_template('add_user.html', staff=staff, user=user)
    else:
        return "user not allowed"



@app.route(AdminUrl('/add_student'), methods=['GET', 'POST'])
@login_required
def add_student():
    if admin_access():
        # clerk access
        if request.method == 'POST':
            try:
                name = request.form['name']
                father_name = request.form['father_name']
                mother_name = request.form['mother_name']
                admision_number = request.form['admision_number']
                phone_number = request.form['phone_number']
                secondary_phone_number = request.form['secondary_phone_number']
                birth_date = request.form['birth_date']
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
                admision_date = request.form['admision_date']
                gender = request.form['gender']
                blood_group = request.form['blood_group']
                social_category = request.form['social_category']
                aadhar_number = request.form['aadhar_number']
                
                class_id = request.form['standared']

                section_id = request.form['section']

                address = request.form['address']


                admision_date = datetime.strptime(admision_date, "%Y-%m-%d")
                admision_year = str(admision_date.year)
                
                running_session = SessionYear.query.filter_by(session_year = admision_year).first()
                session_id = running_session.id

                
                student = StudentDetail(name=name, father_name=father_name, mother_name=mother_name, admision_number=admision_number, 
                                        phone_number=phone_number, secondary_phone_number=secondary_phone_number, address = address,
                                        birth_date=birth_date, admision_date=admision_date, gender=gender,
                                        blood_group=blood_group, social_category=social_category, aadhar_number=aadhar_number)
                
                db.session.add(student)
                db.session.commit()
                
                student_crunt_class_id = f"{session_id}-{class_id}-{section_id}"
                running_class = RunningClass.query.filter_by(running_class_unique_id=student_crunt_class_id).first()
                running_class.students.append(student)
                db.session.commit()

            except IntegrityError as e:
                db.session.rollback()
                error_message = str(e.orig)

                if 'admision_number' in error_message:
                    flash('This Admision Number is Already Assigned To any another Student')

                elif 'aadhar_number' in error_message:
                    flash('The Aadhar Number is Unique and This Aadhar is Already Linked With a Student')

                else:
                    flash(error_message)

                return redirect(url_for('add_student'))

            return redirect(url_for('student_detail', student_id=student.id))
        
        clases = Standared.query.all()
        current_date = datetime.now().date()
        return render_template('add_student.html', current_date=current_date, clases=clases)

    return "user not allowed"

@app.route(AdminUrl('/remove_student/<student_id>'))
@login_required
def remove_student(student_id):
    if admin_access():
        student = db.get_or_404(StudentDetail, student_id)
        exames = student.exams
        for exam in exames:
            db.session.delete(exam)
        
        all_attendence = student.attendence
        for attendence in all_attendence:
            db.session.delete(attendence)
        
        path = os.path.join(Upload_Folder, "students", f"student_{student_id}")
        try:
            shutil.rmtree(path)
        except:
            pass
        documents = student.documents
        for document in documents:
            db.session.delete(document)
        
        db.session.delete(student)
        
        db.session.commit()
    flash('This Student Removed From YOur School')
    return redirect(url_for('all_students'))


@app.route(AdminUrl('/add_staff'), methods=['GET', 'POST'])
@login_required
def add_staff():
    # admin access
    if admin_access():
        if request.method == 'POST':
            name = request.form['name']
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            phone_number = request.form['phone_number']
            secondary_phone_number = request.form['secondary_phone_number']
            gender = request.form['gender']
            husband_name = request.form['husband_name']
            merital_status = request.form['merital_status']
            joining_date = request.form['joining_date']
            
            joining_date = datetime.strptime(joining_date, "%Y-%m-%d")
            birth_date = request.form['birth_date']
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d")

            blood_group = request.form['blood_group']
            social_category = request.form['social_category']

            aadhar_card = request.files["aadhar_card"]
            aadhar_number = request.form['aadhar_number']

            pan_card = request.files['pan_card']
            pan_number = request.form['pan_number']
            
            pin = request.form['pin']
            city = request.form['city']
            state = request.form['state']
            address = request.form['address']
            bank_name = request.form['bank_name']
            account_number = request.form['account_number']
            ifsc_code = request.form['ifsc_code']
            basic_salary = request.form['basic_salary']
            experience = request.form['experience']

            pf = request.form['pf']
            tax = request.form['tax']

            staff_teaching_status = request.form['staff_type']
            qualification = request.form['qualification']

            try:
                if staff_teaching_status == 'true':
                    staff_teaching_status = True
                    subject = request.form['subject_speciliest']
                    designation = request.form['designation']

                    new_staff = Staff(name=name, father_name=father_name, mother_name=mother_name, phone_number=phone_number, secondary_phone_number=secondary_phone_number, gender=gender
                                    ,joining_date=joining_date, birth_date=birth_date, blood_group=blood_group, social_category=social_category, aadhar_number=aadhar_number, pan_number=pan_number,
                                    pin=pin, city=city, state=state, address=address, bank_name=bank_name, account_number=account_number, ifsc_code=ifsc_code, basic_salary=basic_salary,
                                    experience=experience, pf=pf, tax=tax, staff_teaching_status=staff_teaching_status, qualification=qualification, subject=subject, designation=designation,
                                    husband_name=husband_name, merital_status=merital_status)

                else:
                    staff_teaching_status = False
                    new_staff = Staff(name=name, father_name=father_name, mother_name=mother_name, phone_number=phone_number, secondary_phone_number=secondary_phone_number, gender=gender
                            ,joining_date=joining_date, birth_date=birth_date, blood_group=blood_group, social_category=social_category, aadhar_number=aadhar_number, pan_number=pan_number,
                            pin=pin, city=city, state=state, address=address, bank_name=bank_name, account_number=account_number, ifsc_code=ifsc_code, basic_salary=basic_salary,
                            experience=experience, pf=pf, tax=tax, staff_teaching_status=staff_teaching_status, qualification=qualification,
                            husband_name=husband_name, merital_status=merital_status)
                
                db.session.add(new_staff)
                db.session.commit()

                staff_id = new_staff.id
                
                teacher_directory = os.path.join(os.getcwd(), "uploads", "Staff", f"staff_{staff_id}")
                print(teacher_directory)
                if os.path.exists(teacher_directory):
                    pass
                else:
                    os.makedirs(teacher_directory)

                
                aadhar_card_file_name =  aadhar_card.filename
                extension_name = aadhar_card_file_name.split(".")[1]
                aadhar_card_file_name = f"{teacher_directory}/Document.{extension_name}"


                aadhar_card.save(aadhar_card_file_name)

            

                aadhar_document = StaffDocument(document_name = 'Aadhar Card', staff_id = staff_id, file_name = f"Document.{extension_name}", uploaded_date = datetime.now().date())
                print(aadhar_document, "\naadhar card is going to save in database....\n")
                db.session.add(aadhar_document)
                db.session.commit()
                
                pan_card_file_name = pan_card.filename
                extension_name = pan_card_file_name.split(".")[1]
                pan_card_file_name = f"{teacher_directory}/Document_1.{extension_name}"
                print(pan_card_file_name, '\n pan card is going to save...')
                pan_card.save(pan_card_file_name)

                pan_document = StaffDocument(document_name = 'PAN Card', staff_id = staff_id, file_name = f"Document_1.{extension_name}", uploaded_date=datetime.now().date())
                db.session.add(pan_document)
                db.session.commit()

                return redirect(url_for('staff_detail', staff_id=staff_id))


            except IntegrityError as e:
                db.session.rollback()
                error_message = str(e.orig)

                if 'aadhar_number' in error_message:
                    flash('The Aadhar Number is Unique and This Aadhar is Already Linked With another Stamm Member !')

                elif "pan_number" in error_message.message:
                    flash('Pan Number is A Unique Id And This Pan Number is Already Linked With another Staff Member !')
                else:
                    flash(error_message)

                return redirect(url_for('add_staff'))

        return render_template('add_staff.html', current_date = datetime.now().date())

    return "user not allowed"



########################################################################################################################################################
################################################################## STUDENT PROFILE #####################################################################
########################################################################################################################################################

@app.route(AdminUrl('/student_detail/<student_id>'))
@login_required
def student_detail(student_id):
    student = db.get_or_404(StudentDetail, student_id)
    session = request.args.get("session")
    if session == None:
        classes = student.classes
        print(classes)
        last_class = classes[len(classes) - 1]
    else:
        running_session = SessionYear.query.filter_by(session_year = session).first()
        if running_session == None:
            return redirect(url_for('student_detail', student_id=student_id))
        
        all_clases = student.classes
        for clas in all_clases:
            if clas.session_id == running_session.id:
                last_class = clas
                break



    return render_template('student_detail.html', student=student, last_class=last_class)


@app.route(AdminUrl('/update_student_profile/<student_id>'), methods= ['POST'])
@login_required
def update_student_profile(student_id):
    if request.method == 'POST':
        # try:
        student = db.get_or_404(StudentDetail, student_id)
        student.name = request.form['name']
        student.gender = request.form['gender']
        birth_date = request.form['birth_date']
        student.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        
        admision_date = request.form['admision_date']
        student.admision_date = datetime.strptime(admision_date, "%Y-%m-%d")

        student.father_name = request.form['father_name']
        student.mother_name = request.form['mother_name']
        student.phone_number = request.form['phone_no']
        student.secondary_phone_number = request.form['secondary_mobile']
        student.address = request.form['address']
        student.blood_group = request.form['blood_group']
        
        student.social_category = request.form['social_catogry']
        student.aadhar_number = request.form['aadhar_no']
        db.session.commit()
        
        last_session = SessionYear.query.count()
        session_year = db.get_or_404(SessionYear, last_session)
        current_class = request.form['current_class']
        current_section = request.form['current_section']
        running_class = RunningClass.query.filter(RunningClass.class_id == current_class, RunningClass.section_id==current_section, RunningClass.session_id==session_year.id).first()
        
        if student not in running_class.students:
            last_class = student.get_last_class()
            
            if last_class.session_id == session_year.id:
                last_class.students.remove(student)
                db.session.commit()
            
            running_class.students.append(student)
            db.session.commit()
        # except Exception as e:
        #     flash(f"There is Some Error {e}")
        
        return redirect(url_for('student_detail', student_id=student.id))

@app.route(AdminUrl('/update_staff_detail/<staff_id>'), methods=['POST'])
@login_required
def update_staff_detail(staff_id):
    if request.method == 'POST':
        staff = db.get_or_404(Staff, staff_id)
        staff.name = request.form['name']
        staff.gender = request.form['gender']
        birth_date = request.form['birth_date']
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        staff.birth_date = birth_date
        joining_date = request.form['joining_date']
        joining_date = datetime.strptime(joining_date, "%Y-%m-%d")
        staff.joining_date = joining_date
        staff.father_name = request.form['father_name']
        staff.mother_name = request.form['mother_name']
        staff.phone_number = request.form['phone_no']
        staff.secondary_phone_number = request.form['secondary_mobile']
        staff.address = request.form['address']
        staff.blood_group = request.form['blood_group']
        staff.social_category = request.form['social_category']
        staff.aadhar_number = request.form['aadhar_number']
        staff.pan_number = request.form['pan_number']
        staff.basic_salary = request.form['basic_salary']
        staff.bank_name = request.form['bank_name']
        staff.ifsc_code = request.form['ifsc_code']
        staff.account_number = request.form['account_number']
        staff.experience = request.form['experience']
        db.session.commit()
    
        return redirect(url_for('staff_detail', staff_id=staff_id))
    


@app.route(AdminUrl('/add_comment/<student_id>'), methods=['GET', 'POST'])
@login_required
def add_comment(student_id):
    if request.method == 'POST':
        comment = request.form['comment']
        new_comment = Comment(comment=comment, student_id=student_id, user_id = current_user.id, comment_time=datetime.now())
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('student_detail', student_id=student_id))
    
    return "Method Not Allowed"



@app.route(AdminUrl('/all_students'))
@login_required
def all_students():
    admision_number = request.args.get('admision_number')
    # student_type = request.args.get('student_type') # Regular, New Admision, Pass Out Students

    father_name = request.args.get('father_name')
    mother_name = request.args.get('mother_name')

    session_counts = SessionYear.query.count()
    running_session = db.get_or_404(SessionYear, session_counts)
    
    admision_number = request.args.get('admision_number')
    if admision_number == None:
        admision_number = ""


    data_counts = 10
        

    
    class_id = request.args.get('class_id')
    if class_id == None:
        class_id = ""
    
    section_id = request.args.get('section_id')
    if section_id == None:
        section_id = ""
    
    name = request.args.get("name")
    if name == None:
        name = ""
    
    father_name = request.args.get('father_name')
    if father_name == None:
        father_name = ""

    mother_name = request.args.get('mother_name')
    if mother_name == None:
        mother_name = ""
    

    aadhar_number = request.args.get('aadhar_number')
    if aadhar_number == None:
        aadhar_number = ""


    if class_id == "" and section_id == "":
        if admision_number != "":
            students = StudentDetail.query.filter_by(admision_number=admision_number).all()

        else:
            students = StudentDetail.query.filter(StudentDetail.name.like(f'%{name}%'), StudentDetail.father_name.like(f"%{father_name}%"), StudentDetail.mother_name.like(f"%{mother_name}%")).limit(data_counts).all()
            

    else:

        
        if admision_number != "":
            students = StudentDetail.query.filter(StudentDetail.admision_number==admision_number).all()
            
            return render_template("all_student.html",students = students, running_session=running_session, name=name, father_name=father_name, mother_name=mother_name)
            

        elif class_id != "" and section_id != "":
            
            running_class = RunningClass.query.filter_by(class_id=class_id, section_id=section_id, session_id=running_session.id).first()
            if running_class == None:
                students = []
            else:
                students = StudentDetail.query.filter(StudentDetail.classes.any(id=running_class.id), StudentDetail.name.like(f'%{name}%'), StudentDetail.father_name.like(f"%{father_name}%"), StudentDetail.mother_name.like(f"%{mother_name}%")).limit(data_counts).all()
            return render_template("all_student.html",students = students, running_session=running_session, name=name, father_name=father_name, mother_name=mother_name)

        elif class_id != "" and section_id == "":
            
            running_clases = RunningClass.query.filter_by(session_id = running_session.id, class_id = class_id).all()

        elif class_id == "" and section_id != "":
            
            running_clases = RunningClass.query.filter_by(session_id=running_session.id,section_id = section_id).all()
            
        
        students = []
        for class_obj  in running_clases:
            
            for student in class_obj.students:
                if len(students) < 10:
                    if (name.lower() in str(student.name).lower() and father_name.lower() in student.father_name.lower() and mother_name.lower() in student.mother_name.lower() and aadhar_number.lower() in str(student.aadhar_number) and admision_number in str(student.admision_number)):
                        students.append(student)
                else:
                    break
    

    return render_template("all_student.html",students = students, running_session=running_session, name=name, father_name=father_name, mother_name=mother_name)


########################################################################################################################################################
################################################################## STAFF PROFILE #######################################################################
########################################################################################################################################################
@app.route(AdminUrl('/staff_detail/<staff_id>'))
@login_required
def staff_detail(staff_id):
    staff_member = db.get_or_404(Staff, staff_id)
    return render_template('staff_detail.html', staff_member=staff_member)

@app.route(AdminUrl('/staf_list'))
@login_required
def staf_list():
    name = request.args.get('name')
    if name == None:
        name = ""

    phone_number = request.args.get("phone_number")
    if phone_number == None:
        phone_number = ""
    aadhar_number = request.args.get('aadhar_number')
    if aadhar_number == None:
        aadhar_number = ""
    designation = request.args.get('designation')
    if designation == None:
        designation = ""
    pan_number = request.args.get('pan_number')
    if pan_number == None:
        pan_number = ""

    current_staff = request.args.get('current_staff') # Current Staff / Old Staff
    if current_staff == None:
        current_staff = "Current Staff"

    
    if current_staff == "Current Staff":
        staff_active_status = True
    else:
        staff_active_status = False
    
    staff_teaching_status = request.args.get('staff_type') # Teaching staff / Non-Teaching Staff
    if staff_teaching_status == None or staff_teaching_status == "":
        staff_teaching_status = ""
        all_staff = Staff.query.filter(Staff.name.contains(name), Staff.designation.contains(designation), Staff.staff_active_status == staff_active_status, Staff.phone_number.contains(phone_number), Staff.aadhar_number.contains(aadhar_number), Staff.pan_number.contains(pan_number)).limit(10).all()

    else:
        if staff_teaching_status == 'true':
            staff_teaching_status = True
        else:
            staff_teaching_status = False

        all_staff = Staff.query.filter(Staff.name.contains(name), Staff.designation.contains(designation), Staff.staff_active_status == staff_active_status, Staff.phone_number.contains(phone_number), Staff.aadhar_number.contains(aadhar_number), Staff.pan_number.contains(pan_number), Staff.staff_teaching_status == staff_teaching_status).limit(10).all()

    if len(all_staff) == 0:
        min_id = 0
    else:
        min_id = all_staff[len(all_staff) - 1].id
    return render_template('staf_list.html', all_staff=all_staff, name=name, staff_teaching_status=staff_teaching_status, min_id=min_id, phone_number=phone_number, aadhar_number=aadhar_number, pan_number=pan_number, designation=designation, staff_active_status = staff_active_status)


#######################################################################################################################################################
################################################################# ATTENDENCE ##########################################################################
#######################################################################################################################################################

@app.route(AdminUrl('/add_attendence'), methods=['GET', 'POST'])
@login_required
def add_attendence():
    if request.method == 'POST':
        attendence = request.form['attendence_date']
        class_id = request.form['class']

        all_attendence = request.form

        return_data = {}
        
        if class_id == 'teachers':
            today_first_attendence = StaffAttendence.query.filter_by(attendence_date = datetime.now().date()).first()
            if today_first_attendence != None:
                for attendence in all_attendence:
                    
                    if attendence == 'attendence_date' or attendence == 'class' or attendence == 'section':
                        pass
                     
                    else:
                        current_attendence = StaffAttendence.query.filter_by(attendence_date = datetime.now().date(), staff_id = attendence).first()
                        current_attendence.taken_by = current_user.name
                        current_attendence.present_status = request.form[attendence]

                    db.session.commit()

                flash ('Staff Attendence Updated Successfully !')
                return redirect( url_for('add_attendence'))
            else:

                for attendence in all_attendence:
                    
                    if attendence == 'attendence_date' or attendence == 'class' or attendence == 'section':
                        pass

                    else:
                        
                        new_attendence = StaffAttendence(staff_id=attendence, present_status=request.form[attendence], attendence_date = datetime.now().date(), attendence_day=str(datetime.now().strftime("%A")), taken_by=current_user.name)
                        db.session.add(new_attendence)

                    db.session.commit()


                flash('Staff Attendence Added Successfully !')
                return redirect (url_for('add_attendence'))
        else:
            section_id = request.form['section']
            running_session = SessionYear.query.count()
            running_session = db.get_or_404(SessionYear, running_session)
            running_class = RunningClass.query.filter_by(class_id=class_id, section_id=section_id, session_id = running_session.id).first()


            today_first_attendence = StudentAttendence.query.filter_by(class_id=running_class.id, attendence_date = datetime.now().date()).first()

            if today_first_attendence != None:

                for attendence in all_attendence:
                    
                    if attendence == 'attendence_date' or attendence == 'class' or attendence == 'section':
                        pass
                    else:
                        return_data[attendence] = all_attendence[attendence]
                        current_attendence = StudentAttendence.query.filter_by(attendence_date = datetime.now().date(), student_id = attendence).first()
                        current_attendence.present_status = request.form[attendence]
                        current_attendence.taken_by = current_user.name

                db.session.commit()


                flash (f"Today's Attendence Of Class :- {running_class.class_name()} is Updated Successfully")
                return redirect( url_for('add_attendence'))
            else:
                for attendence in all_attendence:
                    
                    if attendence == 'attendence_date' or attendence == 'class' or attendence == 'section':
                        pass
                    else:
                        return_data[attendence] = all_attendence[attendence]
                        
                        new_attendence = StudentAttendence(class_id = running_class.id, student_id=attendence, present_status=request.form[attendence], attendence_date = datetime.now().date(), attendence_day=str(datetime.now().strftime("%A")), taken_by=current_user.name)
                        db.session.add(new_attendence)
                        db.session.commit()

                            
                flash(f"Today's Attendence of Class {running_class.class_name()} is Added Successfully.")
                return redirect( url_for('add_attendence') )

    current_date = datetime.now().date()
    return render_template('add_attendence.html', current_date=current_date)


@app.route(AdminUrl('/show_student_attendence'))
@login_required
def show_student_attendence():
    attendence_type = request.args.get('attendence_type')
    attendence_date = request.args.get('attendence_date')


    if attendence_type == None or attendence_type == 'Daily':
        attendence_type = 'Daily'
        if attendence_date == None:
            attendence_date = datetime.now().date()


    else:
        attendence_type == 'Monthly'

        if attendence_date == None or attendence_date == "":
            attendence_date = datetime.now().date()
            attendence_date = attendence_date.strftime("%Y-%m")

    return render_template('show_student_attendence.html', attendence_type = attendence_type, attendence_date = attendence_date)

@app.route(AdminUrl('/show_staff_attendence'))
@login_required
def show_staff_attendence():
    attendence_type = request.args.get('attendence_type')
    attendence_date = request.args.get('attendence_date')


    if attendence_type == None or attendence_type == 'Daily':
        attendence_type = 'Daily'
        if attendence_date == None:
            attendence_date = datetime.now().date()


    else:
        attendence_type == 'Monthly'

        if attendence_date == None or attendence_date == "":
            attendence_date = datetime.now().date()
            attendence_date = attendence_date.strftime("%Y-%m")

    return render_template('show_staff_attendence.html', attendence_type = attendence_type, attendence_date = attendence_date)

@app.route(AdminUrl('/show_attendence'))
@login_required
def show_attendence():

    all_classes = Standared.query.all()

    attendence_date = request.args.get('attendence_date')
    
    if attendence_date == None or attendence_date == "":
        attendence_date = datetime.now().date()
    else:
        attendence_date = datetime.strptime(attendence_date, "%Y-%m-%d").date()
    
    running_class_id = request.args.get('running_class_id')

    if running_class_id == None:

        selected_class = request.args.get("attendence_class")
        if selected_class == None:
            selected_class = ""

        section_id = request.args.get('section')
        if section_id == None or section_id == "":
            selected_section = {"section_id": "", "section_name": "Chose Section"}
        else:
            selected_section = db.get_or_404(Section, section_id)
        
        try:
            if selected_class == "" or selected_section['section_id'] == "":
                flash("This Class Doesn't Exist ! Please Select Select Class And Section Porperly !")
        except:
            pass    
        return render_template('show_attendence.html', attendence_date=attendence_date,all_classes=all_classes, selected_class = selected_class, selected_section=selected_section)

    else:
        running_class = db.get_or_404(RunningClass, running_class_id)
        
        redirect_url = url_for('show_attendence') + f"?attendence_date={attendence_date}&attendence_class={running_class.class_id}&section={running_class.section_id}"
        
        return redirect(redirect_url)


#######################################################################################################################################################
############################################################## DOCUMENT ###############################################################################
#######################################################################################################################################################
    
@app.route(AdminUrl('/save_staff_document/<staff_id>'), methods=['POST', 'GET'])
@login_required
def save_staff_document(staff_id):
    if request.method == 'POST':
        document_name = request.form['document_name']
        document_file = request.files['document_file']


        student_directory = os.path.join(os.getcwd() , "uploads", "Staff", f'staff_{staff_id}')
        if os.path.exists(student_directory):
            pass
        else:
            os.mkdir(student_directory)
            

        staff = db.get_or_404(Staff, staff_id)
        staff_document = staff.documents

        if len(staff_document) == 0:
            new_document_name = "Document"

        else:
            documents_counts = len(staff_document) - 1
            last_document = staff_document[documents_counts]
            last_document_name = last_document.file_name
            if last_document_name.split(".")[0] == "Document":
                new_document_name = "Document_1"
            else:
                new_document_name = int(last_document_name.split(".")[0].split("_")[1]) + 1
                new_document_name = f"Document_{new_document_name}"
        
        document_file_name = document_file.filename
        extension_name = document_file_name.split(".")


        extension_name = extension_name[len(extension_name) - 1]

        new_file_name = os.path.join(student_directory, f"{new_document_name}.{extension_name}")

        document_file.save(new_file_name)


        new_document = StaffDocument(file_name = new_document_name + "." + extension_name, document_name = document_name, uploaded_date = datetime.now().date(), staff_id = staff_id)
        db.session.add(new_document)
        db.session.commit()

        flash(f"Your { document_name } has Been Uploaded Successfully...")
        return redirect(url_for('staff_detail', staff_id = staff_id))


    else:
        return "Method Not Allowed..."

@app.route(AdminUrl('/save_student_document/<student_id>'), methods=['GET', 'POST'])
@login_required
def save_student_document(student_id):
    if request.method == 'POST':
        document_name = request.form['document_name']
        document_file = request.files['document_file']


        student_directory = os.path.join(os.getcwd() , "uploads", "students", f'student_{student_id}')
        print(student_directory)
        print('code ni fata')
        if os.path.exists(student_directory):
            pass
        else:
            os.mkdir(student_directory)



        student = db.get_or_404(StudentDetail, student_id)
        student_documents = student.documents
        
        if len(student_documents) == 0:
            new_document_name = "Document"

        else:
            documents_counts = len(student_documents) - 1
            last_document = student_documents[documents_counts]
            last_document_name = last_document.file_name
            if last_document_name.split(".")[0] == "Document":
                new_document_name = "Document_1"
            else:
                new_document_name = int(last_document_name.split(".")[0].split("_")[1]) + 1
                new_document_name = f"Document_{new_document_name}"
        
        document_file_name = document_file.filename
        extension_name = document_file_name.split(".")


        extension_name = extension_name[len(extension_name) - 1]

        new_file_name = os.path.join(student_directory, f"{new_document_name}.{extension_name}")

        document_file.save(new_file_name)


        student_document = Document(file_name = new_document_name + "." + extension_name, document_name = document_name, uploaded_date = datetime.now().date(), student_id = student_id)
        db.session.add(student_document)
        db.session.commit()

        flash(f"Your { document_name } has Been Uploaded Successfully...")
        return redirect(url_for('student_detail', student_id = student_id))


    else:
        return "Method Not Allowed..."

@app.route(AdminUrl('/get_individual_document'))
@login_required
def get_individual_document():

    request_for = request.args.get('request_for')
    document_id = request.args.get('document_id')

    if request_for == 'Staff':
        document = db.get_or_404(StaffDocument, document_id)
        document_file = os.path.join("uploads", "Staff", f"staff_{document.staff_id}", document.file_name)
    elif request_for == 'Student':
        document = db.get_or_404(Document, document_id)
        document_file = os.path.join("uploads", "students", f"student_{document.student_id}", document.file_name)

    return send_file(document_file)

@app.route(AdminUrl('/delete_individual_document'))
@login_required
def delete_individual_document():
    request_for = request.args.get('request_for')
    document_id = request.args.get('document_id')

    if request_for == 'Staff':
        document = db.get_or_404(StaffDocument, document_id)
        document_file_path = os.path.join("uploads", "Staff", f"staff_{document.staff_id}", document.file_name)
        os.remove(document_file_path)

        document_name = document.document_name
        staff_id = document.staff_id
        db.session.delete(document)
        db.session.commit()

        flash(f'{document_name} Has Been Deleted From The Document List')
        return redirect(url_for('staff_detail', staff_id = staff_id))
    
    elif request_for == 'Student':
        document = db.get_or_404(Document, document_id)
        document_file_path = os.path.join("uploads", "students", f"student_{document.student_id}", document.file_name)
        os.remove(document_file_path)

        student_id = document.student_id
        document_name = document.document_name
        db.session.delete(document)
        db.session.commit()


        flash(f'{document_name} Has Been Removed From The Document List')
        return redirect(url_for('student_detail', student_id = student_id))
    



#####################################################################################################################################################
################################################### WRITE STUDENTS AND STAFF USING EXCEL ############################################################
#####################################################################################################################################################

@app.route(AdminUrl('/write_students_using_excel'), methods=['POST'])
@login_required
def write_students_using_excel():
    if request.method == 'POST':

        document_file = request.files['student_excel_sheet']


        # student_directory = os.path.join(os.getcwd())
        file_name = os.path.join(os.getcwd(), "school_student.xlsx")
        document_file.save(file_name)
        write_students(file_name)
        os.remove(file_name)
        flash('All Students Uploaded Successfully')
        return redirect(url_for("write_staff_using_excel"))
    

@app.route(AdminUrl('/write_staff_using_excel'), methods=['GET', 'POST'])
@login_required
def write_staff_using_excel():
    if request.method == 'POST':

        staff_excel_sheet = request.files['staff_excel_sheet']
        file_name = os.path.join(os.getcwd(), "staff_sheet.xlsx")
        staff_excel_sheet.save(file_name)
        write_staff(file_name)
        os.remove(file_name)
        flash('All Staff Uploaded Successfully')
        return redirect(url_for("write_staff_using_excel"))
    else:
        return render_template('staff_excel_upload.html')




# #################################################### NOTICE #################################################################
@app.route(AdminUrl('/notice_board'), methods=['GET', 'POST'])
@login_required
def notice_board():
    if request.method == 'POST':

        notice = request.form['notice']
        notice_time = datetime.now()
        new_notice = Notice(notice_time = notice_time, notice = notice, user_id = current_user.id)
        db.session.add(new_notice)
        db.session.commit()
        flash('New Notice Has Been Created')
        return redirect(url_for('notice_board'))
    return render_template('add_notice.html')

@app.route(AdminUrl('/delete_notice/<notice_id>'))
@login_required
def delete_notice(notice_id):
    notice = db.get_or_404(Notice, notice_id)
    db.session.delete(notice)
    db.session.commit()
    return redirect(url_for('notice_board'))

# ################################################### TEXT ######################################################################
@app.route(AdminUrl('/add_exam'), methods=['GET', 'POST'])
@login_required
def add_exam():
    if request.method == 'POST':
        exam_date = request.form['exam_date']
        class_id = request.form['class_id']
        section_id = request.form['section_id']
        exam_name = request.form['exam_name']
        exam_name = exam_name.title()
        
        subject = request.form['subject']
        max_marks = request.form['max_marks']
        last_session = SessionYear.query.count()
        last_session = db.get_or_404(SessionYear, last_session)
        
        running_class = RunningClass.query.filter(RunningClass.class_id==class_id, RunningClass.section_id==section_id, RunningClass.session_id==last_session.id).first()
        exam_data = request.form
        user_id = current_user.id

        for exam  in exam_data:

            if exam == "exam_date" or exam == "max_marks" or exam == "exam_name" or exam == "class_id" or exam == "section_id" or exam == "subject":
                pass
            else:

                student_id = exam

                new_exam = Exam(exam_date=exam_date,exam_name=exam_name,subject=subject, max_marks=max_marks, marks_obtained=exam_data[exam], student_id=student_id, class_id=running_class.id, user_id=user_id)
                db.session.add(new_exam)
        db.session.commit()
        flash(f"{exam_name} Has Been Added Successfully...")
        redirect(url_for('show_exam'))
    current_date = datetime.now().date()
    return render_template('add_exam.html', current_date=current_date)

@app.route(AdminUrl('/show_exam'))
@login_required
def show_exam():
    class_id = request.args.get('class_id')
    if class_id != None:
        section_id = request.args.get('section_id')
        subject_name = request.args.get('subject')
        test_name = request.args.get('test_name')
        test_name = test_name.title()
        session_count = SessionYear.query.count()
        last_session = db.get_or_404(SessionYear, session_count)
        running_class = RunningClass.query.filter(RunningClass.class_id==class_id, RunningClass.section_id==section_id, RunningClass.session_id==last_session.id).first()
        result = Exam.query.filter(Exam.class_id==running_class.id, Exam.exam_name == test_name, Exam.subject == subject_name).all()

    else:
        result = []
    all_classes = Standared.query.all()
    all_subjects = Subject.query.all()
    return render_template('show_exam.html', all_classes=all_classes, all_subjects=all_subjects, result=result)


@app.route(DataApi('/get_student_result'))
@login_required
def get_student_result():
    student_id = request.args.get('student_id')
    from_date = request.args.get('from_date')
    if from_date == "":
        from_date = "2003-01-01"
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = request.args.get('to_date')
    if to_date == "":
        to_date = "2050-01-01"
    to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
    subject_name = request.args.get('subject_name')
    
    class_id = request.args.get('class_id')

    if subject_name == "" and class_id == "":
        students_result = Exam.query.filter(Exam.student_id == student_id, Exam.exam_date >= from_date, Exam.exam_date < to_date).all()

    elif subject_name == "" and class_id != "":
        students_result = Exam.query.filter(Exam.student_id == student_id, Exam.exam_date >= from_date, Exam.class_id == class_id, Exam.exam_date < to_date).all()

    elif subject_name != "" and class_id == "":
        students_result = Exam.query.filter(Exam.student_id == student_id, Exam.subject == subject_name, Exam.exam_date >= from_date, Exam.exam_date < to_date).all()

    else:
        students_result = Exam.query.filter(Exam.student_id == student_id, Exam.subject == subject_name, Exam.class_id == class_id, Exam.exam_date >= from_date, Exam.exam_date < to_date).all()

    return_data = []
    for result in students_result:
        append_data = {"exam_date": result.exam_date.strftime("%d-%b-%Y"), "exam_name": result.exam_name, "marks_obtained": result.marks_obtained, "max_marks": result.max_marks, "subject": result.subject}
        return_data.append(append_data)

    return return_data

@app.route(DataApi('/get_student_all_classes'))
@login_required
def get_student_all_classes():
    student_id = request.args.get('student_id')
    student = db.get_or_404(StudentDetail, student_id)
    classes = student.classes
    return_data = []
    for clas in classes:
        return_data.append({"class_id": clas.id, "class_name": clas.class_name()})

    return return_data

# ################################################# TIME TABLE ##################################################################
@app.route(AdminUrl('/add_time_table'))
@login_required
def add_time_table():
    return render_template('time_table.html')


@app.route(AdminUrl('/update_time_table'))
@login_required
def update_time_table():
    return render_template('update_time_table.html')


@app.route(DataApi('/add_new_time_table'), methods=['POST', 'GET'])
@login_required
def add_new_time_table():
    if request.method == 'POST':
        time_table_day = request.args.get('day')
        # delete time table day data
        this_day_time_table = TimeTable.query.filter(TimeTable.day == time_table_day).all()
        if this_day_time_table == [] :
            pass
        else:
            for this_day_table in this_day_time_table:
                db.session.delete(this_day_table)

            db.session.commit()

        time_table_data = request.get_data()

        time_table_data = json.loads(time_table_data)

        for period in time_table_data:

            for clas in time_table_data[period]['period_detail']:
                new_period = TimeTable(
                    day = time_table_day,
                    period_name = period,
                    period_starting_time = datetime.strptime(time_table_data[period]['starting_time'], "%H:%M").time(),
                    period_end_time = datetime.strptime(time_table_data[period]['end_time'], "%H:%M").time(),
                    teacher_id = clas['teacher_id'],
                    subject_id = clas['subject_id'],
                    class_id = clas['class_id'],
                )
                db.session.add(new_period)
        
        db.session.commit()

        return {"status": "done"}

########################################################################################################################################################
################################################################## DATA API ############################################################################
########################################################################################################################################################

@app.route(DataApi('/get_student_time_table'))
@login_required
def get_student_time_table():
    return_data = {}
    student_id = request.args.get('student_id')
    student = db.get_or_404(StudentDetail, student_id)
    student_classes = student.classes
    running_class = student_classes[len(student_classes) - 1]
    class_time_table = TimeTable.query.filter(TimeTable.class_id == running_class.id)
    for period in class_time_table:
        subject_id = period.subject_id
        if subject_id == None or subject_id == "":
            subject = ""
        else:
            subject = period.subject.subject_name
        
        teacher_id = period.teacher
        if teacher_id == None or teacher_id == "":
            teacher = ""
        else:
            teacher = period.teacher.name
        
        append_data = {"period_name": period.period_name, "teacher_name": teacher, "subject": subject, "start_time": period.period_starting_time.strftime("%H:%M"), "end_time": period.period_end_time.strftime("%H:%M")}
        try:
            return_data[period.day].append(append_data)
        except:
            return_data[period.day] = [append_data]



    return return_data


@app.route(DataApi('/get_teacher_time_table'))
@login_required
def get_teacher_time_table():
    teacher_id = request.args.get('teacher_id')

    return_data = {}

    time_table_data = TimeTable.query.filter(TimeTable.teacher_id == teacher_id)
    for time_table in time_table_data:
        subject_id = time_table.subject_id

        if subject_id == None or subject_id == "":
            subject_name = ""
        else:
            subject_name = time_table.subject.subject_name
        
        append_data = {"period_name": time_table.period_name, "subject": subject_name, "class_name": time_table.running_class.class_name(),"start_time": time_table.period_starting_time.strftime("%H:%M"), "end_time": time_table.period_end_time.strftime("%H:%M")}
        try:
            return_data[time_table.day].append(append_data)
        except:
            return_data[time_table.day] = [append_data]

    return return_data


@app.route(DataApi('/get_current_time_table'))
@login_required
def get_current_time_table():
    current_time = datetime.now().time()
    current_day = datetime.now().strftime("%A")
    
    running_periods = TimeTable.query.filter(TimeTable.period_starting_time < current_time, TimeTable.period_end_time >= current_time, TimeTable.day == current_day).all()
    return_data = {}
    for period in running_periods:
        clas_id = period.class_id
        if clas_id == None or clas_id == "":
            class_name = ""
        else:
            class_name = period.running_class.class_name()
        
        subject_id = period.subject_id
        if subject_id == None or subject_id == "":
            subject_name = ""
        else:
            subject_name = period.subject.subject_name
        
        teacher_id = period.teacher_id
        if teacher_id == None or teacher_id == "":
            teacher_name = ""
        else:
            teacher_name = period.teacher.name
        append_data = {"class": class_name, "subject": subject_name, "teacher": teacher_name}
        try:
            return_data[period.period_name].append(append_data)
        except:
            return_data[period.period_name] = [append_data]

    return return_data

@app.route(DataApi('/get_all_time_table'))
@login_required
def get_all_time_table():
    period_day = request.args.get('day')
    return_data = {}
    all_time_table = TimeTable.query.filter(TimeTable.day == period_day).order_by(TimeTable.period_starting_time)


    for period in all_time_table:
        class_name = period.running_class.class_name()
        try:
            return_data[class_name].append({"period_name": period.period_name, "period_end_time": period.period_end_time.strftime("%H:%M"), "period_starting_time": period.period_starting_time.strftime("%H:%M"), "teacher_id": period.teacher_id, "subject_id": period.subject_id, "class_id": period.running_class.id})
        except:
            return_data[class_name] = [{"period_name": period.period_name, "period_end_time": period.period_end_time.strftime("%H:%M"), "period_starting_time": period.period_starting_time.strftime("%H:%M"), "teacher_id": period.teacher_id, "subject_id": period.subject_id, "class_id": period.running_class.id}]
            
    return return_data

@app.route(DataApi('/get_today_teacher_time_table'))
@login_required
def get_today_teacher_time_table():
    teacher_id = request.args.get("teacher_id")
    current_day = datetime.now().date().strftime("%A")
    current_day = 'Thursday'
    running_periods = TimeTable.query.filter(TimeTable.day == current_day, TimeTable.teacher_id==teacher_id).all()
    return_data = {}
    for period in running_periods:
        clas_id = period.class_id
        if clas_id == None or clas_id == "":
            class_name = ""
        else:
            class_name = period.running_class.class_name()
        
        subject_id = period.subject_id
        if subject_id == None or subject_id == "":
            subject_name = ""
        else:
            subject_name = period.subject.subject_name
        
        
        append_data = {"class": class_name, "subject": subject_name, "period_name": period.period_name, "period_starting_time": period.period_starting_time.strftime("%I:%M %p"), "period_end_time": period.period_end_time.strftime("%I:%M %p")}
        try:
            return_data[period.period_name].append(append_data)
        except:
            return_data[period.period_name] = [append_data]

    return return_data

@app.route(DataApi('/get_last_admision_number'))
@login_required
def get_last_admision_number():
    students_counts = StudentDetail.query.count()
    last_student = db.get_or_404(StudentDetail, students_counts)
    admision_number = last_student.admision_number
    
    return_data = {"total_student": admision_number}

    return return_data

@app.route(DataApi('/get_section'))
@login_required
def get_section_api():
    class_id = request.args.get('class_id')
    
    return_data = []
    selected_class = db.get_or_404(Standared, class_id)

    sections = selected_class.sections
    for section in sections:
        return_data.append({"id": section.id, "section_name": section.section_name})
    
    return return_data

@app.route(DataApi('/get_all_clases'))
@login_required
def get_all_clases_api():
    all_clases = Standared.query.all()
    return_data = [{"id": "", "class_name": "Choose Class"}]
    for clas in all_clases:
        return_data.append({"id": clas.id, "class_name": clas.class_name})
    
    if current_user.user_type == 'admin':
        return_data.append({"id": "teachers", "class_name": "Teacher"})
    
    return return_data

@app.route(DataApi('/get_all_sections'))
@login_required
def get_all_sections_api():
    all_sections = Section.query.all()
    return_data = []
    for section in all_sections:
        return_data.append({"id": section.id, "section_name": section.section_name})
    
    return return_data

@app.route(DataApi('/get_subjects'))
@login_required
def get_subjects_api():
    subjects = Subject.query.all()
    return_data = []
    for subject in subjects:
        return_data.append({"id": subject.id, "subject_name": subject.subject_name})
    
    return return_data

@app.route(DataApi('/all_students'))
@login_required
def all_student_api():

    admision_number = request.args.get('admision_number')
    # student_type = request.args.get('student_type') # Regular, New Admision, Pass Out Students

    father_name = request.args.get('father_name')
    mother_name = request.args.get('mother_name')

    session_counts = SessionYear.query.count()
    running_session = db.get_or_404(SessionYear, session_counts)
    
    admision_number = request.args.get('admision_number')
    if admision_number == None:
        admision_number = ""

    min_id = request.args.get('min_id')
    if min_id == None:
        min_id = 1
    else:
        min_id = int(min_id)

    
    class_id = request.args.get('class_id')
    if class_id == None:
        class_id = ""
    
    section_id = request.args.get('section_id')
    if section_id == None:
        section_id = ""
    
    name = request.args.get("name")
    if name == None:
        name = ""
    
    father_name = request.args.get('father_name')
    if father_name == None:
        father_name = ""

    mother_name = request.args.get('mother_name')
    if mother_name == None:
        mother_name = ""
    

    aadhar_number = request.args.get('aadhar_number')
    if aadhar_number == None:
        aadhar_number = ""


    if class_id == "" and section_id == "":
        if admision_number != "":
            students = StudentDetail.query.filter(StudentDetail.admision_number > min_id, StudentDetail.admision_number==admision_number).all()

        else:
            students = StudentDetail.query.filter(StudentDetail.name.like(f'%{name}%'), StudentDetail.father_name.like(f"%{father_name}%"), StudentDetail.mother_name.like(f"%{mother_name}%")).all()
            

    else:

        
        if admision_number != "":
            students = StudentDetail.query.filter(StudentDetail.admision_number==admision_number).all()
            

        elif class_id != "" and section_id != "":
            
            running_class = RunningClass.query.filter_by(class_id=class_id, section_id=section_id, session_id=running_session.id).first()
            if running_class == None:
                students = []
            else:
                students = StudentDetail.query.filter(StudentDetail.classes.any(id=running_class.id), StudentDetail.name.like(f'%{name}%'), StudentDetail.father_name.like(f"%{father_name}%"), StudentDetail.mother_name.like(f"%{mother_name}%")).all()
            
        else:
            if class_id != "" and section_id == "":
                
                running_clases = RunningClass.query.filter_by(session_id = running_session.id, class_id = class_id).all()

            elif class_id == "" and section_id != "":
                
                running_clases = RunningClass.query.filter_by(session_id=running_session.id,section_id = section_id).all()
                
            
            students = []
            for class_obj  in running_clases:
                
                for student in class_obj.students:
                    if (name.lower() in str(student.name).lower() and father_name.lower() in student.father_name.lower() and mother_name.lower() in student.mother_name.lower() and aadhar_number.lower() in str(student.aadhar_number) and admision_number in str(student.admision_number)):
                        students.append(student)
                    else:
                        break
    



    return_data = []
    n = 0
    for student in students:
        if student.admision_number > min_id:
            data = {
                "id": student.id,
                "name": student.name,
                "father_name": student.father_name,
                "mother_name": student.mother_name,
                "admision_number": student.admision_number,
                "class": student.class_in_year(running_session.session_year),
                "action_link": url_for('student_detail', student_id=student.id )
                
                }
            return_data.append(data)

    return return_data

@app.route(DataApi('/get_students'))
@login_required
def get_all_students():
    class_id = request.args.get("class_id")
    section_id = request.args.get("section_id")
    session_counts = SessionYear.query.count()
    running_session = db.get_or_404(SessionYear, session_counts)
    running_clases = RunningClass.query.filter_by(class_id=class_id, section_id=section_id, session_id=running_session.id).first()
    students = running_clases.students
    return_data = []

    for student in students:
        return_data.append({"roll_number": student.roll_no(running_clases.running_class_unique_id), "name": student.name, "father_name": student.father_name, "id": student.id})
    
    return return_data

@app.route(DataApi('/get_teachers'))
@login_required
def get_active_teacher():
    all_teachers = Staff.query.filter(Staff.staff_active_status == True).all()
    return_data = []
    for teacher in all_teachers:
        append_data = {"roll_no": teacher.id, "name": teacher.name, "father_name": teacher.father_name, "id": teacher.id, "designation": teacher.designation}
        return_data.append(append_data)
    
    return return_data


@app.route(DataApi('/get_remaining_staff_list'))
@login_required
def get_remaining_staff_list():
    return_data = []

    min_id = request.args.get('min_id')

    name = request.args.get('name')
    if name == None:
        name = ""

    phone_number = request.args.get("phone_number")
    if phone_number == None:
        phone_number = ""
    aadhar_number = request.args.get('pan_number')
    if aadhar_number == None:
        aadhar_number = ""
    designation = request.args.get('designation')
    if designation == None:
        designation = ""
    pan_number = request.args.get('pan_number')
    if pan_number == None:
        pan_number = ""
    current_staff = request.args.get('current_staff') # Current Staff / Old Staff
    if current_staff == None:
        current_staff = "Current Staff"

    
    if current_staff == "Current Staff":
        staff_active_status = True
    else:
        staff_active_status = False
    
    staff_teaching_status = request.args.get('staff_type') # Teaching staff / Non-Teaching Staff
    if staff_teaching_status == None:
        staff_teaching_status = ""
        all_staff = Staff.query.filter(Staff.id > min_id, Staff.name.contains(name), Staff.designation.contains(designation), Staff.staff_active_status == staff_active_status, Staff.phone_number.contains(phone_number), Staff.aadhar_number.contains(aadhar_number), Staff.pan_number.contains(pan_number)).limit(10).all()

    else:
        if staff_teaching_status == 'true':
            staff_teaching_status = True
        else:
            staff_teaching_status = False

        all_staff = Staff.query.filter(Staff.id > min_id, Staff.name.contains(name), Staff.designation.contains(designation), Staff.staff_active_status == staff_active_status, Staff.phone_number.contains(phone_number), Staff.aadhar_number.contains(aadhar_number), Staff.pan_number.contains(pan_number), Staff.staff_teaching_status == staff_teaching_status).limit(10).all()

    for staff in all_staff:
        append_data = {"staff_id": staff.id, "name": staff.name, "father_name": staff.father_name, "designation": staff.designation, "action_url": url_for('staff_detail', staff_id=staff.id) }
        return_data.append(append_data)
    
    return return_data


@app.route(DataApi('/get_attendence'))
@login_required
def get_attendence():
    return_data = []
    attendence_date = request.args.get('attendence_date')
    if attendence_date == None:
        attendence_date = datetime.now().date()
    else:
        attendence_date = datetime.strptime(attendence_date, "%Y-%m-%d").date()

    request_for = request.args.get('request_for')

    if request_for == 'Teachers':
        all_attendence = StaffAttendence.query.filter(StaffAttendence.attendence_date == attendence_date).all()
        for attendence in all_attendence:
            append_data = {"roll_no": attendence.staff_id,"id": attendence.staff.id,"attendence_date": str(attendence.attendence_date.strftime("%d-%b-%Y")), "attendence_day": str(attendence.attendence_day), "present_status": attendence.present_status, "name": str(attendence.staff.name), "father_name": str(attendence.staff.father_name), "designation": str(attendence.staff.designation)}
            return_data.append(append_data)
        
    elif request_for == 'SingleStaff':
        staff_id = request.args.get('staff_id')
        
        all_attendence = StaffAttendence.query.filter(extract("month", StaffAttendence.attendence_date) == attendence_date.month, extract("year", StaffAttendence.attendence_date) == attendence_date.year, StaffAttendence.staff_id==staff_id).all()
        for attendence in all_attendence:
            append_data = {"attendence_date": attendence.attendence_date.strftime("%d-%b-%Y"), "attendence_day": attendence.attendence_day, "present_status": attendence.present_status, "name": attendence.staff.name, "designation": attendence.staff.designation}
            return_data.append(append_data)

    elif request_for == 'SingleClass':
        
        class_id = request.args.get('class_id')
        section_id = request.args.get('section_id')
        attendence_date = request.args.get('attendence_date')
        if attendence_date == None or attendence_date == "":
            attendence_date = datetime.now().date()
        else:
            attendence_date = datetime.strptime(attendence_date, "%Y-%m-%d").date()

        session_year = attendence_date.year
        session_year = SessionYear.query.filter(SessionYear.session_year == session_year).first()
        session_id = session_year.id
        unique_id = f"{session_id}-{class_id}-{section_id}"
        running_class = RunningClass.query.filter(RunningClass.running_class_unique_id == unique_id).first()

        all_attendence = StudentAttendence.query.filter(StudentAttendence.attendence_date == attendence_date, StudentAttendence.class_id == running_class.id).all()

        for attendence in all_attendence:
            try:
                append_data = {"id": attendence.student.id, "attendence_date": attendence.attendence_date.strftime("%d-%b-%Y"), "attendence_day": attendence.attendence_day, "present_status": attendence.present_status, "name": attendence.student.name, "father_name": attendence.student.father_name,"gender": attendence.student.gender, "roll_number": attendence.student.roll_no(attendence.running_class.running_class_unique_id), "class_name": attendence.running_class.class_name()}
                return_data.append(append_data)
            except :
                pass

    elif request_for == 'SingleStudent':
        student_id = request.args.get('student_id')
        all_attendence = StudentAttendence.query.filter(extract("month", StudentAttendence.attendence_date) == attendence_date.month, extract("year", StudentAttendence.attendence_date) == attendence_date.year, StudentAttendence.student_id == student_id).all()
        
        for attendence in all_attendence:
            append_data = {'attendence_date': attendence.attendence_date.strftime("%d-%b-%Y"), "attendence_day": attendence.attendence_day, "present_status": attendence.present_status, "name": attendence.student.name, "father_name": attendence.student.father_name, "roll_numbe": attendence.student.roll_no(attendence.running_class.running_class_unique_id), "class_name": attendence.running_class.class_name()}
            return_data.append(append_data)
    
    elif request_for == 'AllClasses':
        session_year = attendence_date.year
        running_session = SessionYear.query.filter(SessionYear.session_year == session_year).first()
        all_classes = running_session.main_classes

        for clas in all_classes:
            class_id = clas.id
            class_present_students = StudentAttendence.query.filter(StudentAttendence.attendence_date == attendence_date, StudentAttendence.present_status == 'Present', StudentAttendence.class_id == class_id).count()
            class_absent_students = StudentAttendence.query.filter(StudentAttendence.attendence_date == attendence_date, StudentAttendence.present_status == 'Absent', StudentAttendence.class_id == class_id).count()
            class_leave_students = StudentAttendence.query.filter(StudentAttendence.attendence_date == attendence_date, StudentAttendence.present_status == 'Leave', StudentAttendence.class_id == class_id).count()
            append_data = {"attendence_date": attendence_date.strftime("%d-%b-%Y"), "attendence_day": attendence_date.strftime("%A"), "present_count": class_present_students, "absent_count": class_absent_students, "leave_counts": class_leave_students, "class_name": clas.class_name(), "class_id":clas.id}
            return_data.append(append_data)


    return return_data

@app.route(DataApi('/get_monthly_attendence'))
@login_required
def get_monthly_attendence():
    return_data = []
    attendence_date = request.args.get('attendence_date')
    request_for = request.args.get('request_for')

    if attendence_date == None:
        attendence_date = datetime.now().date()
    else:
        attendence_date = datetime.strptime(attendence_date, "%Y-%m")
    
    if request_for == 'All_Staff':
        all_staff = Staff.query.filter(Staff.staff_active_status == True).all()
        for staff in all_staff:
            staff_present_count = StaffAttendence.query.filter(extract('month', StaffAttendence.attendence_date) == attendence_date.month, extract('year', StaffAttendence.attendence_date) == attendence_date.year, StaffAttendence.staff_id == staff.id, StaffAttendence.present_status == 'Present').count()
            staff_absent_count = StaffAttendence.query.filter(extract('month', StaffAttendence.attendence_date) == attendence_date.month, extract('year', StaffAttendence.attendence_date) == attendence_date.year, StaffAttendence.staff_id == staff.id, StaffAttendence.present_status == 'Absent').count()
            staff_leave_count = StaffAttendence.query.filter(extract('month', StaffAttendence.attendence_date) == attendence_date.month, extract('year', StaffAttendence.attendence_date) == attendence_date.year, StaffAttendence.staff_id == staff.id, StaffAttendence.present_status == 'Leave').count()
            append_data = {"name": staff.name, "designation": staff.designation, "present_count": staff_present_count, "absent_count": staff_absent_count, "leave_count": staff_leave_count}
            return_data.append(append_data)

    elif request_for == 'AllClasses':
        session_year = attendence_date.year
        running_session = SessionYear.query.filter(SessionYear.session_year == session_year).first()
        all_classes = running_session.main_classes

        for clas in all_classes:
            class_id = clas.id
            class_present_students = StudentAttendence.query.filter(extract('month', StudentAttendence.attendence_date) == attendence_date.month, extract('year', StudentAttendence.attendence_date) == attendence_date.year, StudentAttendence.present_status == 'Present', StudentAttendence.class_id == class_id).count()
            class_absent_students = StudentAttendence.query.filter(extract('month', StudentAttendence.attendence_date) == attendence_date.month, extract('year', StudentAttendence.attendence_date) == attendence_date.year, StudentAttendence.present_status == 'Absent', StudentAttendence.class_id == class_id).count()
            class_leave_students = StudentAttendence.query.filter(extract('month', StudentAttendence.attendence_date) == attendence_date.month, extract('year', StudentAttendence.attendence_date) == attendence_date.year, StudentAttendence.present_status == 'Leave', StudentAttendence.class_id == class_id).count()
            append_data = {"attendence_date": attendence_date.strftime("%d-%b-%Y"), "attendence_day": attendence_date.strftime("%A"), "present_count": class_present_students, "absent_count": class_absent_students, "leave_counts": class_leave_students, "class_name": clas.class_name()}
            return_data.append(append_data)


    return return_data


@app.route(DataApi('/get_monthly_attendence_data'))
@login_required
def get_monthly_attendence_data():
    attendence_date = request.args.get('attendence_date')
    if attendence_date != None:
        current_date = datetime.strptime(attendence_date, "%Y-%m").date()
    else:
        current_date = datetime.now().date()
        
    student_present_count = StudentAttendence.query.filter(extract('month', StudentAttendence.attendence_date) == current_date.month, extract('year', StudentAttendence.attendence_date == current_date.year), StudentAttendence.present_status == 'Present').count()
    student_absent_count = StudentAttendence.query.filter(extract('month', StudentAttendence.attendence_date) == current_date.month, extract('year', StudentAttendence.attendence_date == current_date.year), StudentAttendence.present_status == 'Absent').count()
    student_leave_count = StudentAttendence.query.filter(extract('month', StudentAttendence.attendence_date) == current_date.month, extract('year', StudentAttendence.attendence_date == current_date.year), StudentAttendence.present_status == 'Leave').count()

    staff_present_count = StaffAttendence.query.filter(extract('month', StaffAttendence.attendence_date) == current_date.month, extract('year', StaffAttendence.attendence_date == current_date.year), StaffAttendence.present_status == 'Present').count()
    staff_absent_count = StaffAttendence.query.filter(extract('month', StaffAttendence.attendence_date) == current_date.month, extract('year', StaffAttendence.attendence_date == current_date.year), StaffAttendence.present_status == 'Absent').count()
    staff_leave_count = StaffAttendence.query.filter(extract('month', StaffAttendence.attendence_date) == current_date.month, extract('year', StaffAttendence.attendence_date == current_date.year), StaffAttendence.present_status == 'Leave').count()
    
    return_data = {"student_attendence_data": {"present": student_present_count, "absent": student_absent_count, "leave": student_leave_count},
                   "staff_attendence_data": {"present": staff_present_count, "absent": staff_absent_count, 'leave': staff_leave_count}}
    
    return return_data

@app.route(DataApi('/get_students_documents'))
@login_required
def get_students_documents():
    return_data = []
    student_id = request.args.get('student_id')
    student = db.get_or_404(StudentDetail, student_id)
    documents = student.documents
    for document in documents:
        append_data = {"document_name": document.document_name, "uploaded_date": document.uploaded_date.strftime("%d-%b-%Y"), "download_url": f"{url_for('get_individual_document')}?request_for=Student&document_id={document.id}", "delete_url": f"{url_for('delete_individual_document')}?request_for=Student&document_id={document.id}"}
        return_data.append(append_data)
    return return_data

@app.route(DataApi('/get_staff_documents'))
@login_required
def get_staff_documents():
    return_data = []
    staff_id = request.args.get('staff_id')
    staff = db.get_or_404(Staff, staff_id)
    documents = staff.documents
    for document in documents:
        append_data = {"document_name": document.document_name, "uploaded_date": document.uploaded_date.strftime("%d-%b-%Y"), "download_url": f"{url_for('get_individual_document')}?request_for=Staff&document_id={document.id}", "delete_url": f"{url_for('delete_individual_document')}?request_for=Staff&document_id={document.id}"}
        return_data.append(append_data)
    return return_data

@app.route(DataApi('/get_subject_in_class'))
@login_required
def get_subject_in_class():
    class_id = request.args.get('class_id')
    return_data = []
    running_class = db.get_or_404(RunningClass, class_id)
    subjects = running_class.subjects

    for subject in subjects:
        teachers = subject.class_teachers(class_id)
        
        append_data = {"subject_name": subject.subject_name, "teachers": teachers}
        return_data.append(append_data)
    
    return return_data

@app.route(DataApi('/get_all_subjects_classes'))
@login_required
def get_all_subjects_classes():
    session_counts = SessionYear.query.count()
    running_session = db.get_or_404(SessionYear, session_counts)

    return_data = []

    all_clases = running_session.main_classes
    for clas in all_clases:
        subjects = []
        for subject in clas.subjects:
            subject_data = {"subject_id": subject.id, "subject_name": subject.subject_name}
            subjects.append(subject_data)
        append_data = {"class_id": clas.id, "class_name": clas.class_name(), "subjects": subjects}
        
        return_data.append(append_data)

    return return_data

@app.route(DataApi('/get_all_subjects_for_class'))
@login_required
def get_all_subjects_for_class():
    running_class_id = request.args.get('running_class_id')
    if running_class_id == None:
        class_id = request.args.get("class_id")
        section_id = request.args.get("section_id")
        session_counts = SessionYear.query.count()
        running_session = db.get_or_404(SessionYear, session_counts)
        running_clases = RunningClass.query.filter_by(class_id=class_id, section_id=section_id, session_id=running_session.id).first()
    else:
        running_clases = db.get_or_404(RunningClass, running_class_id)

    subjects = running_clases.subjects
    return_data = []

    for subject in subjects:
        return_data.append({"subject_name": subject.subject_name})

    return return_data

@app.route(DataApi('/get_all_notice'))
@login_required
def get_all_notice():
    all_notice = Notice.query.order_by(Notice.notice_time.desc()).all()

    return_data = []
    for notice in all_notice:
        # time_gap = datetime.now() - notice.notice_time 
        # time_gap = int(time_gap.total_seconds() / 60)
        notice_time = notice.notice_time.strftime("%I:%M %p")
        append_data = {"notice_date": notice.notice_time.strftime("%d-%b-%Y"), "notice": notice.notice, "assigned_by": notice.user.name, "time": notice_time, "delete_url": url_for('delete_notice', notice_id=notice.id)}
        return_data.append(append_data)
    
    return return_data


@app.route(DataApi('/get_all_running_classes'))
@login_required
def get_all_running_classes():
    session_counts = SessionYear.query.count()
    running_session = db.get_or_404(SessionYear, session_counts)

    return_data = []

    all_clases = running_session.main_classes
    for clas in all_clases:
        return_data.append(clas.class_name())

    return return_data


################################################## DASHBOARD API ######################################################

######### Dynamic Data (This data come again and again)
@app.route(DataApi('/get_todays_attendence_data'))
@login_required
def get_todays_attendence_data():
    attendence_date = request.args.get('attendence_date')
    if attendence_date != None:
        current_date = datetime.strptime(attendence_date, "%Y-%m-%d").date()
    else:
        current_date = datetime.now().date()
    student_present_count = StudentAttendence.query.filter(StudentAttendence.attendence_date == current_date, StudentAttendence.present_status == 'Present').count()
    student_absent_count = StudentAttendence.query.filter(StudentAttendence.attendence_date == current_date, StudentAttendence.present_status == 'Absent').count()
    student_leave_count = StudentAttendence.query.filter(StudentAttendence.attendence_date == current_date, StudentAttendence.present_status == 'Leave').count()

    staff_present_count = StaffAttendence.query.filter(StaffAttendence.attendence_date == current_date, StaffAttendence.present_status == 'Present').count()
    staff_absent_count = StaffAttendence.query.filter(StaffAttendence.attendence_date == current_date, StaffAttendence.present_status == 'Absent').count()
    staff_leave_count = StaffAttendence.query.filter(StaffAttendence.attendence_date == current_date, StaffAttendence.present_status == 'Leave').count()
    
    return_data = {"student_attendence_data": {"present": student_present_count, "absent": student_absent_count, "leave": student_leave_count},
                   "staff_attendence_data": {"present": staff_present_count, "absent": staff_absent_count, 'leave': staff_leave_count}}
    
    return return_data




############################################################################################################################################################
######################################################## LOG-IN / LOG-OUT ##################################################################################
############################################################################################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']

        user = User.query.filter_by(login_id=login_id).first()

        if user == None:
            flash("This Login Id Doesn't exist")
            return redirect(url_for('login'))
        
        else:
            print('else condition...')
            if user.password == password:
                user.login_status = True
                user.last_login = datetime.now()
                db.session.commit()
                login_user(user=user)
                return redirect(url_for("dashboard"))
            else:
                flash('Password Is Not Match with Your Login Id')
                return redirect(url_for('login'))
            
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    current_user.login_status = False
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))


            


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
