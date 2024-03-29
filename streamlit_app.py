import streamlit as st
import sqlite3
import random

# Constants
DATABASE = "database.db"

# Initialize database connection
conn = sqlite3.connect(DATABASE)
c = conn.cursor()

# Create table if it doesn't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS people
             (name TEXT, surname TEXT, department TEXT)"""
)
conn.commit()


def is_name_in_sql(name, surname):
    c.execute("SELECT * FROM people WHERE name=? AND surname=?", (name, surname))
    return c.fetchone() is not None


def add_name_to_sql(name, surname, department):
    if not is_name_in_sql(name, surname):
        c.execute(
            "INSERT INTO people (name, surname, department) VALUES (?, ?, ?)",
            (name, surname, department),
        )
        conn.commit()
        return True
    else:
        return False


def delete_name_from_sql(name, surname):
    if is_name_in_sql(name, surname):
        c.execute("DELETE FROM people WHERE name=? AND surname=?", (name, surname))
        conn.commit()
        return True
    else:
        return False


def read_names_from_sql(department_filter="Any"):
    if department_filter == "Any":
        c.execute("SELECT name, surname, department FROM people")
    else:
        c.execute(
            "SELECT name, surname, department FROM people WHERE department=?",
            (department_filter,),
        )
    return [f"{row[0]} {row[1]} ({row[2]})" for row in c.fetchall()]


st.title("☕️ Accenture Coffee Match App")

# Show .webp image in streamlit
st.image("image.webp", use_column_width=True)
st.markdown("## 👋 Welcome to the coffee match app!")
st.markdown(
    "Please register your name or find a coffee match by choosing one of the options below."
)

# Creating tabs
tab1, tab2 = st.tabs(["Submit Name", "Find Coffee Match"])

# Submit Name tab
with tab1:
    st.markdown(
        "Here you can register your name so someone else can find you as a coffee match, or delete your name if it's already registered."
    )
    st.markdown("👇")
    with st.form("submit_name_form"):
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        department = st.selectbox(
            "Department", ["Sales", "Marketing", "Engineering", "Intelligence"]
        )
        submitted = st.form_submit_button("Submit", help="Registers your name")
        deleted = st.form_submit_button(
            ":red[Delete]", help="Deletes your registered name from the database"
        )  # Add Delete button

        if submitted and name and surname:
            if add_name_to_sql(name, surname, department):
                st.success(f"Submitted: {name} {surname} ({department})")
            else:
                st.error("Name already exists in the database.")
        if deleted and name and surname:  # Delete action
            if delete_name_from_sql(name, surname):
                st.success(f"Deleted: {name} {surname}")
            else:
                st.error("Name not found in the database.")

# Find Coffee Match tab
with tab2:
    st.markdown(
        "👇 Select a department and click the button below to find your coffee match 😊."
    )
    department_filter = st.selectbox(
        "Filter by Department",
        ["Any", "Sales", "Marketing", "Engineering", "Finance"],
        key="department_filter",
    )
    if st.button("Find Coffee Match"):
        database = read_names_from_sql(department_filter)
        if len(database) > 1:
            match = random.choice(database)
            st.balloons()
            st.write(f" ## Your coffee match is: {match}")
            st.write("📨 Send them a message on Teams to schedule a coffee break! ☕️")
            st.write(
                "🎫 Use the voucher below to grab a free coffee in the Accenture cafe!"
            )
            st.image("voucher.webp", use_column_width=True)

        else:
            st.write(
                "😢 Not enough people in the database for a match, or not enough people in the selected department."
            )
