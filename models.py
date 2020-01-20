from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://twewxikheafkcm:0a85002e32d391f3878c7a30f7c2f1545825c06fa5ec1a7c7e86b6f942df5e76" \
                                        "@ec2-107-21-97-5.compute-1.amazonaws.com:5432/d2v3n5k0dhe10"
app.config['SECRET_KEY'] = "kursovahorodniukserhii"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'orm_user'

    user_email = db.Column(db.String(45), nullable=False)
    user_username = db.Column(db.String(45), primary_key=True)
    user_password = db.Column(db.String(64), nullable=False)
    is_owner = db.Column(db.Boolean, default=False)

    company_id = db.Column(db.Integer, db.ForeignKey('orm_company.id'))


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


db.create_all()
