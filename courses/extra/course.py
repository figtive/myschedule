from enum import Enum
from itertools import product

class Course:
  '''
  represents a course, 
  example: DDP2
  '''
  def __init__(self, course_code, course_name, sks=None, term=None, curriculum=None):
    self.course_code = course_code
    self.course_name = course_name
    self.sks = sks
    self.term = term
    self.curriculum = curriculum
    self.prerequisites = []
  
  def addPrerequisite(self, course):
    if not isinstance(course, Course):
      raise ValueError('course must be instance of Course')
    self.prerequisites.append(course)

  def __str__(self):
    return '{} {}, {} sks, term {}, curriculum {}\nprerequisites: {}'.format(
      self.course_code, self.course_name, self.sks, self.term, self.curriculum, 
      ', '.join(map(lambda p: '{} {}'.format(p.course_code, p.course_name), self.prerequisites))
    )

class CourseClass:
  '''
  represents class of course, 
  example: class DDP2 A of DDP2
  '''
  def __init__(self, name, language, course):
    self.name = name
    self.language = language
    self.meetings = []
    self.course = course
    self.lecturer = []
  
  def addMeeting(self, meeting):
    if not isinstance(meeting, Meeting):
      raise ValueError('meeting must be instance of Meeting')
    self.meetings.append(meeting)

  def addLecturer(self, lecturer_name):
    self.lecturer.append(lecturer_name)

  def setCourse(self, course):
    if not isinstance(course, Course):
      raise ValueError('course must be instance of Course')
    self.course = course

  def clashWith(self, other):
    if not isinstance(other, CourseClass):
      raise ValueError('other must be instance of CourseClass')
    g = product(self.meetings, other.meetings)
    try:
      while(True):
        meeting1, meeting2 = next(g)
        if meeting1.clashWith(meeting2):
          return True
    except StopIteration:
      pass
    return False
  
  def get_course_info(self):
    return {
      'course_code': self.course.course_code,
      'course_name': self.course.course_name,
      'sks': self.course.sks,
      'term': self.course.term,
      'curriculum': self.course.curriculum,
    }
  
  def __str__(self):
    result = '{}, language: {}, lecturer: {}\n'.format(self.name, self.language, ', '.join(self.lecturer))
    for meeting in self.meetings:
      result += '\t{}\n'.format(meeting)
    return result

class Meeting:
  '''
  represents one class session in a course, 
  example: DDP2 A class on Monday 13.00 - 14.40
  '''
  def __init__(self, day, start, end, class_room):
    if not (isinstance(day, Day)):
      raise ValueError('day must be instance of Day')
    if not (isinstance(start, Time) and isinstance(end, Time)):
      raise ValueError('start, end must be instance of Time')
    
    self.day = day
    self.start = start
    self.end = end
    self.class_room = class_room
  
  def clashWith(self, other):
    if not isinstance(other, Meeting):
      raise ValueError('other must be instance of Meeting')
    
    if self.day != other.day:
      return False
    
    if self.start == other.start:
      return True

    if self.start < other.start:
      return False if self.end < other.start else True
    else:
      return other.clashWith(self)
  
  def __str__(self):
    return '{:<10s} {}-{}  {}'.format(self.day, self.start, self.end, self.class_room)

class Day(Enum):
  '''
  represents day of class meeting held
  '''
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6

  def __str__(self):
    return self.name

class Time:
  '''
  represents time of class meeting held, 
  allows for comparison of Time objects
  '''

  separator = '.'

  def __init__(self, hour_minute):
    if not (isinstance(hour_minute, str) and len(hour_minute) == 5 and Time.separator in hour_minute):
      raise ValueError('hour_minute must be string from 00{}00 to 23{}59'.format(Time.separator, Time.separator))
    
    self.hour_int = int(hour_minute.split(Time.separator)[0])
    self.minute_int = int(hour_minute.split(Time.separator)[1])
    self.hour_string = "{:02d}".format(self.hour_int)
    self.minute_string = "{:02d}".format(self.minute_int)

  def __eq__(self, other):
    if isinstance(other, Time):
      return self.hour_int == other.hour_int and self.minute_int == other.minute_int
    return NotImplemented
  
  def __ne__(self, other):
    result = self.__eq__(other)
    if result is NotImplemented:
      return result
    return not result
  
  def __lt__(self, other):
    if isinstance(other, Time):
      return self.hour_int < other.hour_int or (self.hour_int == other.hour_int and self.minute_int < other.minute_int)
    return NotImplemented

  def __gt__(self, other):
    if isinstance(other, Time):
      return (not self.__lt__(other)) and (not self.__eq__(other))
    return NotImplemented
  
  def __le__(self, other):
    if isinstance(other, Time):
      return self.__lt__(other) or self.__eq__(other)
    return NotImplemented

  def __ge__(self, other):
    if isinstance(other, Time):
      return self.__gt__(other) or self.__eq__(other)
    return NotImplemented
  
  def __str__(self):
    return '{:s}{:s}{:s}'.format(self.hour_string, Time.separator, self.minute_string)
