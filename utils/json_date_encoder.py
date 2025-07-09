import json
from datetime import datetime, date

class DateTimeEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, (datetime, date)):
                return object.isoformat()
        return super().default(object)