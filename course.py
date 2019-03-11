from enum import Enum

class Course:
  def __init__(self, name, code, lecturer, credit):
    self.name = name
    self.code = code
    self.lecturer = lecturer
    self.credit = credit
    self.meetings = []
  
  def addMeeting(self, meeting):
    self.meetings.append(meeting)

  def clashWith(self, course):
    if type(course) != Course:
      raise ValueError
    for this_meeting in self.meetings:
      for that_meeting in course.meetings:
        if this_meeting.clashWith(that_meeting):
          return True
    return False
    
class Meeting:
  '''
  represents one class session in a course
  example: IS class on Monday 13.00 - 14.40
  '''
  def __init__(self, day, start, end):
    self.day = day
    self.start = start
    self.end = end
  
  def clashWith(self, meeting):
    if type(meeting) != Meeting:
      raise ValueError
    if self.day == meeting.day:
      if self.start == meeting.start:
        return True
      if self.start < meeting.start and meeting.start < self.end:
        return True
      if meeting.start < self.start and self.start < meeting.end:
        return True
    return False
  
class Day(Enum):
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6