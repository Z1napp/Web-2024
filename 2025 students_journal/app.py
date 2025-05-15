from flask import (
    Flask, render_template, redirect, url_for, request, flash,
    make_response
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required, logout_user,
    UserMixin, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from io import StringIO
import csv

# ------------------------------
# Ініціалізація Flask-додатку
# ------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ------------------------------
# Моделі бази даних
# ------------------------------

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')


class Grade(db.Model):
    __tablename__ = 'grade'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)


# ------------------------------
# Логін-менеджер
# ------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------------------
# Маршрути: Головна сторінка
# ------------------------------

@app.route('/')
def home():
    return redirect(url_for('dashboard'))


# ------------------------------
# Маршрут: Dashboard (для різних ролей)
# ------------------------------

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Загальні дані
    subjects_all = [
        "Математика", "Фізика", "Історія", "Біологія", "Хімія", "Географія",
        "Література"
    ]

    if current_user.role == 'student':
        return dashboard_student(subjects_all)

    elif current_user.role == 'teacher':
        return dashboard_teacher(subjects_all)

    elif current_user.role == 'admin':
        return dashboard_admin()

    return redirect(url_for('logout'))

def dashboard_admin():
    users = User.query.all()
    return render_template(
        'dashboard_admin.html',
        name=current_user.login,
        role=current_user.role,
        users=users
    )

def dashboard_student(subjects_all):
    # Унікальні предмети студента
    subjects = db.session.query(Grade.subject).filter_by(student_id=current_user.id).distinct().all()
    subjects = [s[0] for s in subjects]

    selected_subject = request.args.get('subject')

    if request.method == 'POST':
        selected_subject = request.form['subject']
        return redirect(url_for('dashboard', subject=selected_subject))

    grades_data = []
    if selected_subject:
        grades_query = (
            db.session.query(Grade, User.login.label('teacher_login'))
            .join(User, Grade.teacher_id == User.id)
            .filter(Grade.student_id == current_user.id, Grade.subject == selected_subject)
            .all()
        )

        for grade, teacher_login in grades_query:
            grades_data.append({
                'grade': grade.grade,
                'date': grade.date,
                'teacher_login': teacher_login
            })

    average_grade = round(sum(g['grade'] for g in grades_data) / len(grades_data), 2) if grades_data else None

    return render_template(
        'dashboard_student.html',
        name=current_user.login,
        role=current_user.role,
        subjects=subjects,
        selected_subject=selected_subject,
        grades_for_subject=grades_data,
        average_grade=average_grade
    )


def dashboard_teacher(subjects_all):
    selected_subject = request.args.get('subject') or request.form.get('subject')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    students = User.query.filter_by(role='student').all()

    # Додавання оцінки
    if request.method == 'POST' and 'add_grade' in request.form:
        grade = int(request.form['grade'])
        student_id = int(request.form['student_id'])
        new_grade = Grade(
            subject=selected_subject,
            grade=grade,
            student_id=student_id,
            teacher_id=current_user.id,
            date=datetime.utcnow()
        )
        db.session.add(new_grade)
        db.session.commit()
        return redirect(url_for('dashboard', subject=selected_subject, start_date=start_date_str, end_date=end_date_str))

    students_grades = {}
    average_per_student = {}

    if selected_subject:
        for student in students:
            query = Grade.query.filter_by(student_id=student.id, subject=selected_subject)
            if start_date:
                query = query.filter(Grade.date >= start_date)
            if end_date:
                query = query.filter(Grade.date <= end_date)
            grades = query.all()

            if grades:
                students_grades[student.login] = grades
                average = round(sum([g.grade for g in grades]) / len(grades), 2)
                average_per_student[student.login] = average

    return render_template('dashboard_teacher.html',
                           name=current_user.login,
                           role=current_user.role,
                           students=students,
                           subjects=subjects_all,
                           selected_subject=selected_subject,
                           students_grades=students_grades,
                           average_per_student=average_per_student,
                           start_date=start_date_str,
                           end_date=end_date_str)


# ------------------------------
# Маршрути: Управління оцінками
# ------------------------------

@app.route('/add_grade', methods=['POST'])
@login_required
def add_grade():
    subject = request.form['subject']
    grade_value = request.form['grade']
    student_id = request.form['student_id']

    new_grade = Grade(
        subject=subject,
        grade=int(grade_value),
        student_id=int(student_id),
        teacher_id=current_user.id
    )
    db.session.add(new_grade)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/edit_grade/<int:grade_id>', methods=['POST'])
