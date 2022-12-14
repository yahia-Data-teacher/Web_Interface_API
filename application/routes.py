from application import app
# import sqlalchemy as sqa
from application.models import engine, session
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpenses, url
# from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import json


# engine = sqa.create_engine(
#     'postgresql://bccgxmfz:JAsuLsAgJqQYpLUyBCRQXM7ZsmJTGdWn@babar.db.elephantsql.com/bccgxmfz', echo=True)
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()
# session.rollback()

@app.route('/')
def index():
    entries = session.query(IncomeExpenses).order_by(
        IncomeExpenses.date.desc()).all()
    return render_template('index.html', title='index', entries=entries)


@app.route('/add', methods=["GET", "POST"])
def add_expense():
    form = UserInputForm()
    if form.validate_on_submit():

        entry = IncomeExpenses(type=form.type.data, amount=form.amount.data,
                               category=form.category.data)
        try:
            session.add(entry)
            session.commit()
            flash("Sucessful entry", "success")
        except:
            session.rollback()
            flash("Error", "danger")

        return redirect(url_for('index'))
    return render_template("add.html", title='add', form=form)


@app.route('/delete/<int:entry_id>')
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
        session.rollback()
        flash("Error", "danger")
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    session.rollback()
    income_vs_expense  = session.query(func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(
        IncomeExpenses.type).order_by(IncomeExpenses.type).all()
    
    category_comparison  = session.query(func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(
        IncomeExpenses.category).order_by(IncomeExpenses.category).all()
    
    dates = session.query(func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(
        IncomeExpenses.date).order_by(IncomeExpenses.date).all()
    
    income_category = []
    labels=[]
    for amount, label in category_comparison :
        income_category.append(amount)
        labels.append(label)
    
    income_expense = []
    for total_amount, _ in income_vs_expense :
        income_expense.append(total_amount)
    
    over_time_expenditure = []
    dates_labels=[]
    for amount, date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime("%m-%d-%y"))
        
     
    
    return render_template("dashboard.html", title='dashboard',
                           income_vs_expense  = json.dumps(income_expense),
                           income_category=json.dumps(income_category),
                           income_category_labels=json.dumps(labels),
                           over_time_expenditure = json.dumps(over_time_expenditure),
                           dates_labels = json.dumps(dates_labels),
                           
                           )
