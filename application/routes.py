from application import app
# import sqlalchemy as sqa
from application.models import engine, SESSION
from flask_login import login_required, current_user
from flask import *
from . import app
from application.form import UserInputForm
from application.models import IncomeExpenses, url
# from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import json

from werkzeug.security import check_password_hash

from application.models import User

from flask_login import login_user, logout_user, current_user

from flask_login import login_required


# engine = sqa.create_engine(
#     'postgresql://bccgxmfz:JAsuLsAgJqQYpLUyBCRQXM7ZsmJTGdWn@babar.db.elephantsql.com/bccgxmfz', echo=True)
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()
# session.rollback()

@app.route('/')
@login_required
def index():
    entries = SESSION.query(IncomeExpenses).order_by(
        IncomeExpenses.date.desc()).all()
    return render_template('index.html', title='index', entries=entries)


@app.route('/add', methods=["GET", "POST"])
@login_required
def add_expense():
    form = UserInputForm()
    if form.validate_on_submit():

        entry = IncomeExpenses(type=form.type.data, amount=form.amount.data,
                               category=form.category.data)
        try:
            SESSION.add(entry)
            SESSION.commit()
            flash("Sucessful entry", "success")
        except:
            SESSION.rollback()
            flash("Error", "danger")

        return redirect(url_for('index'))
    return render_template("add.html", title='add', form=form)


@app.route('/delete/<int:entry_id>')
@login_required
def delete(entry_id):
    # connection = psycopg2.connect(url)
    # cursor = connection.cursor()
    # query=
    # cursor.execute("DELETE FROM IncomeExpenses WHERE id = {0}".format(entry_id))
    # entry=session.query(IncomeExpenses).get(entry_id)
    try:
        engine.execute("DELETE FROM api_sold WHERE id = {}".format(entry_id))
        flash("Deleting was success", "success")
    except:
        SESSION.rollback()
        flash("Error", "danger")
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    SESSION.rollback()
    income_vs_expense = SESSION.query(func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(
        IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    category_comparison = SESSION.query(func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(
        IncomeExpenses.category).order_by(IncomeExpenses.category).all()

    dates = SESSION.query(func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(
        IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_category = []
    labels = []
    for amount, label in category_comparison:
        income_category.append(amount)
        labels.append(label)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_labels = []
    for amount, date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime("%m-%d-%y"))

    return render_template("dashboard.html", title='dashboard',
                           income_vs_expense=json.dumps(income_expense),
                           income_category=json.dumps(income_category),
                           income_category_labels=json.dumps(labels),
                           over_time_expenditure=json.dumps(over_time_expenditure),
                           dates_labels=json.dumps(dates_labels),
                           )


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    SESSION.rollback()
    # user = User.query.filter_by(email=email).first()
    user = SESSION.query(User).filter(User.email == email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not (user.password == password):  # check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
