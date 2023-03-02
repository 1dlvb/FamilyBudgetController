import eel
from datetime import *
import sqlite3 as sq
from array import array
import unicodedata
import os

db_path = os.path.dirname(os.path.abspath("family_budget.db"))
print(db_path + "/family_budget.db")
"""DATABASE"""
with sq.connect(db_path + "/family_budget.db") as db:
    cur = db.cursor()  # Cursor

    # budget table
    cur.execute("""CREATE TABLE IF NOT EXISTS budget(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           month_spent REAL DEFAULT 0 NOT NULL, 
           month_rest REAL DEFAULT 0 NOT NULL, 
           month_profit REAL DEFAULT 0 NOT NULL,
           selected_month_profit REAL DEFAULT 0 NOT NULL,
           selected_month_cost REAL DEFAULT 0 NOT NULL,
           data_inc TEXT DEFAULT 0 NOT NULL,
           data_exp TEXT DEFAULT 0 NOT NULL,

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
def get_num_of_rows_inc():                            # Get number of incomes table rows
    rows_query_inc = "SELECT Count() FROM incomes"
    cur.execute(rows_query_inc)
    number_of_rows_inc = cur.fetchone()[0]
    # print(number_of_rows_inc)
    return number_of_rows_inc


def get_num_of_rows_exp():                            # Get number of expenses table rows
    rows_query_exp = "SELECT Count() FROM expenses"
    cur.execute(rows_query_exp)
    number_of_rows_exp = cur.fetchone()[0]
    # print(number_of_rows_exp)
    return number_of_rows_exp


def get_num_of_rows_exp():                            # Get number of expenses table rows
    rows_query_debt = "SELECT Count() FROM expenses"
    cur.execute(rows_query_debt)
    number_of_rows_debt = cur.fetchone()[0]
    # print(number_of_rows_debt)
    return number_of_rows_debt


def get_num_of_rows_budget():                            # Get number of budget table rows
    rows_query_budget = "SELECT Count() FROM budget"
    cur.execute(rows_query_budget)
    number_of_rows_budget = cur.fetchone()[0]
    # print(number_of_rows_budget)
    return number_of_rows_budget


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
        # print(l_entry_list)
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
shorten_the_date_list(now)


# Checking whether the month matches the current one
def does_the_match_month(date, current_date):
    s_now = shorten_the_date_list(current_date)
    s_date = shorten_the_date_list(date)

    if (s_now[0] != s_date[0]) or ((s_now[0] >= s_date[0]) and (s_now[1] < s_date[1])):
        match_or_not = False
    else:
        match_or_not = True
    return match_or_not


def does_the_match_year(date, current_date):
    s_now = shorten_the_date_list(current_date)
    s_date = shorten_the_date_list(date)

    if s_now[0] != s_date[0]:
        match_or_not = False
    else:
        match_or_not = True
    return match_or_not


# JavaScript functions
# incomes logic. tag, profit, date
@eel.expose
def incomes_py(tag_inc_js, amg_js, date_js_inc):
    tag = tag_inc_js
    amount = round(float(amg_js), 2)
    date = str(date_js_inc)
    num_of_rows = get_num_of_rows_inc()

    # add values to database
    cur.execute("INSERT INTO incomes (tag_incomes, profit_amount, date) VALUES (?, ?, ?)", (tag, amount, date))
    db.commit()

    # month
    if (num_of_rows > 0) and (does_the_match_month(date, now) is True):
        amount = cur.execute("SELECT profit_amount FROM incomes WHERE id=?", [l_id_inc()]).fetchone()[0]
        # print("AMOUNT IS: {0}".format(amount))
        cur.execute("UPDATE budget SET month_profit = month_profit + (?)", [amount])
        db.commit()
    else:
        print("Incomes problem!")

    # year
    if (num_of_rows > 0) and (does_the_match_month(date, now) is True):
        cur.execute("UPDATE budget SET year_profit = year_profit + (?)", [amount])
        db.commit()

    show_month_rest_money_py()

    # print(tag, date, amount)
    return tag, amount, date


# expenses logic. tag, profit, date
@eel.expose
def expenses_py(tag_exp_js, ams_js, date_js_exp):
    tag = tag_exp_js
    amount = round(float(ams_js), 2)
    date = str(date_js_exp)
    num_of_rows = get_num_of_rows_exp()

    # add values to database
    cur.execute("INSERT INTO expenses (tag_expenses, spent_amount, date) VALUES(?,?, ?)", (tag, amount, date))
    db.commit()

    # month
    if (num_of_rows > 0) and (does_the_match_month(date, now) is True):
        amount = cur.execute("SELECT spent_amount FROM expenses WHERE id=?", [l_id_exp()]).fetchone()[0]
        # print("AMOUNT IS: {0}".format(amount))
        cur.execute("UPDATE budget SET month_spent = month_spent + (?)", [amount])
        db.commit()
    else:
        print("Expenses problem!")

    # year
    if (num_of_rows > 0) and (does_the_match_year(date, now) is True):
        cur.execute("UPDATE budget SET year_spent = year_spent + (?)", [amount])
        db.commit()

    show_month_rest_money_py()
    # print(tag, amount, date)
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
    show_month_rest_money_py()

    # print(name, amount, date)
    return name, amount, date


# Show month total profit
@eel.expose
def show_total_month_profit_py():
    # total month profit
    now = datetime.now()
    s_dates = []
    split_date = []
    selected_id = []
    unique_selected_id = []
    profit = 0
    s_profit = 0

    # print(now)

    dates = cur.execute("SELECT date FROM incomes").fetchall()
    for value in dates:
        for value1 in value:
            s_dates.append(value1)
    i = 0
    while i < len(s_dates):
        if i <= len(s_dates):
            split_date.append(shorten_the_date_list(s_dates[i]))

        # checking for a date match
        if shorten_the_date_list(s_dates[i])[1] == str(shorten_the_date_list(now)[1]) and \
                (shorten_the_date_list(s_dates[i])[0] == str(shorten_the_date_list(now)[0])):

            is_m_and_y_match = True

            # print(s_dates[i] + ' ' + str(is_m_and_y_match))

        else:
            is_m_and_y_match = False
            # print(s_dates[i] + ' ' + str(is_m_and_y_match))

        if is_m_and_y_match is True:
            id = cur.execute("SELECT id FROM incomes WHERE date = (?)", [s_dates[i]]).fetchall()
            for value in id:
                for value1 in value:
                    selected_id.append(value1)
            unique_selected_id = list(set(selected_id))
        else:
            s_profit = 0
        i += 1
    i = 0
    while i < len(unique_selected_id):
        profit = cur.execute("SELECT profit_amount FROM incomes WHERE id = (?)", [unique_selected_id[i]]).fetchall()
        for value in profit:
            for value1 in value:
                s_profit += value1

        i += 1
    # print("PROFIT IS {0}".format(s_profit))
    cur.execute("UPDATE budget SET month_profit = (?)", [s_profit])
    db.commit()
    return s_profit

# Show month expenses
@eel.expose
def show_total_month_expenses_py():
    # total month expenses
    now = datetime.now()
    s_dates = []
    split_date = []
    selected_id = []
    unique_selected_id = []
    cost = 0
    s_cost = 0

    # print(now)

    dates = cur.execute("SELECT date FROM expenses").fetchall()
    for value in dates:
        for value1 in value:
            s_dates.append(value1)
    i = 0
    while i < len(s_dates):
        if i <= len(s_dates):
            split_date.append(shorten_the_date_list(s_dates[i]))

        # checking for a date match
        if shorten_the_date_list(s_dates[i])[1] == str(shorten_the_date_list(now)[1]) and \
                (shorten_the_date_list(s_dates[i])[0] == str(shorten_the_date_list(now)[0])):

            is_m_and_y_match = True

            # print(s_dates[i] + ' ' + str(is_m_and_y_match))

        else:
            is_m_and_y_match = False
            # print(s_dates[i] + ' ' + str(is_m_and_y_match))

        if is_m_and_y_match is True:
            id = cur.execute("SELECT id FROM expenses WHERE date = (?)", [s_dates[i]]).fetchall()
            for value in id:
                for value1 in value:
                    selected_id.append(value1)
            unique_selected_id = list(set(selected_id))
        else:
            s_cost = 0
        i += 1
    i = 0
    while i < len(unique_selected_id):
        cost = cur.execute("SELECT spent_amount FROM expenses WHERE id = (?)", [unique_selected_id[i]]).fetchall()
        for value in cost:
            for value1 in value:
                s_cost += value1

        i += 1
    # print("COST IS {0}".format(s_cost))
    cur.execute("UPDATE budget SET month_spent = (?)", [s_cost])
    db.commit()
    return s_cost


# Show month rest of money
@eel.expose
def show_month_rest_money_py():
    # Get total month profit
    profit = cur.execute("SELECT month_profit FROM budget").fetchone()[0]

    # Get total month expenses
    amount_of_spent = cur.execute("SELECT month_spent FROM budget").fetchone()[0]

    # Add rest of money to DB
    res = round(float(profit - amount_of_spent), 2)
    cur.execute("UPDATE budget SET month_rest = (?)", (res, ))
    db.commit()
    # Get rest of money from DB
    rest = cur.execute("SELECT month_rest FROM budget").fetchone()[0]
    # # print(rest)
    return rest


# Get data from selected month and year
@eel.expose
def data_from_selected_m_y_py(selected_month_js, selected_year_js, where):
    i = 0
    s_dates = []
    split_date = []

    month_incomes = []
    month_incomes_id = []
    selected_inc_id = []
    unique_selected_inc_id = []

    month_expenses = []
    month_expenses_id = []
    selected_exp_id = []
    unique_selected_exp_id = []

    total_month_incomes = 0
    total_month_expenses = 0

    # print(selected_month_js, selected_year_js, where)
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

                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            else:
                is_m_and_y_match = False
                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            # HERE
            # get month incomes from db
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
        # print(unique_selected_inc_id)

        # get sum of nums
        i = 0
        while i < len(unique_selected_inc_id):
            month_incomes.append(
                cur.execute("SELECT profit_amount FROM incomes WHERE id=?", [unique_selected_inc_id[i]]).fetchall())
            i += 1
        for value in month_incomes:
            for value1 in value:
                for value2 in value1:
                    total_month_incomes += value2
                    # print(total_month_incomes)
                    cur.execute("UPDATE budget SET selected_month_profit = (?)", [total_month_incomes])
                    db.commit()
    else:

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

                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            else:
                is_m_and_y_match = False
                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            # HERE
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
        # print(unique_selected_exp_id)

        # get sum of nums
        i = 0
        while i < len(unique_selected_exp_id):
            month_expenses.append(cur.execute("SELECT spent_amount FROM expenses WHERE id=?",
                                              [unique_selected_exp_id[i]]).fetchall())
            i += 1
        for value in month_expenses:
            for value1 in value:
                for value2 in value1:
                    total_month_expenses += value2
                    # print(total_month_expenses)
                    cur.execute("UPDATE budget SET selected_month_cost = (?)", [total_month_expenses])
                    db.commit()


# get and show selected month data
@eel.expose
def get_and_show_selected_month_data_py(selected_month_js, selected_year_js, where):
    month_expenses_id = []
    selected_exp_id = []
    month_expenses = []

    month_incomes_id = []
    selected_inc_id = []
    month_incomes = []


    s_dates = []
    split_date = []

    unique_selected_inc_id = []
    unique_selected_exp_id = []

    total_month_incomes = 0
    total_month_expenses = 0

    tags = []
    values = []
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

                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            else:
                is_m_and_y_match = False
                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            # HERE
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

        # send data to to db
        cur.execute("UPDATE budget SET data_inc = (?)", [data])
        db.commit()

        # print("total month incomes = " + str(total_month_incomes))
        # print('data is {0}'.format(data))

    else:
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

                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            else:
                is_m_and_y_match = False
                # print(s_dates[i] + ' ' + str(is_m_and_y_match))

            # HERE
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

        # send data to to db
        cur.execute("UPDATE budget SET data_exp = (?)", [data])
        db.commit()

        # print("total month expenses = " + str(total_month_expenses))
        # print('data is {0}'.format(data))


# show incomes for selected month
@eel.expose
def show_selected_month_incomes_py():
    profit = cur.execute("SELECT selected_month_profit FROM budget").fetchone()[0]
    data = cur.execute("SELECT data_inc FROM budget").fetchone()[0]
    return profit, data


# show expenses for selected month
@eel.expose
def show_selected_month_data_py():
    cost = cur.execute("SELECT selected_month_cost FROM budget").fetchone()[0]
    data = cur.execute("SELECT data_exp FROM budget").fetchone()[0]
    return cost, data


eel.start('index.html', size=(750, 900))
