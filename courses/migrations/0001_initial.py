# Generated by Django 2.2 on 2019-04-09 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('course_name', models.CharField(max_length=40)),
                ('sks', models.IntegerField(blank=True, null=True)),
                ('term', models.IntegerField(blank=True, null=True)),
                ('curriculum', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='CourseClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('language', models.CharField(blank=True, choices=[('IDN', 'Indonesian'), ('ENG', 'English')], max_length=3)),
                ('course', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_classes', to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('class_room', models.CharField(max_length=15)),
                ('course_class', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='courses.CourseClass')),
            ],
        ),
        migrations.AddField(
            model_name='courseclass',
            name='lecturers',
            field=models.ManyToManyField(to='courses.Lecturer'),
        ),
        migrations.AddField(
            model_name='course',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='courses', to='courses.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, to='courses.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='courseclass',
            unique_together={('name', 'course')},
        ),
    ]
