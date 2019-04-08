from pyquery import PyQuery
import parse
import json
import os
import course

class SiakParser:
  '''
  takes html page of particular term and department, 
  outputs json file in data/ folder
  '''
  @staticmethod
  def html_to_json(html_file_name):
    html_string_content = ''
    with open(html_file_name, 'r') as html:
      html_string_content = ''.join(html.readlines())
    pq = PyQuery(html_string_content)
    row_generator = pq('table').children().items()
    # skip first two rows
    for j in range(2):
      next(row_generator)
    result = {'courses': []}
    this_course = {}
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
        parsed_course_info = parse.parse('{} - {} ({} SKS, Term {}); Kurikulum {}\n{}', row.text())
        this_course['course_code'] = parsed_course_info[0]
        this_course['course_name'] = parsed_course_info[1]
        this_course['sks'] = int(parsed_course_info[2])
        this_course['term'] = int(parsed_course_info[3])
        this_course['curriculum'] = parsed_course_info[4]
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
        this_course_class = {}
        this_course_class['name'] = this_class_info.eq(1).text()
        this_course_class['language'] = this_class_info.eq(2).text()
        this_course_class['schedule'] = []
        for class_schedule, class_room in zip(this_class_info.eq(4).text().split('\n'), this_class_info.eq(5).text().split('\n')):
          parsed_class_schedule = parse.parse('{}, {}-{}', class_schedule)
          this_course_class['schedule'].append({
                                            'day': parsed_class_schedule[0],
                                            'start': parsed_class_schedule[1],
                                            'end': parsed_class_schedule[2],
                                            'class': class_room,
                                          })
          this_course_class['lecturer'] = this_class_info.eq(6).text().split('\n')
        this_course['classes'].append(this_course_class)

    return result

class CourseParser:
  # takes complete json and returns list of (course, list of classes) tuple
  @staticmethod
  def get_course_to_classes_list(complete_json):
    if not (isinstance(complete_json, dict)):
      raise ValueError('json must be of type dict')
    list_of_tuple = []
    course_code_to_course = CourseParser.create_course_code_to_course(complete_json)
    for course in complete_json['courses']:
      tuple = (course_code_to_course[course['course_code']], [])
      for class_json in course['classes']:
        tuple[1].append(CourseParser.create_course_class_without_course(class_json))
      list_of_tuple.append(tuple)
    
    return list_of_tuple

  # takes complete json and returns dict of course code to course including prerequisites
  @staticmethod
  def create_course_code_to_course(complete_json):
    if not (isinstance(complete_json, dict)):
      raise ValueError('json must be of type dict')

    course_code_to_course = {}
    # make course objects
    for course_json in complete_json['courses']:
      course_code_to_course[course_json['course_code']] = course.Course(
        course_json['course_code'], 
        course_json['course_name'], 
        course_json['sks'], 
        course_json['term'], 
        course_json['curriculum']
      )
    # add prerequisites to each course
    for course_json in complete_json['courses']:
      for prerequisite in course_json['prerequisites']:
        try:
          course_code_to_course[course_json['course_code']].addPrerequisite(course_code_to_course[prerequisite['course_code']])
        except KeyError:
          course_code_to_course[prerequisite['course_code']] = course.Course(prerequisite['course_code'], prerequisite['course_name'])
          course_code_to_course[course_json['course_code']].addPrerequisite(course_code_to_course[prerequisite['course_code']])
    
    return course_code_to_course

  # takes json representing a class, returns course class with meetings
  @staticmethod
  def create_course_class_without_course(class_json):
    if not (isinstance(class_json, dict)):
      raise ValueError('json must be of type dict')
    
    course_class = course.CourseClass(class_json['name'], class_json['language'], None)    
    for meeting in class_json['schedule']:
      day = None
      if meeting['day'] == 'Senin':
        day = course.Day.MONDAY
      elif meeting['day'] == 'Selasa':
        day = course.Day.TUESDAY
      elif meeting['day'] == 'Rabu':
        day = course.Day.WEDNESDAY
      elif meeting['day'] == 'Kamis':
        day = course.Day.THURSDAY
      elif meeting['day'] == 'Jumat':
        day = course.Day.FRIDAY
      else:
        raise ValueError('json contain inappropriate day')
      course_class.addMeeting(course.Meeting(
        day, course.Time(meeting['start']), course.Time(meeting['end']), meeting['class']
      ))
    for lecturer_name in class_json['lecturer']:
      course_class.addLecturer(lecturer_name)

    return course_class


def main():
  html_dir = 'html/'
  data_dir = 'data/'
  
  for root, dirs, files in os.walk(html_dir):
    for file in files:
      if file.endswith('.html'):
        with open(data_dir + file.replace('.html', '') + '.json', 'w') as json_file:
          json_file.write(json.dumps(
            SiakParser.html_to_json(html_dir + file), indent=4, sort_keys=False
          ))

if __name__ == '__main__':
  main()