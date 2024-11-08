import pandas as pd
from app import app, StudentDetail, RunningClass, Standared, Section, SessionYear, db, Staff, Subject
from datetime import datetime



# session_year = SessionYear.query.filter_by(session_year='2024').first()
# print(session_year)

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
        print(class_name)
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
        



with app.app_context():
    write_staff('C:\\Users\\gurus\\OneDrive\\Desktop\\staff_excel_sheet.xlsx')
#     write_students()