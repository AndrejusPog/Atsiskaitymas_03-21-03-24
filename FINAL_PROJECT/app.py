import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user
from flask_sqlalchemy import SQLAlchemy


import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'myBills.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Falses


bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "Login"
login_manager.login_message_category = "Information"


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column("Description", db.String)
    amount = db.Column("Amount", db.String)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    grouprelation = db.relationship("Group")


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    paskaitos = db.relationship("Bill")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        encrypted_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data,
                    password=encrypted_pass)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('groups'))
        else:
            flash('Please check your email and password')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/groups", methods=["GET", "POST"])
def groups():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    forma = forms.GetGroupForm()
    if forma.validate_on_submit():
       test = forma.id.data
       print(test)
       return redirect (url_for('edit_bill', id=forma.data['id']))
    try:
        groups = Group.query.all()
    except:
        groups = []
    return render_template("groups.html", groups=groups, form=forma)


@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    db.create_all()
    forma = forms.GroupForm()
    if forma.validate_on_submit():
        add_group = Group(name=forma.name.data)
        db.session.add(add_group)
        db.session.commit()
        return redirect(url_for('groups'))
    return render_template("add_group.html", form=forma)


@app.route("/delete_group/<int:id>")
def delete_group(id):
    request = Group.query.get(id)
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('groups'))


@app.route("/edit_group/<int:id>", methods=['GET', 'POST'])
def edit_group(id):
    forma = forms.GroupForm()
    grouprelation = Group.query.get(id)
    if forma.validate_on_submit():
        grouprelation.name = forma.name.data
        db.session.commit()
        return redirect(url_for('groups'))
    return render_template("edit_group.html", form=forma, grouprelation=grouprelation)


@app.route("/bills")
def bills():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    try:
        bills = Bill.query.all()
    except:
        bills = []
    return render_template("bills.html", bills=bills)


@app.route("/add_bill", methods=["GET", "POST"])
def add_bill():
    db.create_all()
    forma = forms.BillForm()
    if forma.validate_on_submit():
        new_bill = Bill(description=forma.description.data, amount=forma.amount.data, group_id=forma.group.data.id)
        db.session.add(new_bill)
        db.session.commit()
        return redirect(url_for('bills'))
    return render_template("add_bill.html", form=forma)


@app.route("/delete_bill/<int:id>")
def delete_bill(id):
    request = Bill.query.get(id)
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('bills'))


@app.route("/edit_bill/<int:id>", methods=['GET', 'POST'])
def edit_bill(id):
    forma = forms.BillForm()
    myBill = Bill.query.get(id)
    if forma.validate_on_submit():
        myBill.description = forma.description.data
        myBill.amount = forma.amount.data
        myBill.group_id = forma.group.data.id
        db.session.commit()
        return redirect(url_for('bills'))
    return render_template("edit_bill.html", form=forma, myBill=myBill)





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()
