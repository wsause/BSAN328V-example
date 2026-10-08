import sqlite3
import pandas as pd
import streamlit as st

st.header("View tickets")

# Get all the tickets
conn = sqlite3.connect('helpdesk.db')
df = pd.read_sql_query("SELECT * FROM Tickets", conn)
conn.close()

# Show the table and let the user select one row
event = st.dataframe(
    df,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
)

selected = event.selection.rows

if len(selected) > 0:
    ticketID = int(df.iloc[selected[0]]["TicketID"])

    if st.button("✏️ Update ticket"):
        st.session_state["ticket_to_update"] = ticketID
        st.switch_page("pages/update.py")

    if st.button("🗑️ Delete ticket"):
        st.session_state["ticket_to_delete"] = ticketID
        st.switch_page("pages/delete.py")
        # conn = sqlite3.connect('helpdesk.db')
        # cursor = conn.cursor()
        # cursor.execute("DELETE FROM Tickets WHERE TicketID = ?", (ticketID,))
        # conn.commit()
        # conn.close()
        # st.rerun()
else:
    st.caption("Select a ticket to update or delete it.")