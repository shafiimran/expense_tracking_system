from http.client import HTTPException
from fastapi import FastAPI
from datetime import date
import calendar
import db_helper
from typing import List
from pydantic import BaseModel

app=FastAPI()
# uvicorn server:app --reload
# fastapi dev .\main.py

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class  DateRange(BaseModel):
    start_date:date
    end_date:date

@app.get('/expenses/{expense_date}', response_model=List[Expense])
def get_expenses(expense_date:date):
    expenses=db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail='failed to retrieve expense summary')
    return expenses

@app.post('/expenses/{expense_date}')
def add_update_expenses(expense_date:date, expenses:list[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date,expense.amount,expense.category,expense.notes)
    return f'expenses updated successfully'

@app.post('/analytics/')
def get_analytics(date_range: DateRange):
    data=db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail='failed to retrieve expense summary')

    total = sum([row['total'] for row in data])
    breakdown={}
    for row in data:
        percentage=(row['total']/total)*100 if total !=0 else 0
        breakdown[row['category']]={
            "total":row['total'],
            "percentage":percentage

        }
    return breakdown

@app.post('/analytics_by_month/')
def get_analytics_by_month():
    data=db_helper.fetch_expense_summary_by_month()
    if data is None:
        raise HTTPException(status_code=500, detail='failed to retrieve expense summary')

    for item in data:
        item['month_name'] = calendar.month_name[item['month']][:3]

    dict = {item['month']: item for item in data}
    return dict

# new_dict = {}
# for item in data:
#     new_dict[item['month']] = {'total': item['total'], 'month_name': item['month_name']}
#
# print(new_dict)