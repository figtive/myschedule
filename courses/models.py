from django.db import models
from itertools import product

class Department(models.Model):
  name = models.CharField(
    max_length=2,
    unique=True
  )

  def __str__(self):
    return self.name

class Course(models.Model):
  course_code = models.CharField(max_length=10, unique=True)
  course_name = models.CharField(max_length=40)
  sks = models.IntegerField(blank=True, null=True)
  term = models.IntegerField(blank=True, null=True)
  curriculum = models.CharField(max_length=16, blank=True)
  
  prerequisites = models.ManyToManyField(
    'self', symmetrical=False
  )
  departments = models.ManyToManyField(
    'Department', related_name='courses'
  )

  def __str__(self):
    return '{}:{}:{}'.format(self.course_code, ','.join(map(lambda d: d.name, self.departments.all())), self.course_name)

class CourseClass(models.Model):
  class Meta:
    unique_together = ('name', 'course', )

  name = models.CharField(max_length=40)
  LANGUAGE_CHOICES = (
    ('IDN', 'Indonesian'),
    ('ENG', 'English'),
  )
  language = models.CharField(
    max_length=3,
    choices=LANGUAGE_CHOICES, 
    blank=True
  )

  lecturers = models.ManyToManyField('Lecturer')
  course = models.ForeignKey(
    'Course', on_delete=models.CASCADE, related_name='course_classes', 
    blank=True, null=True
  )

  def clash_with(self, other):
    g = product(self.meetings.all(), other.meetings.all())
    try:
      while(True):
        meeting1, meeting2 = next(g)
        if meeting1.clash_with(meeting2):
          return True
    except StopIteration:
      pass
    return False

  def __str__(self):
    return self.name

class Lecturer(models.Model):
  name = models.CharField(max_length=60, unique=True)

  def __str__(self):
    return self.name

class Meeting(models.Model):
  DAY_CHOICES = (
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
  )
  day = models.CharField(
    max_length=3, 
    choices=DAY_CHOICES, 
    blank=True
  )
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  end_time = models.TimeField(auto_now=False, auto_now_add=False)
  class_room = models.CharField(max_length=15)

  course_class = models.ForeignKey(
    'CourseClass', on_delete=models.CASCADE, 
    related_name='meetings', blank=True, null=True
  )

  def clash_with(self, other):
    if self.day == other.day and self._time_overlap(other):
      return True
    else:
      return False
    
  def _time_overlap(self, other):
    if self.start_time == other.start_time:
      return True
    if self.start_time < other.start_time:
      return False if self.end_time < other.start_time else True
    else:
      return other._time_overlap(self)
  
  def __str__(self):
    return '{}:{}-{}:{}'.format(self.day, self.start_time.strftime('%H.%M'), self.end_time.strftime('%H.%M'), self.class_room)
