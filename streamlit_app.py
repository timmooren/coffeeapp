import streamlit as st
from sqlalchemy import create_engine, Column, String, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random

# Constants
DATABASE_URI = "sqlite:///database.db"
Base = declarative_base()

# Database setup
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


# Model definition
class Person(Base):
    __tablename__ = "people"
    name = Column(String, primary_key=True)
    surname = Column(String, primary_key=True)
    department = Column(String)


# Create table
Base.metadata.create_all(engine)


def is_name_in_sql(name, surname):
    return (
        session.query(Person).filter_by(name=name, surname=surname).first() is not None
    )


def add_name_to_sql(name, surname, department):
    if not is_name_in_sql(name, surname):
        new_person = Person(name=name, surname=surname, department=department)
        session.add(new_person)
        session.commit()
        return True
    else:
        return False


def delete_name_from_sql(name, surname):
    person = session.query(Person).filter_by(name=name, surname=surname).first()
    if person:
        session.delete(person)
        session.commit()
        return True
    else:
        return False


def read_names_from_sql(department_filter="Any"):
    if department_filter == "Any":
        people = session.query(Person).all()
    else:
        people = session.query(Person).filter_by(department=department_filter).all()
    return [
        f"{person.name} {person.surname} ({person.department})" for person in people
    ]


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
    st.info(
        " 👇 Here you can register your name so someone else can find you as a coffee match, or delete your name if it's already registered."
    )
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
                st.success(f"Registered: {name} {surname} ({department})")
            else:
                st.error("⚠️ Name already exists in the database.")
        if deleted and name and surname:  # Delete action
            if delete_name_from_sql(name, surname):
                st.success(f"Deleted: {name} {surname}")
            else:
                st.error("👀 Name not found in the database.")

# Find Coffee Match tab
with tab2:
    st.info(
        "👇 Select a department and click the button below to find your coffee match."
    )
    department_filter = st.selectbox(
        "Filter by Department",
        ["Any", "Sales", "Marketing", "Engineering", "Finance"],
        key="department_filter",
    )
    if st.button("🔎 Find Coffee Match"):
        database = read_names_from_sql(department_filter)
        if len(database) > 1:
            # put output in container
            with st.container(border=True):
                match = random.choice(database)
                st.balloons()
                st.write(f" ## Your coffee match is: {match}")
                st.info(
                    "📨 Send them a message on Teams to schedule a coffee break! ☕️"
                )
                st.success(
                    "🎫 Use the voucher below to grab a free coffee in the Accenture cafe!"
                )
                st.image("voucher.webp", use_column_width=True)

        else:
            st.write(
                "😢 Not enough people in the database for a match, or not enough people in the selected department."
            )

st.markdown("### Credits:")

st.markdown("This app was made by the Song 2024 interns:")
# link to timmooren.streamlit.app
st.link_button("Tim Mooren", "https://timmooren.streamlit.app")
st.button("More names")
