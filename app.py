import os
import pdoc
import uuid
import codecs

from hashlib import sha256
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin

from forms import UploadForm, SignUpForm, LogInForm, ChangeForm, FilterForm, CompanyForm, ProjectForm

ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://twewxikheafkcm:0a85002e32d391f3878c7a30f7c2f1545825c06fa5ec1a7c7e86b6f942df5e76" \
                                        "@ec2-107-21-97-5.compute-1.amazonaws.com:5432/d2v3n5k0dhe10"
app.config['SECRET_KEY'] = "kursovahorodniukserhii"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'kpistudydb@gmail.com'
app.config['MAIL_PASSWORD'] = 'kpistudy129087'

db = SQLAlchemy(app)
Bootstrap(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):

    __tablename__ = 'orm_user'

    user_email = db.Column(db.String(45), nullable=False)
    user_username = db.Column(db.String(45), primary_key=True)
    user_password = db.Column(db.String(64), nullable=False)
    is_owner = db.Column(db.Boolean, default=False)

    company_id = db.Column(db.Integer, db.ForeignKey('orm_company.id'))

    def get_id(self):
        return self.user_username


class File(db.Model):

    __tablename__ = 'orm_file'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(45), nullable=False)
    upload_time = db.Column(db.String(100), nullable=False)
    documentation = db.Column(db.String(45))

    user_username = db.Column(db.String(45), db.ForeignKey('orm_user.user_username'))
    project_id = db.Column(db.Integer, db.ForeignKey('orm_project.id'))


class Company(db.Model):

    __tablename__ = 'orm_company'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False, unique=True)
    website = db.Column(db.String(100))
    secret_key = db.Column(db.String(100))

    projects = db.relationship('Project')
    users = db.relationship('User')