@login_required
def edit_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    if current_user.role != 'teacher':
        flash('Доступ заборонено.', 'error')
        return redirect(url_for('dashboard'))

    new_grade_value = request.form.get('grade')
    if not new_grade_value or not new_grade_value.isdigit() or not (1 <= int(new_grade_value) <= 100):
        flash('Оцінка має бути числом від 1 до 100.', 'error')
        return redirect(url_for('dashboard'))

    grade.grade = int(new_grade_value)
    db.session.commit()
    flash('Оцінку оновлено', 'success')
    return redirect(url_for('dashboard', subject=grade.subject))


@app.route('/delete_grade/<int:grade_id>', methods=['POST'])
@login_required
def delete_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    if current_user.role != 'teacher':
        flash('Доступ заборонено.', 'error')
        return redirect(url_for('dashboard'))

    subject = grade.subject
    db.session.delete(grade)
    db.session.commit()
    flash('Оцінку видалено', 'success')
    return redirect(url_for('dashboard', subject=subject))


# ------------------------------
# Маршрут: Експорт оцінок CSV
# ------------------------------

@app.route('/export_grades')
@login_required
def export_grades():
    subject = request.args.get('subject')
    start_date_raw = request.args.get('start_date')
    end_date_raw = request.args.get('end_date')

    start_date = None if not start_date_raw or start_date_raw == "None" else datetime.strptime(start_date_raw, "%Y-%m-%d")
    end_date = None if not end_date_raw or end_date_raw == "None" else datetime.strptime(end_date_raw, "%Y-%m-%d")

    query = Grade.query
    if subject:
        query = query.filter_by(subject=subject)
    if start_date:
        query = query.filter(Grade.date >= start_date)
    if end_date:
        query = query.filter(Grade.date <= end_date)

    grades = query.all()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Subject', 'Grade', 'Student', 'Teacher', 'Date'])

    for g in grades:
        student = User.query.get(g.student_id)
        teacher = User.query.get(g.teacher_id)
        cw.writerow([
            g.id,
            g.subject,
            g.grade,
            student.login if student else 'Unknown',
            teacher.login if teacher else 'Unknown',
            g.date.strftime('%Y-%m-%d')
        ])

    output = si.getvalue()
    si.close()

    response = make_response(output)
    response.headers["Content-Disposition"] = "attachment; filename=grades.csv"
    response.headers["Content-type"] = "text/csv"
    return response


# ------------------------------
# Маршрут: Менеджмент користувачів
# ------------------------------

@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    if current_user.role == 'admin':
        login = request.form['login']
        password = request.form['password']
        role = request.form['role']

        new_user = User(login=login, password=generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Студент доданий успішно!')
    return redirect(url_for('dashboard'))

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        abort(403)

    login_val = request.form['login']
    password = request.form['password']
    role = request.form['role']

    if User.query.filter_by(login=login_val).first():
        flash('Користувач з таким логіном вже існує.')
        return redirect(url_for('dashboard'))

    new_user = User(
        login=login_val,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    flash('Користувача додано успішно!')
    return redirect(url_for('dashboard'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        abort(403)
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Ви не можете видалити свій власний акаунт.', 'error')
        return redirect(url_for('dashboard'))

    # Видаляємо всі оцінки, пов’язані з цим користувачем
    Grade.query.filter((Grade.student_id == user.id) | (Grade.teacher_id == user.id)).delete()

    db.session.delete(user)
    db.session.commit()
    flash('Користувача видалено успішно.', 'success')
    return redirect(url_for('dashboard'))

# ------------------------------
# Маршрути: Авторизація, Реєстрація, Вихід
# ------------------------------

@app.route('/auth')
def auth():
    mode = request.args.get('mode', 'login')
    return render_template('auth.html', mode=mode)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        password_input = request.form['password']
        user = User.query.filter_by(login=login_input).first()

        if user and check_password_hash(user.password, password_input):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Неправильний логін або пароль')
        return redirect(url_for('auth'))

    return render_template('auth.html')


@app.route('/register', methods=['POST'])
def register():
    login_name = request.form['login']
    password = request.form['password']
    role = request.form.get('role', 'student')

    if User.query.filter_by(login=login_name).first():
        flash('Користувач з таким логіном вже існує.')
        return redirect(url_for('auth'))

    new_user = User(login=login_name, password=generate_password_hash(password), role=role)
    db.session.add(new_user)
    db.session.commit()

    flash('Реєстрація успішна! Увійдіть в акаунт.')
    return redirect(url_for('auth'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))


# ------------------------------
# Створення таблиць БД (при запуску)
# ------------------------------

with app.app_context():
    db.create_all()


# ------------------------------
# Запуск додатку
# ------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
