from config.db import MongoConnection
from models.schedule_model import Schedule
from bson import ObjectId

class ScheduleSchema:
    def __init__(self):
        self.db = MongoConnection()
        self.schedules = []

    def get_all_schedules(self):
        schedules = self.db.get_collection("schedules")
        if not schedules:
            return []
        for schedule in schedules:
            schedule['id'] = str(schedule.pop('_id'))
            schedule['group_id'] = str(schedule.pop('group_id'))
            for sub in schedule['subjects_list']:
                sub['subject_id'] = str(sub.pop('subject_id'))
                sub['user_id'] = str(sub.pop('user_id'))
                print(sub)
            self.schedules.append(schedule)
        return self.schedules
    
    def get_schedule(self, schedule_id):
        schedule = self.db.get_item_from_collection_by_id("schedules", schedule_id)
        return schedule
    
    def add_schedule(self, schedule):
        data = self.db.insert_item_into_collection("schedules", schedule.dict())
        return data

    def get_schedule_by_group(self, group_id):
        schedules = self.db.get_collection("schedules")
        if not schedules:
            return []
        for schedule in schedules:
            schedule['id'] = str(schedule.pop('_id'))
            if schedule['group_id'] == ObjectId(group_id):
                self.schedules.append(schedule)
        return self.schedules