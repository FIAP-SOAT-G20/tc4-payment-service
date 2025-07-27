
from pynamodb.attributes import UnicodeAttribute
from engine.app.repositories.models.default import BaseModel
from os import environ as environment


class PaymentModel(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "payments"
        region = "us-east-1"
        aws_access_key_id = environment.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = environment.get('AWS_SECRET_ACCESS_KEY')
        aws_session_token = environment.get('AWS_SESSION_TOKEN')

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
