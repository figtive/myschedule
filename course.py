from enum import Enum
import json
import rhinoscriptsyntax as rs



#prompt the user for a file to import
filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
filename = rs.OpenFileName("Open JSON File", filter)

#Read JSON data into the datastore variable
if filename:
    with open(filename, 'r') as f:
        datastore = json.load(f)

#Use the new datastore datastructure
print datastore["day"]["start"]["end"]


# with open("data.json", "w") as write_file:
#    json.dump(data, write_file) 

# class CsvCourseReader:
  # def create_courses_from(csv_file_path):
    # '''
    # read data from a csv file, create courses and 
    # return a dictionary of course name to list of course classes 

    # example: 
    # ddp2a = Course('DDP2', 'A', 'Drs. Lim Yohanes Stefanus M.Math., Ph.D', '4')
    # ddp2a.addMeeting(Day.MONDAY, Time('16:00'), Time('17.40'))
    # ddp2a.addMeeting(...) # until all class session is included

    # ddp2b = Course('DDP2', 'B', 'Dr. Fariz Darari', '4')
    # ddp2b.addMeeting(...) # until all class session is included

    # dictionary_returned = {'DDP2': [ddp2a, ddp2b, ...], 'Anum': [..., ...]}
    # '''

    # if not (isinstance(csv_file_path, str)):
      # raise ValueError('argument csv_file_path must be string')

    # # TODO
    # file_pointer = open(csv_file_path, 'r')
    # course_name_to_available_courses = {'DDP2': []}

    # return course_name_to_available_courses

class Course:
  '''
  represents a class of a course
  example: class DDP2 A of 'DDP2'
  '''
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
  represents what day a class session is held
  '''
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6

class Time:
  '''
  represents time in hour and minute, allows for comparison of Time objects
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
