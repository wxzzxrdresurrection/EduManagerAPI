from models.group_model import Group
from config.db import MongoConnection

class GroupSchema:
    def __init__(self):
        self.db = MongoConnection()
        self.groups = []

    def get_groups(self):
        groups = self.db.get_collection("groups")
        if not groups:
            return []
        for group in groups:
            group['id'] = str(group.pop('_id'))
            self.groups.append(group)    
        return self.groups

    def get_group(self, group_id):
        group = self.db.get_item_from_collection_by_id("groups", group_id)
        return group

    def add_group(self, group):
        data = self.db.insert_item_into_collection("groups", group.dict())
        return data