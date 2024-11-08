from app import app, db, Standared, Section, User, SessionYear
from datetime import datetime


def CreateFirstUser():
    user = User(name="guru sevak singh", login_id="guru@school.com", password="guru@2003", user_type='admin')
    db.session.add(user)
    db.session.commit()

def CreateAllClases():

    clas = Standared(class_name='VI')
    db.session.add(clas)
    db.session.commit()
    clas = Standared(class_name='VII')
    db.session.add(clas)
    db.session.commit()
    clas = Standared(class_name='VIII')
    db.session.add(clas)
    db.session.commit()
    clas = Standared(class_name='IX')
    db.session.add(clas)
    db.session.commit()
    clas = Standared(class_name='X')
    db.session.add(clas)
    db.session.commit()
    clas = Standared(class_name='XI')
    db.session.add(clas)
    db.session.commit()
    clas = Standared(class_name='XII')
    db.session.add(clas)
    db.session.commit()

def CreateAllSectioins():
    section = Section(section_name='A')
    db.session.add(section)
    db.session.commit()
    section = Section(section_name='Commerce')
    db.session.add(section)
    db.session.commit()
    section = Section(section_name='Arts')
    db.session.add(section)
    db.session.commit()

def CreateSession():
    session_year = datetime.now().year
    session_name = f"{session_year}-{session_year + 1}"
    session = SessionYear(session_year = f"{session_year}", session_name=session_name)
    db.session.add(session)
    db.session.commit()


with app.app_context():
    db.create_all()
    CreateFirstUser()
    CreateSession()
    # CreateAllClases()
    # CreateAllSectioins()

    