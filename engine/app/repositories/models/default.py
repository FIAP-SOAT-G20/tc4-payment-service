from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.expressions.update import SetAction
from datetime import datetime, timezone


class BaseModel(Model):

    class Meta:
        table_name = None
        region = 'us-east-1'
        host = None


    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

    def save(self, *args, **kwargs):
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        super().save(*args, **kwargs)

    def update(self, actions=None, condition=None, **kwargs):
        if actions is None:
            actions = []

        now = datetime.now(timezone.utc)
        actions.append(BaseModel.updated_at.set(now))

        return super().update(actions=actions, condition=condition, **kwargs)

