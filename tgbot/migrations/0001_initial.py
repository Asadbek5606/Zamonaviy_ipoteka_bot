# Generated by Django 2.2.7 on 2021-09-22 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_uz', models.TextField()),
                ('text_ru', models.TextField()),
            ],
            options={
                'verbose_name': 'Biz haqimizda',
                'verbose_name_plural': 'Biz haqimizda',
                'db_table': 'about_us',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=150)),
                ('name_ru', models.CharField(max_length=150)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tgbot.Category')),
            ],
            options={
                'verbose_name': 'Kategoriya',
                'verbose_name_plural': 'Kategoriyalar',
                'db_table': 'category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('comment_text', models.TextField()),
                ('username', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Kommentariya',
                'verbose_name_plural': 'Kommentariyalar',
                'db_table': 'comment',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('heading_uz', models.CharField(max_length=500)),
                ('heading_ru', models.CharField(max_length=500)),
                ('text_uz', models.TextField()),
                ('text_ru', models.TextField()),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('verify', models.CharField(max_length=20, null=True)),
                ('verify_counter', models.IntegerField(default=0)),
                ('lang_id', models.IntegerField()),
                ('chat_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Mijoz',
                'verbose_name_plural': 'Mijozlar',
                'db_table': 'user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=150)),
                ('name_ru', models.CharField(max_length=150)),
                ('description_uz', models.TextField()),
                ('description_ru', models.TextField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tgbot.Category')),
            ],
            options={
                'verbose_name': 'Mahsulot',
                'verbose_name_plural': 'Mahsulotlar',
                'db_table': 'product',
                'managed': True,
            },
        ),
    ]
