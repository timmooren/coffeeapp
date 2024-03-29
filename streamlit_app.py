import streamlit as st
import csv
import random
import os

# Constants
CSV_FILE = "database.csv"


def is_name_in_csv(name, surname):
    try:
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            for row in reader:
                if name == row[0] and surname == row[1]:
                    return True
        return False
    except FileNotFoundError:
        return False


# Function to add a new name to the CSV database
def add_name_to_csv(name, surname):
    if not is_name_in_csv(name, surname):
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, surname])
        return True
    else:
        return False


def read_names_from_csv():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        return [f"{row[0]} {row[1]}" for row in reader]


st.title("☕️ Accenture Coffee Match App")

# show .webp image in streamlit
st.image("image.webp", use_column_width=True)


st.markdown(
    "Please register your name or find a coffee match by choosing one of the options below."
)

# Creating tabs
tab1, tab2 = st.tabs(["Submit Name", "Find Coffee Match"])

# Submit Name tab
with tab1:
    st.markdown(
        "👇 Here you can regster your name so someone else can find you as a coffee match."
    )
    with st.form("submit_name_form"):
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        submitted = st.form_submit_button("Submit")
        if submitted and name and surname:
            if add_name_to_csv(name, surname):
                st.success(f"Submitted: {name} {surname}")
            else:
                st.error("Name already exists in the database.")

# Find Coffee Match tab
with tab2:
    if st.button("Find Coffee Match"):
        database = read_names_from_csv()
        if len(database) > 1:
            # Ensuring the random choice is not the last submitted user, if applicable
            match = random.choice([person for person in database])
            st.balloons()
            st.write(f"Your coffee match is: {match}")
            st.write("Send them a message on Teams to schedule a coffee break! ☕️")

        else:
            st.write("Not enough people in the database for a match.")
