from django.contrib.staticfiles import finders

from os import walk, path
from json import loads, dumps
from datetime import time
from timeit import default_timer as timer
from pyquery import PyQuery
from parse import parse

from .models import Course, CourseClass, Meeting, Lecturer, Department

def fill_all_course_data_to_db():
  start_time = timer()
  log = ''
  reset_db()
  data_dir = finders.find('data/')
  fill_department_table()
  for _, _, files in walk(data_dir):
    for file in files:
      if file.endswith('.json'):
        fill_specific_course_data_to_db(path.join(data_dir, file))
        
  end_time = timer()
  log += 'database populated in {} seconds.'.format(end_time - start_time)
  return log

def fill_department_table():
  # fill 3 departments: IK, SI and KI manually
  Department.objects.create(name='IK')
  Department.objects.create(name='SI')
  Department.objects.create(name='KI')

def reset_db():
  Department.objects.all().delete()
  Course.objects.all().delete()
  CourseClass.objects.all().delete()
  Meeting.objects.all().delete()
  Lecturer.objects.all().delete()

def fill_specific_course_data_to_db(path_to_data):
  # read json
  data_dict = None
  with open(path.join(path_to_data), 'r') as json_file:
    data_dict = loads(json_file.read())

  # determine department based on json file name
  current_department = None
  if 'ki' in path_to_data:
    current_department = 'KI'
  elif 'ik' in path_to_data:
    current_department = 'IK'
  elif 'si' in path_to_data:
    current_department = 'SI'

  for course_dict in data_dict['courses']:
    current_course = None
    # create course objects
    if not Course.objects.filter(course_code=course_dict['course_code']).exists():
      current_course = Course.objects.create(
        course_code = course_dict['course_code'], 
        course_name = course_dict['course_name'], 
        sks = course_dict['sks'], 
        term = course_dict['term'], 
        curriculum = course_dict['curriculum']
      )
      current_course.departments.add(Department.objects.get(name=current_department))
    else:
      current_course = Course.objects.get(course_code=course_dict['course_code'])
      # if course object is created but not complete (if it is read as prerequisite)
      if (not current_course.sks) or (not current_course.term) or (not current_course.curriculum):
        current_course.sks = course_dict['sks']
        current_course.term = course_dict['term']
        current_course.curriculum = course_dict['curriculum']
        current_course.save()
      # if current department not yet in this course's department, then add it
      if not current_course.departments.all().filter(name=current_department).exists():
        current_course.departments.add(Department.objects.get(name=current_department))
    # add prerequisites
    for prerequisite_dict in course_dict['prerequisites']:
      current_prerequisite = None
      # if no course created yet, create an incomplete one
      if not Course.objects.filter(course_code = prerequisite_dict['course_code']).exists():
        current_prerequisite = Course.objects.create(
          course_code = prerequisite_dict['course_code'], 
          course_name = prerequisite_dict['course_name']
        )
      else:
        current_prerequisite = Course.objects.get(course_code = prerequisite_dict['course_code'])
      current_course.prerequisites.add(current_prerequisite)
    # add classes to current course
    for class_dict in course_dict['classes']:
      language = None
      if class_dict['language'] == 'Indonesia':
        language = 'IDN'
      elif class_dict['language'] == 'Inggris':
        language = 'ENG'
      current_class = CourseClass.objects.create(
        name = class_dict['name'], 
        language = language, 
        course = current_course
      )
      # add lecturers to current class
      for lecturer_name in class_dict['lecturer']:
        current_lecturer = None
        if not Lecturer.objects.filter(name=lecturer_name).exists():
          current_lecturer = Lecturer.objects.create(name=lecturer_name)
        else:
          current_lecturer = Lecturer.objects.get(name=lecturer_name)
        current_class.lecturers.add(current_lecturer)
      # add meetings to current class
      for meeting_dict in class_dict['schedule']:
        day = None
        if meeting_dict['day'] == 'Senin':
          day = 'MON'
        elif meeting_dict['day'] == 'Selasa':
          day = 'TUE'
        elif meeting_dict['day'] == 'Rabu':
          day = 'WED'
        elif meeting_dict['day'] == 'Kamis':
          day = 'THU'
        elif meeting_dict['day'] == 'Jumat':
          day = 'FRI'
        elif meeting_dict['day'] == 'Sabtu':
          day = 'SAT'
        Meeting.objects.create(
          day = day, 
          start_time = time(
            hour = int(meeting_dict['start'].split('.')[0]), 
            minute = int(meeting_dict['start'].split('.')[1])
          ), 
          end_time = time(
            hour = int(meeting_dict['end'].split('.')[0]), 
            minute = int(meeting_dict['end'].split('.')[1])
          ), 
          class_room = meeting_dict['class'], 
          course_class = current_class
        )

