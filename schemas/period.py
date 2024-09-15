from models.period_model import Period
from config.db import MongoConnection

class PeriodSchema():
    def __init__(self):
        self.mongo = MongoConnection()
        self.periods = []

    def get_all_periods(self):
        periods = self.mongo.get_collection("periods")
        if not periods:
            return []
        for period in periods:
            period['id'] = str(period.pop('_id'))
            self.periods.append(period)
        return self.periods
    
    def get_period(self, period_id):
        period = self.mongo.get_item_from_collection_by_id("periods", period_id)
        return period
    
    def add_period(self, period):
        period.start_date = period.start_date.isoformat()
        period.end_date = period.end_date.isoformat()
        print(period.dict())
        data = self.mongo.insert_item_into_collection("periods", period.dict())
        return data