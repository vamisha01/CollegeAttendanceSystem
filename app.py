from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Student, Subject, AttendanceLog

@app.route('/')
def index():
    students = Student.query.all()
    subjects = Subject.query.all()
    return render_template('index.html', students=students, subjects=subjects)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_no = request.form['roll_no']
    class_name = request.form['class_name']
    student = Student(name=name, roll_no=roll_no, class_name=class_name)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_subject', methods=['POST'])
def add_subject():
    name = request.form['name']
    subject = Subject(name=name)
    db.session.add(subject)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    status = request.form['status']
    attendance = AttendanceLog(student_id=student_id, subject_id=subject_id, date=datetime.date.today(), status=status)
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
