# Generated by Django 3.2.12 on 2022-11-23 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('corporate_memberships', '0025_auto_20201223_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorpProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corporate_memberships.corpprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='corpprofile',
            name='products',
            field=models.ManyToManyField(related_name='corpprofile_list', through='corporate_memberships.CorpProduct', to='products.Product', verbose_name='corporate / product'),
        ),
        migrations.AlterUniqueTogether(
            name='corpproduct',
            unique_together={('corp_profile', 'product')},
        ),
    ]
