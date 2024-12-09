#CRUD (Create, Read, Update, Delete)
from logging_setup import setup_logger
import mysql.connector
from contextlib import contextmanager
from jupyter_server.auth import passwd

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='expense_manager'
    )

    cursor=connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute('SELECT * FROM expenses')
        expenses=cursor.fetchall()
        for expense in expenses:
            print(expense)

def fetch_expenses_for_date(expense_date):
    logger.info(f'fetch_expenses_for_date called with {expense_date}')
    with get_db_cursor() as cursor:
        cursor.execute('SELECT * FROM expenses WHERE expense_date= %s', (expense_date,))
        expenses=cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f'insert_expense called with date:{expense_date}, amount:{amount},category:{category}, notes:{notes}')
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            'INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)', (expense_date, amount, category, notes)
        )

def delete_expense_for_date(expense_date):
    logger.info(f'delete_expenses_for_date called with {expense_date}')
    with get_db_cursor(commit=True) as cursor:#if commit=True not used, changes wont be updated
        cursor.execute('DELETE FROM expenses WHERE expense_date= %s', (expense_date,))

def fetch_expense_summary(start_date,end_date): #for analytics purpose
    logger.info(f'fetch_expense_summary called with start date:{start_date}, end date:{end_date}')
    with get_db_cursor() as cursor:
        cursor.execute(
                    ''' SELECT category, SUM(amount) AS total FROM expenses
                        WHERE expense_date BETWEEN %s AND %s
                        GROUP BY category;''',
                        (start_date,end_date)
                       )
        data=cursor.fetchall()
        return data


def fetch_expense_summary_by_month(): #for analytics purpose
    logger.info(f'fetch_expense_summary_by_month called ')
    with get_db_cursor() as cursor:
        cursor.execute(
                    ''' SELECT MONTH(expense_date) AS month, SUM(amount) AS total FROM expenses
                        GROUP BY month;
                        ''')
        data=cursor.fetchall()
        return data



if __name__=='__main__':
    # insert_expense('2024-09-21','1500','Fast Food','Steak')
    items=fetch_expense_summary_by_month()
    for item in items:
        print(item)


