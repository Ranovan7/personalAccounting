from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    total = models.IntegerField()
    savings = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<{self.owner} Wallet have Rp {self.total}>"

    @property
    def serialize(self):
        '''
        Serialize the row to json format
        '''
        serialized = {
            'id': self.id,
            'total': self.total,
            'savings': self.savings,
            'owner': self.owner.username
        }
        return serialized
