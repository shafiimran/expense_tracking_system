from backend import db_helper
import os
import sys
#  C:\Users\shafi\OneDrive\Desktop\Codebasics\python\projects\expense_tracking_system adding this into system path so test_db_helper can find every files
print(__file__)# so that this file can find backend -> db_helper module directory

def test_fetch_expenses_for_date_for_sep_20():
    data=db_helper.fetch_expenses_for_date('2024-09-20')
    assert len(data)==1
    assert data[0]['amount']==350
    assert data[0]['notes'] == 'Burger'
    assert data[0]['category']=='Fast Food'


def test_fetch_expenses_for_date_invalid_date():
    data = db_helper.fetch_expenses_for_date('2030-01-20')
    assert len(data) == 0

def test_fetch_expense_summary_for_date_invalid_date():
    data = db_helper.fetch_expense_summary('2030-01-20','2030-02-50')
    assert len(data) == 0