class SiakParser:
  '''
  takes html page of particular term and department, 
  outputs json file in data/ folder
  '''
  @staticmethod
  def convert_all_html_to_json():
    html_dir = finders.find('html/')
    data_dir = finders.find('data/')
    for _, _, files in walk(html_dir):
      for file in files:
        if file.endswith('.html'):
          # SiakParser.convert_html_to_json(path.join(html_dir, file))
          data_file = file.replace('.html', '.json')
          SiakParser.convert_html_to_json(path.join(html_dir, file), path.join(data_dir, data_file))

  @staticmethod
  def convert_html_to_json(html_file_path, data_file_path):
    html_string_content = ''
    with open(html_file_path, 'r') as html:
      html_string_content = ''.join(html.readlines())
    pq = PyQuery(html_string_content)
    row_generator = pq('table').children().items()
    # skip first two rows
    for j in range(2):
      next(row_generator)
    result = {'courses': []}
    this_course = {}
    # get next row using generator
    while(True):
      try:
        row = next(row_generator)
      except StopIteration:
        if this_course != None:
          result['courses'].append(this_course)
        break
      # if start of new course
      if not (row.hasClass('alt') or row.hasClass('x')):
        if this_course:
          result['courses'].append(this_course)
          this_course = {}
        # parse table row text
        parsed_course_info = parse('{} - {} ({} SKS, Term {}); Kurikulum {}\n{}', row.text())
        this_course['course_code'] = parsed_course_info[0]
        this_course['course_name'] = parsed_course_info[1]
        this_course['sks'] = int(parsed_course_info[2])
        this_course['term'] = int(parsed_course_info[3])
        this_course['curriculum'] = parsed_course_info[4]
        # parse this course's prerequisites
        string_prerequisites = parsed_course_info[5]
        string_prerequisites = string_prerequisites.replace('Prasyarat:', '').strip()
        this_course_prerequisites = []
        if string_prerequisites:
          for pre_course in string_prerequisites.split(', '):
            pre_course_code, pre_course_name = pre_course.split(' - ')
            this_course_prerequisites.append({'course_code': pre_course_code, 'course_name': pre_course_name})
        this_course['prerequisites'] = this_course_prerequisites
        this_course['classes'] = []
      # if one of classes in current course
      else:
        this_class_info = row.find('td')
        # parse new class for this course
        this_course_class = {}
        this_course_class['name'] = this_class_info.eq(1).text()
        this_course_class['language'] = this_class_info.eq(2).text()
        this_course_class['schedule'] = []
        # parse meetings for this class
        for class_schedule, class_room in zip(this_class_info.eq(4).text().split('\n'), this_class_info.eq(5).text().split('\n')):
          parsed_class_schedule = parse('{}, {}-{}', class_schedule)
          this_schedule = {
            'day': parsed_class_schedule[0],
            'start': parsed_class_schedule[1],
            'end': parsed_class_schedule[2],
            'class': class_room,
          }
          # prevent duplicate meetings
          if not this_schedule in this_course_class['schedule']:
            this_course_class['schedule'].append(this_schedule)
          # parse list of lecturers
          this_course_class['lecturer'] = this_class_info.eq(6).text().split('\n')
        this_course['classes'].append(this_course_class)

    # write result into json file    
    with open(data_file_path, 'w') as json_:
      json_.write(dumps(result, indent=4, sort_keys=False))