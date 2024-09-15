from config.db import MongoConnection

class StudentSchema:
    def __init__(self):
        self.mongo = MongoConnection()
        self.students = []

    def get_students(self):
        students = self.mongo.get_collection("students")
        if not students:
            return []
        for student in students:
            student['id'] = str(student.pop('_id'))
            self.students.append(student)
        return self.students

    def get_student(self, student_id):
        student = self.mongo.get_item_from_collection_by_id("students", student_id)
        return student

    def add_student(self, student):
        data = self.mongo.insert_item_into_collection("students", student.dict())
        return data