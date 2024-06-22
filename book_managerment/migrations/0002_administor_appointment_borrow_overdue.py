# Generated by Django 5.0.6 on 2024-06-12 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_managerment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='administor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('username', models.CharField(max_length=32, verbose_name='姓名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
        ),
        migrations.CreateModel(
            name='appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_managerment.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_managerment.lmsuser')),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('borrow_date', models.DateField(max_length=64, verbose_name='借书日期')),
                ('return_date', models.DateField(max_length=64, verbose_name='还书日期')),
                ('is_return', models.BooleanField(default=False, verbose_name='是否归还')),
                ('is_overtime', models.BooleanField(default=False, verbose_name='是否超时')),
                ('is_renew', models.BooleanField(default=False, verbose_name='是否续借')),
                ('renew_date', models.DateField(max_length=64, verbose_name='续借日期')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_managerment.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_managerment.lmsuser')),
            ],
        ),
        migrations.CreateModel(
            name='overdue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('borrow_date', models.DateField(max_length=64, verbose_name='借书日期')),
                ('return_date', models.DateField(max_length=64, verbose_name='还书日期')),
                ('is_return', models.BooleanField(default=False, verbose_name='是否归还')),
                ('is_overtime', models.BooleanField(default=False, verbose_name='是否超时')),
                ('is_renew', models.BooleanField(default=False, verbose_name='是否续借')),
                ('renew_date', models.DateField(max_length=64, verbose_name='续借日期')),
                ('fine', models.IntegerField(default=0, verbose_name='罚款金额')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_managerment.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_managerment.lmsuser')),
            ],
        ),
    ]