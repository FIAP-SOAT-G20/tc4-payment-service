from datetime import datetime

class Payment:

    _status = ""

    def __init__(self, id:str, created_at:datetime, order_id: str, additional_data: str,
                 title: str, status:str, updated_at = "", qr_data = ""):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.order_id = order_id
        self.additional_data = additional_data
        self.title = title
        self.status = status
        self.qr_data = qr_data

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status in ["PROCESSING", "CONFIRMED", "FAILED", "ABORTED"]:
            self._status = status
        else:
            raise ValueError("Invalid status")

