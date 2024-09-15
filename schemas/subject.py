from config.db import MongoConnection
from bson import ObjectId
from models.subject_model import Subject

class SubjectSchema:
    def __init__(self):
        self.mongo = MongoConnection()
        self.subjects = []

    def get_subjects(self):
        subjects = self.mongo.get_collection("subjects")
<<<<<<< HEAD
        if not subjects:
            return []
=======
>>>>>>> upstream/zapataLuis
        for subject in subjects:
            subject['id'] = str(subject.pop('_id'))
            self.subjects.append(Subject(**subject))
        return self.subjects

    def get_subject(self, subject_id):
        subject = self.mongo.get_item_from_collection_by_id("subjects", ObjectId(subject_id))
        return subject

    def add_subject(self, subject):
        data = self.mongo.insert_item_into_collection("subjects", subject.dict())
        return data
