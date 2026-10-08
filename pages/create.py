import streamlit as st
import sqlite3

st.header("Create a support ticket")

form = st.form("my_form")
employeeName = form.text_input("Employee Name")
problem = form.text_area("Problem")
col1, col2, col3 = form.columns(3)
priority = col1.selectbox("Priority", ("Low", "Medium", "High"))
dateSubmitted = col2.date_input("Date Submitted")
status = col3.selectbox("Status", ("Open", "Resolved", "Closed"))

# Now add a submit button to the form:
submitted = form.form_submit_button("Submit")

if submitted:
    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Tickets (EmployeeName, Problem, Priority, DateSubmitted, Status) "
        "VALUES (?, ?, ?, ?, ?)",
        (employeeName, problem, priority, str(dateSubmitted), status)
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    st.success(f"Ticket {new_id} created")