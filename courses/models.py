from django.db import models
from itertools import product

class Course(models.Model):
  course_code = models.CharField(max_length=10, primary_key=True)
  course_name = models.CharField(max_length=40)
  sks = models.IntegerField(blank=True, null=True)
  term = models.IntegerField(blank=True, null=True)
  curriculum = models.CharField(max_length=16, blank=True)
  prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

  def __str__(self):
    return '{}:{}'.format(self.course_code, self.course_name)

class CourseClass(models.Model):
  name = models.CharField(max_length=40)
  language = (
    ('IDN', 'Indonesian'),
    ('ENG', 'English'),
  )
  lecturers = models.ManyToManyField('Lecturer')
  course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_classes', blank=True)

  def clash_with(self, other):
    if isinstance(other, CourseClass):
      raise ValueError('other must be instance of CourseClass')
    g = product(self.meetings, other.meetings)
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
  name = models.CharField(max_length=60)

  def __str__(self):
    return self.name

class Meeting(models.Model):
  day = (
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
  )
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  end_time = models.TimeField(auto_now=False, auto_now_add=False)
  course_class = models.ForeignKey('CourseClass', on_delete=models.CASCADE, related_name='meetings', blank=True)

  def clash_with(self, other):
    if isinstance(other, Meeting):
      raise ValueError('other must be instance of Meeting')
    if self.day == other.day and self._time_overlap(other):
      return True
    else:
      return False
    
  def _time_overlap(self, other):
    if isinstance(other, Meeting):
      raise ValueError('other must be instance of Meeting')
    if self.start_time == other.start_time:
      return True
    if self.start_time < other.start_time:
      return False if self.end_time < other.start_time else True
    else:
      return other._time_overlap(self)
