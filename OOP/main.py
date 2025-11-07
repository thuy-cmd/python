class Person:
    company = "Lang Son"
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def infor(self):
        print(f"Name: {self.name} - Age: {self.age}")
# person = Person("Eric", 20)

class Students:
    school_name = "CDSP Lang Son"
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

    def information(self):
        print("-----THONG TIN SINH VIEN-----")
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"School name: {self.school_name}")
    @classmethod
    def rename_school(cls, new_name):
        cls.school_name = new_name

Students.rename_school("CD Lang Son")
student = Students("Eric", "CD23TIN01")
student.information()
