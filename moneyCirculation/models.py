from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from babel.numbers import format_decimal


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"<{self.name} Category>"

    @property
    def serialize(self):
        '''
        Serialize the row to json format
        '''
        serialized = {
            'id': self.id,
            'name': self.name
        }
        return serialized


class Reports(models.Model):
    isExpense = models.BooleanField(default=True)
    amount = models.IntegerField()
    transactionDate = models.DateField(default=timezone.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        date = self.transactionDate.strftime('%d %B %Y')
        nominal = format_decimal(self.amount, locale='en_US')
        category_name = self.category.name
        status = "Expense" if self.isExpense else "Income"
        return f"<{status} report at {date} for Rp {nominal} on {category_name} from {self.owner.username}>"

    @property
    def serialize(self):
        '''
        Serialize the row to json format
        '''
        serialized = {
            'id': self.id,
            'isExpense': self.isExpense,
            'amount': self.amount,
            'date': self.transactionDate.strftime('%d %B %Y'),
            'category': self.category.name,
            'owner': self.owner.username
        }
        return serialized
