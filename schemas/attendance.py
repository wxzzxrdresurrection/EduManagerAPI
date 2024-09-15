from config.db import MongoConnection
from bson import ObjectId

class AttendanceSchema:
    def __init__(self):
        self.db = MongoConnection()
        self.attendance = []

    def get_all_attendance(self):
        attendance = self.db.get_collection("attendance")
        if not attendance:
            return []
        for att in attendance:
            att['id'] = str(att.pop('_id'))
            self.attendance.append(att)
        return self.attendance
    
    def get_attendance(self, att_id):
        att = self.db.get_item_from_collection_by_id("attendance", att_id)
        return att
    
    def add_attendance(self, att):
        att.day = att.day.isoformat()
        data = self.db.insert_item_into_collection("attendance", att.dict())
        return data

    def add_massive_attendance(self, att):
        data = self.db.insert_many_items_into_collection("attendance", att)
        return data

    def get_attendance_by_group(self, group_id):
        att = self.db.find_items_by_field("attendance", "group_id", group_id)
        return att
    