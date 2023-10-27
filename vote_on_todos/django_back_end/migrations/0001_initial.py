# Generated by Django 4.2.6 on 2023-10-26 10:58
from __future__ import annotations

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListEvent',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('event_type', models.CharField(max_length=100)),
                ('event_type_version', models.IntegerField()),
                ('list_id', models.CharField(db_index=True, max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('payload', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='TodoEvent',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('event_type', models.CharField(max_length=100)),
                ('event_type_version', models.IntegerField()),
                ('todo_id', models.CharField(db_index=True, max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('payload', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='TodoEventSequence',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('todo_id', models.CharField(max_length=100)),
                ('index', models.PositiveIntegerField()),
                (
                    'event', models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='django_back_end.todoevent',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ListEventSequence',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True,
                        primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('list_id', models.CharField(max_length=100)),
                ('index', models.PositiveIntegerField()),
                (
                    'event', models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='django_back_end.listevent',
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='todoeventsequence',
            constraint=models.UniqueConstraint(
                fields=('todo_id', 'index'), name='unique_index_per_todo_id',
            ),
        ),
        migrations.AddConstraint(
            model_name='listeventsequence',
            constraint=models.UniqueConstraint(
                fields=('list_id', 'index'), name='unique_index_per_list_id',
            ),
        ),
    ]
