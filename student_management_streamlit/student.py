class Student:
    def __init__(self, student_id, name, email, department, marks):
        self.student_id = int(student_id)
        self.name = name
        self.email = email
        self.department = department
        self.marks = float(marks)
