# Generated by Django 1.11.16 on 2018-10-08 12:43


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_auto_20160308_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='variance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
