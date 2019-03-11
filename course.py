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

  def clashWith(self, other):
    if not isinstance(other, Course):
      raise ValueError
    for this_meeting in self.meetings:
      for that_meeting in other.meetings:
        if this_meeting.clashWith(that_meeting):
          return True
    return False
    
class Meeting:
  '''
  represents one class session in a course
  example: IS class on Monday 13.00 - 14.40
  '''
  def __init__(self, day, start_time, end_time):
    if not (isinstance(day, Day) and isinstance(start_time, Time) and isinstance(end_time, Time)):
      raise ValueError('argument day must be instance of Day, start_time and end_time instance of Time')
    
    self.day = day
    self.start_time = start_time
    self.end_time = end_time
  
  def clashWith(self, other):
    if not isinstance(other, Meeting):
      raise ValueError('argument other must be instance of Meeting')
    
    if self.day == other.day and \
    (self.start_time == other.start_time or \
    self.start_time < other.start_time and other.start_time < self.end_time or \
    other.start_time < self.start_time and self.start_time < other.end_time):
      return True
    return False
  
class Day(Enum):
  '''
  represents what day a meeting is held
  '''
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6

class Time:
  '''
  represents time in hour and minute
  example: 08:00
  '''

  separator = ':'

  def __init__(self, hour_minute):
    if not (isinstance(hour_minute, str) and len(hour_minute) == 5 and Time.separator in hour_minute):
      raise ValueError('argument must be string 00:00-23:59')
    
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
