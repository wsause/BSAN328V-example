import sqlite3
import datetime
import streamlit as st

st.title("Delete a ticket")

# After a delete, show the confirmation and empty the search box
if "delete_message" in st.session_state:
    st.success(st.session_state["delete_message"])
    del st.session_state["delete_message"]
    st.session_state["ticket_to_delete"] = None

# Search box (already filled in when coming from the View tickets page)
search_form = st.form("search_form")
ticketID = search_form.number_input("Ticket ID", value=None, step=1, key="ticket_to_delete")
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

        form = st.form(f"delete_form_{ticketID}")
        form.subheader(f"Ticket {ticketID}")
        form.text_input("Employee Name", value=row[1], disabled=True)
        form.text_input("Problem", value=row[2], disabled=True)

        col1, col2, col3 = form.columns(3)
        col1.selectbox("Priority", priorities, index=priorities.index(row[3]), disabled=True)
        col2.date_input("Date Submitted", value=datetime.date.fromisoformat(row[4]), disabled=True)
        col3.selectbox("Status", statuses, index=statuses.index(row[5]), disabled=True)

        submitted = form.form_submit_button("Delete ticket")

        if submitted:
            conn = sqlite3.connect('helpdesk.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tickets WHERE TicketID = ?", (ticketID,))
            conn.commit()
            conn.close()

            # Leave a message for the next run, then restart the page
            st.session_state["delete_message"] = f"Ticket {ticketID} deleted"
            st.rerun()