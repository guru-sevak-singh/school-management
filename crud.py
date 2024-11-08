# from app import app, db, Exam, User, Notice, SessionYear,TimeTable, StudentDetail, Standared,Document, Section, RunningClass, standared_section, session_classes, Subject, Comment, Staff, extract, StaffDocument, StudentAttendence, StaffAttendence
from datetime import datetime
from app import *
import shutil

# with app.app_context():
#     # student = db.get_or_404(StudentDetail, 1)
#     # db.session.delete(student)
#     # db.session.commit()
#     # student_attendence = StudentAttendence.query.filter(StudentAttendence.student_id == None).all()
#     # for student in student_attendence:
#     #     db.session.delete(student)
    
#     # db.session.commit()
#     pass

# g = Upload_Folder
# print(g)
# path = os.path.join(g, 'students', 'student_2')
# print(path)


# # os.rmdir(path)
# try:
#     shutil.rmtree(path)
# except:
#     pass


with app.app_context():
    user = User.query.all()
    print(user)
