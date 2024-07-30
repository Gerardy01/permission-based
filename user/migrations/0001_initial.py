# Generated by Django 5.0.7 on 2024-07-30 03:20

import django.db.models.deletion
import user.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('role_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(choices=[('SUPERADMIN', 'SUPERADMIN'), ('ADMIN', 'ADMIN'), ('PERMISSION1', 'PERMISSION1'), ('PERMISSION2', 'PERMISSION2')], max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('account_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.roles', verbose_name='Role')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', user.models.MyAccountManager()),
            ],
        ),
        migrations.AddField(
            model_name='roles',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='user.userpermission', verbose_name='Permissions'),
        ),
    ]
