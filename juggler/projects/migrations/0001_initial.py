# Generated by Django 3.1 on 2021-08-06 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(help_text='Unique project code; Usually the acronym of the name.', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('details', models.CharField(max_length=1000)),
                ('due_date', models.DateField(null=True)),
                ('completed', models.BooleanField(default=False, help_text='Task completion status')),
                ('priority', models.CharField(choices=[('!', 'Low'), ('!!', 'Medium'), ('!!!', 'HIGH')], default='!', max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
