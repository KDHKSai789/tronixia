import streamlit as st
import database
from student import Student


# FIX CURSOR ISSUE
st.markdown("""
<style>
section[data-testid="stSidebar"] * {
    cursor: pointer !important;
}
.stSelectbox div {
    cursor: pointer !important;
}
.stButton button {
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)


# CREATE TABLE
database.create_table()


# TITLE
st.title("🎓 Student Management System")
st.divider()


# SIDEBAR MENU
menu = [
    "➕ Add Student",
    "📋 View Students",
    "✏ Update Student",
    "🗑 Delete Student"
]

choice = st.sidebar.selectbox("Navigation", menu)


# ADD STUDENT
if choice == "➕ Add Student":

    st.subheader("Add New Student")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
        format="%d"
    )

    name = st.text_input("Name")

    email = st.text_input("Email")

    department = st.text_input("Department")

    marks = st.number_input(
        "Marks",
        min_value=0.0,
        max_value=100.0
    )

    if st.button("Add Student"):

        if name == "" or email == "" or department == "":
            st.error("Please fill all fields")

        else:
            student = Student(
                student_id,
                name,
                email,
                department,
                marks
            )

            if database.add_student(student):
                st.success("Student added successfully")
            else:
                st.error("Student ID already exists")


# VIEW STUDENTS
elif choice == "📋 View Students":

    st.subheader("Student Records")

    data = database.get_students()

    if data:
        st.table(
            {
                "Student ID": [row[0] for row in data],
                "Name": [row[1] for row in data],
                "Email": [row[2] for row in data],
                "Department": [row[3] for row in data],
                "Marks": [row[4] for row in data],
            }
        )
    else:
        st.info("No students found")


# UPDATE STUDENT
elif choice == "✏ Update Student":

    st.subheader("Update Student")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
        format="%d"
    )

    name = st.text_input("New Name")

    email = st.text_input("New Email")

    department = st.text_input("New Department")

    marks = st.number_input(
        "New Marks",
        min_value=0.0,
        max_value=100.0
    )

    if st.button("Update Student"):

        student = Student(
            student_id,
            name,
            email,
            department,
            marks
        )

        database.update_student(student)

        st.success("Student updated successfully")


# DELETE STUDENT
elif choice == "🗑 Delete Student":

    st.subheader("Delete Student")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1,
        format="%d"
    )

    if st.button("Delete Student"):

        database.delete_student(student_id)

        st.success("Student deleted successfully")
