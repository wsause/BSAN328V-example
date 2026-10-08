import sqlite3
import datetime
import streamlit as st

st.title("Update ticket")

# After an update, show the confirmation and empty the search box
if "update_message" in st.session_state:
    st.success(st.session_state["update_message"])
    del st.session_state["update_message"]
    st.session_state["ticket_to_update"] = None

# Search box (already filled in when coming from the View tickets page)
search_form = st.form("search_form")
ticketID = search_form.number_input("Ticket ID", value=None, step=1, key="ticket_to_update")
search_form.form_submit_button("Search")

if ticketID is not None:
    # Look up the ticket
    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tickets WHERE TicketID = ?", (ticketID,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        st.error(f"Ticket {ticketID} was not found")
    else:
        priorities = ["Low", "Medium", "High"]
        statuses = ["Open", "Resolved", "Closed"]

        form = st.form(f"update_form_{ticketID}")
        form.subheader(f"Ticket {ticketID}")
        employeeName = form.text_input("Employee Name", value=row[1])
        problem = form.text_input("Problem", value=row[2])

        col1, col2, col3 = form.columns(3)
        priority = col1.selectbox("Priority", priorities, index=priorities.index(row[3]))
        dateSubmitted = col2.date_input("Date Submitted", value=datetime.date.fromisoformat(row[4]))
        status = col3.selectbox("Status", statuses, index=statuses.index(row[5]))

        submitted = form.form_submit_button("Update ticket")

        if submitted:
            conn = sqlite3.connect('helpdesk.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Tickets SET EmployeeName = ?, Problem = ?, Priority = ?, "
                "DateSubmitted = ?, Status = ? WHERE TicketID = ?",
                (employeeName, problem, priority, str(dateSubmitted), status, ticketID)
            )
            conn.commit()
            conn.close()

            # Leave a message for the next run, then restart the page
            st.session_state["update_message"] = f"Ticket {ticketID} updated"
            st.rerun()