# Generated by Django 5.0.6 on 2024-06-12 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_managerment', '0003_alter_book_publisher_delete_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=64, null=True, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='book',
            name='catagoery',
            field=models.CharField(max_length=64, null=True, verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=64, null=True, verbose_name='出版社'),
        ),
    ]
