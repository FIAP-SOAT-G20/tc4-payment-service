
from pynamodb.attributes import UnicodeAttribute
from engine.app.repositories.models.default import BaseModel


class PaymentModel(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "payments"

    order_id = UnicodeAttribute() # precisa ser unique
    additional_data = UnicodeAttribute()
    title = UnicodeAttribute()
    status = UnicodeAttribute()
    qr_data = UnicodeAttribute(null=True)

    VALID_STATUSES = ["PROCESSING", "CONFIRMED", "FAILED", "ABORTED"]

    def save(self, *args, **kwargs):
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {self.status}")
        super().save(*args, **kwargs)
