import streamlit as st

st.set_page_config(page_title="App Name", layout="wide")

# Streamlit supports Google's Material Symbols. 
# You can browse them at fonts.google.com/icons.
# create = st.Page("pages/create.py", title="Create a support ticket", default=True, icon=":material/add:")

# Or use the emoji picker
# Windows: press Win + . 
# Mac: press Ctrl + Cmd + Space
# Or browse and copy from a site like emojipedia.org
create = st.Page("pages/create.py", title="Create a support ticket", default=True, icon="🗒️")
view = st.Page("pages/view.py", title="View tickets", icon="👀")
update = st.Page("pages/update.py", title="Update ticket", icon="✏️")
delete = st.Page("pages/delete.py", title="Delete a ticket", icon="🗑️")

st.logo("it_help_desk_logo.png", size="large")

pg = st.navigation([create, view, update, delete])
pg.run()