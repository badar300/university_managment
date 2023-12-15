# # dissertation_app/models.py
#
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A admin can make it a External supervisor.
    role = models.CharField(max_length=20, default='Student')
    university_id = models.IntegerField()
    LegalStatus = models.CharField(max_length=20, default='Active')

    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Supervisor(models.Model):
    # Basically this will always be a internal supervisor
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university_id = models.IntegerField()
    job_title = models.CharField(max_length=20, default='teacher')


class Dissertation(models.Model):
    std_id = models.IntegerField(default=0, max_length=15)
    supervis_id = models.IntegerField(default=0, max_length=15)
    title = models.CharField(default='', max_length=200)
    faculty = models.CharField(default=None, max_length=15)
    institue = models.CharField(default=None, max_length=15)
    department = models.CharField(default=None, max_length=15)
    sub_year = models.CharField(default=None, max_length=15)
    def_year = models.CharField(default=None, max_length=15)
    def_grade = models.CharField(default=None, max_length=15)


class Major(models.Model):
    name = models.CharField(max_length=25)
    diploma_no = models.IntegerField(max_length=25)
    graduating_sem = models.IntegerField(max_length=25)
    starting_sem = models.IntegerField(max_length=25)
    faculty_otm = models.CharField(max_length=25)
    std_university_id = models.CharField(max_length=25)
    std_id = models.CharField(default=0, max_length=25)
    supervisor_id = models.CharField(max_length=25)
