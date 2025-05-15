from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Модель користувача ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')


# --- Модель оцінок ---
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(2), nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student = db.relationship('User', foreign_keys=[student_id], backref='grades')

    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher = db.relationship('User', foreign_keys=[teacher_id])




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('dashboard'))




# --- Панель користувача ---
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    students = User.query.filter_by(role='student').all()
    subjects = [
        "Математика",
        "Фізика",
        "Історія",
        "Біологія",
        "Хімія",
        "Географія",
        "Література"
    ]

    # Для студента
    if current_user.role == 'student':
        subjects = db.session.query(Grade.subject).filter_by(student_id=current_user.id).distinct().all()
        subjects = [s[0] for s in subjects]

        if request.method == 'POST':
            selected_subject = request.form['subject']
            grades_for_subject = Grade.query.filter_by(
                student_id=current_user.id,
                subject=selected_subject
            ).all()

            # Підготовка структури students_grades
            students_grades = {current_user.login: [g.grade for g in grades_for_subject]}

            return render_template(
                'dashboard_student.html',
                subjects=subjects,
                grades_for_subject=grades_for_subject,
                students_grades=students_grades
            )

        return render_template('dashboard_student.html', subjects=subjects)

    # Для викладача
    elif current_user.role == 'teacher':


        return render_template('dashboard_teacher.html', name=current_user.login, role=current_user.role, students=students, subjects=subjects)

    # Для адміністратора
    elif current_user.role == 'admin':
        return render_template('dashboard_admin.html', name=current_user.login, role=current_user.role)

    return redirect(url_for('logout'))



# --- Додати оцінку ---
@app.route('/add_grade', methods=['POST'])
@login_required
def add_grade():
    subject = request.form['subject']
    grade_value = request.form['grade']
    student_id = request.form['student_id']

    new_grade = Grade(
        subject=subject,
        grade=grade_value,
        student_id=student_id,
        teacher_id=current_user.id
    )

    db.session.add(new_grade)
    db.session.commit()

    return redirect(url_for('dashboard'))


# --- Додати студента ---
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


# --- Сторінка авторизації ---
@app.route('/auth')
def auth():
    mode = request.args.get('mode', 'login')
    return render_template('auth.html', mode=mode)



# --- Обробка логіну ---
# --- Вхід (GET + POST) ---
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

    # GET-запит показує форму авторизації
    return render_template('auth.html')



# --- Обробка реєстрації ---
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


# --- Вихід ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))


# --- Створити БД ---
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
