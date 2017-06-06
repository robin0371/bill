# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 11:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillRub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Счет в рублях')),
            ],
            options={
                'verbose_name_plural': 'Счета в рублях',
                'db_table': 'bill_rub',
                'verbose_name': 'Счет в рублях',
            },
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('inn', models.CharField(max_length=12, verbose_name='ИНН')),
            ],
            options={
                'verbose_name_plural': 'Пользователи',
                'db_table': 'user_card',
                'verbose_name': 'Пользователь',
            },
        ),
        migrations.AddField(
            model_name='billrub',
            name='user_card',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transfer.UserCard', verbose_name='Пользователь'),
        ),
    ]
