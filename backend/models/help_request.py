import uuid
from datetime import datetime

class HelpRequest:
    def __init__(self, question, caller_info):
        self.id = str(uuid.uuid4())
        self.question = question
        self.caller_info = caller_info
        self.status = "Pending"  # Pending, Resolved, Timeout
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.resolved_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "caller_info": self.caller_info,
            "status": self.status,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at
        }
