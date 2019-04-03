from pyquery import PyQuery
import parse
import json
import os

class SiakParser:
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