class Project(db.Model):

    __tablename__ = 'orm_project'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))

    company_id = db.Column(db.Integer, db.ForeignKey('orm_company.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauth():
    return redirect('/login')


@app.route('/', methods=['GET'])
@login_required
def home():
    return redirect('/documentation')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = sha256(str(form.password.data).encode('utf-8')).hexdigest()
            user = User.query.filter_by(user_email=email).first()
            if user:
                current_password = user.user_password
                if current_password != password:
                    return render_template('error.html', message='Password is wrong!', user=None)
                login_user(user)
                return redirect('/')
            else:
                return render_template('error.html', message='User does not exist!', user=None, form=form)
        return render_template('error.html', message='Something is wrong', user=None)
    return render_template('login.html', message=' ', user=None, form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    choice = [(company.id, company.company_name) for company in Company.query.all()]
    form = SignUpForm()
    form.companies.choices = choice
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            password = sha256(str(form.password.data).encode('utf-8')).hexdigest()
            confirm_password = sha256(str(form.confirm_password.data).encode('utf-8')).hexdigest()
            company = Company.query.filter_by(id=form.companies.data).first()
            company_secret_key = company.secret_key
            secret_key = form.secret_key.data
            if password != confirm_password:
                return render_template('error.html', message='Password does not confirmed!', user=None)
            if secret_key != company_secret_key:
                return render_template('error.html', message='Secret key does not valid!', user=None)
            try:
                user = User()
                user.user_password = password
                user.user_email = email
                user.user_username = username
                user.company_id = company.id
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                return render_template('error.html', message=f'Sorry, but {e}', user=None)
            else:
                try:
                    msg = Message(f"Hello, {username}!", sender="kpistudydb@gmail.com", recipients=[email])
                    mail.send(msg)
                except Exception as e:
                    print(e)
                return redirect(url_for('login'))
    return render_template('signup.html', user=None, form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/documentation', methods=['GET', 'POST'])
@login_required
def documentation():
    choice = [(project.id, project.project_name)
              for project in Project.query.filter_by(company_id=current_user.company_id)]
    form = UploadForm()
    form.projects.choices = choice
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.file.data.filename
            project_id = form.projects.data
            if not allowed_file(name):
                return render_template('error.html', message='Is this file python script?')
            form.file.data.save(os.path.join(os.path.abspath(''), 'review.py'))
            libpath = os.path.abspath('templates')
            project = Project.query.filter_by(id=project_id).first()
            try:
                mod = pdoc.import_module('review')
                doc = pdoc.Module(mod)
                html = doc.html()
            except Exception as e:
                print(e)
                return render_template('error.html',
                                       user=current_user.user_username,
                                       message='Something wrong in your module!')
            else:
                now = datetime.now()
                filename = str(uuid.uuid4())
                with open(os.path.join(libpath, f"{filename}.html"), "w") as f:
                    f.write(html)
                file = File(user_username=current_user.user_username,
                            project_id=project.id,
                            file_name=name,
                            upload_time=str(now),
                            documentation=filename)
                db.session.add(file)
                db.session.commit()
                return html
        return render_template('error.html', message='Not valid form!', user=current_user.user_username)
    return render_template('documentation.html', user=current_user.user_username, form=form)


@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    form = FilterForm()
    if request.method == 'POST':
        if form.filter.data == '':
            return redirect('/history')
        if form.validate_on_submit():
            filter_name = str(form.filter.data)
            result = list()
            projects = Project.query.filter_by(company_id=current_user.company_id).all()
            for project in projects:
                q = list()
                files = File.query.filter_by(
                    project_id=project.id,
                    file_name=filter_name
                ).all()
                if files:
                    for file in files:
                        p = list()
                        p.append(file.file_name)
                        p.append(file.upload_time)
                        p.append(file.documentation)
                        p.append(file.user_username)
                        q.append(p)
                    result.append({"name": project.project_name, "value": q})
        else:
            result = []
    else:
        result = list()
        projects = Project.query.filter_by(company_id=current_user.company_id).all()
        for project in projects:
            q = list()
            files = File.query.filter_by(
                user_username=current_user.user_username,
                project_id=project.id
            ).all()
            if files:
                for file in files:
                    p = list()
                    p.append(file.file_name)
                    p.append(file.upload_time)
                    p.append(file.documentation)
                    p.append(file.user_username)
                    q.append(p)
                result.append({"name": project.project_name, "value": q})
    return render_template('history.html', items=result, user=current_user.user_username, form=form)


@app.route('/get_doc_by_filename', methods=['POST', 'GET'])
@login_required
def get_doc_by_filename():
    if request.method == 'POST':
        filename = request.form['filename_by_get']
        path = os.path.abspath('templates')
        f = codecs.open((os.path.join(path, f'{filename}.html')), 'r')
        html = f.read()
        return html
    return redirect('/documentation')


@app.route('/send_mail_by_filename', methods=['POST', 'GET'])
@login_required
def send_mail_by_filename():
    if request.method == 'POST':
        filename = request.form['filename_by_send']
        path = os.path.abspath('templates')
        try:
            f = codecs.open((os.path.join(path, f'{filename}.html')), 'r')
            html = f.read()
        except Exception as e:
            print(e)
            return render_template('error.html', user=current_user.user_username, message='File does not exist!')
        else:
            try:
                msg = Message(f"Your documentation", sender="kpistudydb@gmail.com",
                              recipients=[current_user.user_email])
                msg.html = html
                mail.send(msg)
            except Exception as e:
                print(e)
                return render_template('error.html', message='Document was not sent, sorry!',
                                       user=current_user.user_username)
            else:
                return redirect(url_for('history'))
    return redirect('/documentation')


@app.route('/delete_documentation', methods=['POST'])
@login_required
def delete_documentation():
    if request.method == 'POST':
        filename = request.form['filename_by_delete']
        project_name = request.form['project_name']
        project = Project.query.filter_by(company_id=current_user.company_id, project_name=project_name).first()
        file = File.query.filter_by(documentation=filename, project_id=project.id).first()
        db.session.delete(file)
        db.session.commit()
        return redirect('/history')
    return redirect('/documentation')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            old_password = sha256(str(form.old_password.data).encode('utf-8')).hexdigest()
            new_password = sha256(str(form.new_password.data).encode('utf-8')).hexdigest()
            confirm_password = sha256(str(form.confirm_password.data).encode('utf-8')).hexdigest()
            if confirm_password != new_password:
                return render_template('error.html', message='Password was not confirmed!',
                                       user=current_user.user_username)
            if old_password != current_user.user_password:
                return render_template('error.html', message='Old password is wrong!')
            try:
                current_user.user_password = new_password
                db.session.add(current_user)
                db.session.commit()
            except Exception:
                return render_template('error.html', message='Oops. Something is wrong!',
                                       user=current_user.user_username)
            return redirect(url_for('login'))
        return render_template('error.html', message='Form is not valid', user=current_user.user_username)
    return render_template('change.html', user=current_user.user_username, form=form)


@app.route('/create_company', methods=['POST', 'GET'])
def create_company():
    form = CompanyForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        website = form.website.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            return render_template('error.html', message='Password does not confirmed!', user=None)
        secret_key = form.secret_key.data
        company = Company()
        company.company_name = name
        company.website = website if website else ''
        company.secret_key = secret_key
        db.session.add(company)
        db.session.commit()
        db.session.refresh(company)
        user = User()
        user.user_password = sha256(str(password).encode('utf-8')).hexdigest()
        user.user_email = email
        user.user_username = username
        user.company_id = company.id
        db.session.add(user)
        db.session.commit()
        return redirect('/create_project')
    return render_template('company.html', form=form, user=None)


@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        list_of_names = [project.project_name
                         for project in Project.query.filter_by(company_id=current_user.company_id).all()]
        if name not in list_of_names:
            description = form.description.data
            project = Project()
            project.project_name = name
            project.description = description
            project.company_id = current_user.company_id
            db.session.add(project)
            db.session.commit()
            return render_template('error.html', message='Okay! Lets make some documentation!')
        else:
            return render_template('error.html', message='Project with current name exist in your company.')
    return render_template('project.html', user=current_user.user_username, form=form)


@app.route('/<path:path>')
def anywhere(path):
    return render_template('404.html', user=None)


if __name__ == '__main__':
    app.run(debug=True)
