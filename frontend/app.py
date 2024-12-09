from http.client import responses

import pandas as pd
import streamlit as st
from datetime import datetime
import requests
# streamlit run .\app.py
#use st.write(response) to ensure responses are shown

api_url=('http://localhost:8000') #localhost=127.0.0.1
st.title('Expense Tracking System')
tab1,tab2,tab3= st.tabs(['Add/Update','Analytics By Category','Analytics By Months'])

with tab1:
    selected_date=st.date_input('Enter Date: ', datetime(2024,12,7),label_visibility='collapsed')
    response=requests.get(f'{api_url}/expenses/{selected_date}')
    if response.status_code==200:
        existing_expenses=response.json()
    else:
        st.error('failed to retrieve data')
        existing_expenses=[]

    categories=['Rent','Food','Fast Food','Shopping','Entertainment','Other']
    with st.form(key='expense_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Amount')
        with col2:
            st.subheader('Category')
        with col3:
            st.subheader('Notes')

        expenses=[]
        for i in range(5):

            if i <len(existing_expenses):
                amount=existing_expenses[i]['amount']
                category=existing_expenses[i]['category']
                notes=existing_expenses[i]['notes']
            else:
                amount=0.0
                category='Shopping'
                notes=''

            col1, col2, col3= st.columns(3)
            with col1:
                amount_input=st.number_input(label='amount',min_value=0.0, step=1.0, value=amount, key=f'amount_{i}',label_visibility="collapsed")
            with col2:
                category_input=st.selectbox(label='category',options=categories,index=categories.index(category), key=f'category_{i}',label_visibility="collapsed")
            with col3:
                notes_input=st.text_input(label='notes',value=notes, key=f'notes_{i}',label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button=st.form_submit_button()
        if submit_button:
            filtered_expenses=[expense for expense in expenses if expense['amount']>0]
            response=requests.post(f'{api_url}/expenses/{selected_date}',json=filtered_expenses)
            if response.status_code==200:
                st.success('expenses updated successfully')
            else:
                st.error('failed to update expenses')

with tab2:
    col1,col2= st.columns(2) #to put start and end in one row
    with col1:
        start_date=st.date_input('Start Date', datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input('End Date', datetime(2024, 8, 5))

    if st.button('Get Analytics',key=1): #payload will be whatever you put in postman which is start and end date
        payload={
            'start_date':start_date.strftime('%Y-%m-%d'),
            'end_date':end_date.strftime('%Y-%m-%d')

        }
        response=requests.post(f'{api_url}/analytics', json=payload)
        response=response.json()

        data={
            'category': list(response.keys()),
            'total': [response[category]['total'] for category in response],
            'percentage':[response[category]['percentage'] for category in response]
        }

        df=pd.DataFrame(data)
        df_sorted=df.sort_values(by='percentage',ascending=False)
        st.title('Expense Breakdown By Category')
        st.bar_chart(data=df_sorted.set_index('category')['percentage'], width=0, height=0, use_container_width=True)

        df_sorted["total"] = df_sorted["total"].map("{:.2f}".format)
        df_sorted["percentage"] = df_sorted["percentage"].map("{:.2f}".format)

        st.table(df_sorted)

with tab3:
    response=requests.post(f'{api_url}/analytics_by_month')
    if response.status_code==200:
        if st.button('Get Analytics',key=2):
            response=response.json()
            data={
            'month': [response[month]['month']for month in response],
            'month_name': [response[month]['month_name']for month in response],
            'total': [response[month]['total'] for month in response]
            }
            df=pd.DataFrame(data)

            st.bar_chart(data=df, x='month_name', y='total', use_container_width=True)
            df['total']=df['total'].astype(int)

            st.table(data=df.set_index('month'))

    else:
        st.error('failed to retrieve data')








