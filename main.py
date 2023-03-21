import eel
from datetime import *
import sqlite3 as sq
import os

db_path = os.path.dirname(os.path.abspath("family_budget.db"))
"""DATABASE"""
with sq.connect(db_path + "/family_budget.db") as db:
    cur = db.cursor()  # Cursor

    # budget table
    cur.execute("""CREATE TABLE IF NOT EXISTS budget(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           month_spent REAL DEFAULT 0 NOT NULL, 
           month_rest REAL DEFAULT 0 NOT NULL, 
           month_profit REAL DEFAULT 0 NOT NULL,
           month_debt REAL DEFAULT 0 NOT NULL,
           selected_month_profit REAL DEFAULT 0 NOT NULL,
           selected_month_cost REAL DEFAULT 0 NOT NULL,
           selected_month_debts REAL DEFAULT 0 NOT NULL,
           data_inc TEXT DEFAULT 0 NOT NULL,
           data_exp TEXT DEFAULT 0 NOT NULL,
           data_debt TEXT DEFAULT 0 NOT NULL,

           year_spent REAL DEFAULT 0 NOT NULL, 
           year_profit REAL DEFAULT 0 NOT NULL
           

       )""")

    # incomes table
    cur.execute("""CREATE TABLE IF NOT EXISTS incomes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_incomes TEXT DEFAULT 'Salary',
        profit_amount REAL DEFAULT 0,
        date TEXT NOT NULL

    )""")

    # expenses table
    cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_expenses TEXT DEFAULT 'Other',
        spent_amount REAL DEFAULT 0,
        date TEXT NOT NULL

    ) """)

    # debts table
    cur.execute("""CREATE TABLE IF NOT EXISTS debts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        moneylenders_name TEXT DEFAULT '',
        debt_amount REAL DEFAULT 0,
        date TEXT NOT NULL

        ) """)

    if cur.execute("SELECT Count() FROM budget").fetchone()[0] <= 0:
        cur.execute("INSERT INTO budget (month_spent, month_rest, month_profit,"
                    " year_spent, year_profit) VALUES (?, ?, ?, ?, ?)", (0, 0, 0, 0, 0))

"""MAIN LOGIC"""
eel.init('web')


# auxiliary functions


# Shorten the date
def shorten_the_date_list(date_to_shorten):
    if len(str(date_to_shorten)) > 10:
        date_to_shorten = str(date_to_shorten).split(' ')
        shorted_date = date_to_shorten[0].split('-')
    else:
        shorted_date = date_to_shorten.split('-')
    return shorted_date


# Get incomes from db
def get_incomes_from_db():
    l_entry_list = []

    l_entry = cur.execute("SELECT * FROM incomes WHERE id=?", [l_id_inc()]).fetchall()
    for value1 in l_entry:
        for value2 in value1:
            l_entry_list.append(value2)
    month_db = l_entry_list[3]
    shorten_the_date_list(month_db)

    inc = l_entry_list[2]
    return inc


# last id inc
def l_id_inc():
    m_id = cur.execute("SELECT max(id) FROM incomes")
    l_id = m_id.fetchone()[0]
    return l_id


# last id exp
def l_id_exp():
    m_id = cur.execute("SELECT max(id) FROM expenses")
    l_id = m_id.fetchone()[0]
    return l_id


# last id debts
def l_id_debts():
    m_id = cur.execute("SELECT max(id) FROM debts")
    l_id = m_id.fetchone()[0]
    return l_id


# now date
now = datetime.now()
current_date = shorten_the_date_list(now)


# Checking whether the month matches the current one
def does_the_month_matches(date):
    s_now = current_date
    s_date = shorten_the_date_list(date)
    return s_now[0] == s_date[0] and s_now[1] == s_date[1]


def does_the_year_matches(date):
    s_now = current_date
    s_date = shorten_the_date_list(date)
    return s_now[0] == s_date[0]


# JavaScript functions
# incomes logic. tag, profit, date
@eel.expose
def incomes_py(tag_inc_js, amg_js, date_js_inc):
    tag = tag_inc_js
    amount = round(float(amg_js), 2)
    date = str(date_js_inc)

    # add values to database
    cur.execute("INSERT INTO incomes (tag_incomes, profit_amount, date) VALUES (?, ?, ?)", (tag, amount, date))
    db.commit()
    # month
    if does_the_month_matches(date) is True:
        amount = cur.execute("SELECT profit_amount FROM incomes WHERE id=?", [l_id_inc()]).fetchone()[0]
        cur.execute("UPDATE budget SET month_profit = month_profit + (?)", [amount])
        db.commit()

    # year
    if does_the_year_matches(date) is True:
        cur.execute("UPDATE budget SET year_profit = year_profit + (?)", [amount])
        db.commit()

    return tag, amount, date


# expenses logic. tag, profit, date
@eel.expose
def expenses_py(tag_exp_js, ams_js, date_js_exp):
    tag = tag_exp_js
    amount = round(float(ams_js), 2)
    date = str(date_js_exp)

    # add values to database
    cur.execute("INSERT INTO expenses (tag_expenses, spent_amount, date) VALUES(?,?, ?)", (tag, amount, date))
    db.commit()

    # month
    if does_the_month_matches(date) is True:
        amount = cur.execute("SELECT spent_amount FROM expenses WHERE id=?", [l_id_exp()]).fetchone()[0]
        cur.execute("UPDATE budget SET month_spent = month_spent + (?)", [amount])
        db.commit()

    # year
    if does_the_year_matches(date) is True:
        cur.execute("UPDATE budget SET year_spent = year_spent + (?)", [amount])
        db.commit()

    return tag, amount, date


# debts logic. tag, profit, date
@eel.expose
def debts_py(moneylenders_name_js, amount_of_debt_js, date_js_debt):
    name = moneylenders_name_js
    amount = round(float(amount_of_debt_js), 2)
    date = str(date_js_debt)

    # add values to database
    cur.execute("INSERT INTO debts (moneylenders_name, debt_amount, date) VALUES(?,?, ?)", (name, amount, date))
    db.commit()

    # month
    if does_the_month_matches(date) is True:
        amount = cur.execute("SELECT debt_amount FROM debts WHERE id=?", [l_id_debts()]).fetchone()[0]
        cur.execute("UPDATE budget SET month_debt = month_debt + (?)", [amount])
        db.commit()

    return name, amount, date


@eel.expose
def show_monthly_data_py():
    month_profit = cur.execute("SELECT month_profit FROM budget").fetchone()[0]
    month_expenses = cur.execute("SELECT month_spent FROM budget").fetchone()[0]
    month_debt = cur.execute("SELECT month_debt FROM budget").fetchone()[0]
    month_rest = round(float(month_profit - month_expenses), 2)
    return month_profit, month_expenses, month_rest, month_debt


# get and show selected month data
@eel.expose
def get_and_show_selected_month_data_py(selected_month_js, selected_year_js, where):
    month_expenses_id = []
    selected_exp_id = []
    month_expenses = []

    month_incomes_id = []
    selected_inc_id = []
    month_incomes = []

    month_debts_id = []
    selected_debt_id = []
    month_debts = []

    s_dates = []
    split_date = []

    unique_selected_inc_id = []
    unique_selected_exp_id = []
    unique_selected_debt_id = []

    total_month_incomes = 0
    total_month_expenses = 0
    total_month_debts = 0

    tags = []
    values = []
    moneylenders_name, debt_amount = [], []
    data = ''

    i = 0
    if where == "inc":
        # get all dates from incomes
        dates = cur.execute("SELECT date FROM incomes").fetchall()

        for value in dates:
            for value1 in value:
                s_dates.append(value1)

        while i < len(s_dates):
            if i <= len(s_dates):
                split_date.append(shorten_the_date_list(s_dates[i]))
            # checking for a date match
            if (shorten_the_date_list(s_dates[i])[1] == str(selected_month_js)) and \
                    (shorten_the_date_list(s_dates[i])[0] == str(selected_year_js)):

                is_m_and_y_match = True

            else:
                is_m_and_y_match = False

            # get month expenses from db
            if is_m_and_y_match is True:
                month_incomes_id.append(cur.execute("SELECT id FROM incomes WHERE date=?", [s_dates[i]]).fetchall())
                for value in month_incomes_id:
                    for value1 in value:
                        for value2 in value1:
                            selected_inc_id.append(value2)

                unique_selected_inc_id = list(set(selected_inc_id))

            else:
                cur.execute("UPDATE budget SET selected_month_profit = (?)", [0])
                db.commit()
            i += 1
        i = 0
        while i < len(unique_selected_inc_id):
            month_incomes.append(cur.execute("SELECT tag_incomes, profit_amount FROM incomes WHERE id=?",
                                             [unique_selected_inc_id[i]]).fetchall())
            i += 1
        for value in month_incomes:
            for value1 in value:
                tags.append((value1[0]))
                values.append(value1[1])
                total_month_incomes += value1[1]
                cur.execute("UPDATE budget SET selected_month_profit = (?)", [total_month_incomes])
                db.commit()

        i = 0
        while i < len(tags):
            data += (tags[i] + ' ' + str(values[i]) + '; ')
            i += 1

        # send data to db
        cur.execute("UPDATE budget SET data_inc = (?)", [data])
        db.commit()

    elif where == 'exp':
        # get all dates from expenses
        dates = cur.execute("SELECT date FROM expenses").fetchall()

        for value in dates:
            for value1 in value:
                s_dates.append(value1)

        while i < len(s_dates):
            if i <= len(s_dates):
                split_date.append(shorten_the_date_list(s_dates[i]))

            # checking for a date match
            if (shorten_the_date_list(s_dates[i])[1] == str(selected_month_js)) and \
                    (shorten_the_date_list(s_dates[i])[0] == str(selected_year_js)):

                is_m_and_y_match = True

            else:
                is_m_and_y_match = False

            # get month expenses from db
            if is_m_and_y_match is True:
                month_expenses_id.append(cur.execute("SELECT id FROM expenses WHERE date=?", [s_dates[i]]).fetchall())
                for value in month_expenses_id:
                    for value1 in value:
                        for value2 in value1:
                            selected_exp_id.append(value2)
                unique_selected_exp_id = list(set(selected_exp_id))
            else:
                cur.execute("UPDATE budget SET selected_month_cost = (?)", [0])
                db.commit()
            i += 1

        i = 0
        while i < len(unique_selected_exp_id):
            month_expenses.append(cur.execute("SELECT tag_expenses, spent_amount FROM expenses WHERE id=?",
                                              [unique_selected_exp_id[i]]).fetchall())
            i += 1
        for value in month_expenses:
            for value1 in value:
                tags.append((value1[0]))
                values.append(value1[1])
                total_month_expenses += value1[1]
                cur.execute("UPDATE budget SET selected_month_cost = (?)", [total_month_expenses])
                db.commit()

        i = 0
        while i < len(tags):
            data += (tags[i] + ' ' + str(values[i]) + '; ')
            i += 1

        # send data to db
        cur.execute("UPDATE budget SET data_exp = (?)", [data])
        db.commit()

    elif where == 'debt':
        # get all dates from debts
        dates = cur.execute("SELECT date FROM debts").fetchall()

        for value in dates:
            for value1 in value:
                s_dates.append(value1)
        while i < len(s_dates):
            if i <= len(s_dates):
                split_date.append(shorten_the_date_list(s_dates[i]))

            # checking for a date match
            if (shorten_the_date_list(s_dates[i])[1] == str(selected_month_js)) and \
                    (shorten_the_date_list(s_dates[i])[0] == str(selected_year_js)):

                is_m_and_y_match = True

            else:
                is_m_and_y_match = False

            # get month debts from db
            if is_m_and_y_match is True:
                month_debts_id.append(cur.execute("SELECT id FROM debts WHERE date=?", [s_dates[i]]).fetchall())
                for value in month_debts_id:
                    for value1 in value:
                        for value2 in value1:
                            selected_debt_id.append(value2)
                unique_selected_debt_id = list(set(selected_debt_id))
            else:
                cur.execute("UPDATE budget SET selected_month_debts = (?)", [0])
                db.commit()
            i += 1

        i = 0
        while i < len(unique_selected_debt_id):
            month_debts.append(cur.execute("SELECT moneylenders_name, debt_amount FROM debts WHERE id=?",
                                           [unique_selected_debt_id[i]]).fetchall())
            i += 1
        for value in month_debts:
            for value1 in value:
                moneylenders_name.append((value1[0]))
                debt_amount.append(value1[1])
                total_month_debts += value1[1]
                cur.execute("UPDATE budget SET selected_month_debts = (?)", [total_month_debts])
                db.commit()

        i = 0
        while i < len(moneylenders_name):
            data += (moneylenders_name[i] + '|' + str(debt_amount[i]) + ';')
            i += 1

        # send data to db
        cur.execute("UPDATE budget SET data_debt = (?)", [data])
        db.commit()

    else:
        print('ERROR')


# show incomes for selected month
@eel.expose
def show_selected_month_incomes_py():
    profit = cur.execute("SELECT selected_month_profit FROM budget").fetchone()[0]
    data = cur.execute("SELECT data_inc FROM budget").fetchone()[0]
    return profit, data


# show expenses for selected month
@eel.expose
def show_selected_month_expenses_py():
    cost = cur.execute("SELECT selected_month_cost FROM budget").fetchone()[0]
    data = cur.execute("SELECT data_exp FROM budget").fetchone()[0]
    return cost, data


# show debts for selected month
@eel.expose
def show_selected_month_debts_py():
    debt = cur.execute("SELECT selected_month_debts FROM budget").fetchone()[0]
    data = cur.execute("SELECT data_debt FROM budget").fetchone()[0]
    return debt, data


eel.start('index.html', size=(750, 900))
