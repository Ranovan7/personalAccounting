# Generated by Django 2.1.5 on 2019-01-28 01:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moneyCirculation', '0002_auto_20190128_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reports',
            name='transactionDate',
            field=models.DateField(default=datetime.datetime(2019, 1, 28, 1, 36, 14, 169693, tzinfo=utc)),
        ),
    ]