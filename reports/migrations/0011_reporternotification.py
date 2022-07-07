# Generated by Django 3.2.12 on 2022-07-07 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_incidentreport_case_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReporterNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('condition', models.TextField()),
                ('template', models.TextField()),
                ('is_active', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
