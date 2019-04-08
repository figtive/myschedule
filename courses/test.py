import unittest

from django.contrib.staticfiles import finders

from courses.extra.backtracking import Backtracking
from courses.extra.course import CourseClass, Meeting, Day, Time
from courses.extra.courseparser import CourseParser, SiakParser
from json import loads

class Test(unittest.TestCase):
  def test_clashing_meetings(self):
    meetingA = Meeting(Day.MONDAY, Time('08.00'), Time('09.40'), '3.3113')
    meetingB = Meeting(Day.MONDAY, Time('09.00'), Time('10.40'), '3.3113')
    self.assertTrue(meetingA.clashWith(meetingB))
    self.assertTrue(meetingB.clashWith(meetingA))

  def test_non_clashing_meetings_in_same_day(self):
    meetingA = Meeting(Day.MONDAY, Time('08.00'), Time('09.40'), '3.3113')
    meetingB = Meeting(Day.MONDAY, Time('10.00'), Time('11.40'), '3.3113')
    self.assertFalse(meetingA.clashWith(meetingB))
    self.assertFalse(meetingB.clashWith(meetingA))
    
  def test_non_clashing_meetings_in_different_day(self):
    meetingC = Meeting(Day.MONDAY, Time('08.00'), Time('08.50'), '3.3113')
    meetingD = Meeting(Day.THURSDAY, Time('08.00'), Time('09.40'), '3.3113')
    self.assertFalse(meetingC.clashWith(meetingD))
    self.assertFalse(meetingD.clashWith(meetingC))

  def test_clashing_course(self):
    json_ddp2_a = {"name":"Kelas DDP 2 - A","language":"Indonesia","schedule":[{"day":"Senin","start":"16.00","end":"17.40","class":"A1.03 (Ged Baru)"},{"day":"Selasa","start":"10.00","end":"11.40","class":"A2.08 (Ged Baru)"},{"day":"Kamis","start":"10.00","end":"11.40","class":"A2.08 (Ged Baru)"},{"day":"Senin","start":"16.00","end":"17.40","class":"Lab A1.04 (Ged baru)"}],"lecturer":["Drs. Lim Yohanes Stefanus M.Math., Ph.D"]}
    json_ddp2_b = {"name":"Kelas DDP 2 - B","language":"Indonesia","schedule":[{"day":"Selasa","start":"08.00","end":"09.40","class":"A2.09 (Ged Baru)"},{"day":"Kamis","start":"08.00","end":"09.40","class":"A2.09 (Ged Baru)"},{"day":"Kamis","start":"16.00","end":"17.40","class":"Lab.1101/1103"}],"lecturer":["Dr. Fariz Darari","Laksmita Rahadianti S.Kom., M.Sc., Ph.D."]}
    ddp2_a = CourseParser.create_course_class_without_course(json_ddp2_a)
    ddp2_b = CourseParser.create_course_class_without_course(json_ddp2_b)
    self.assertFalse(ddp2_a.clashWith(ddp2_b))
    self.assertFalse(ddp2_b.clashWith(ddp2_a))
  
  def test_non_clashing_course(self):
    json_ddp2_d = {"name":"Kelas DDP 2 - D","language":"Indonesia","schedule":[{"day":"Selasa","start":"08.00","end":"09.40","class":"A2.07 (Ged baru)"},{"day":"Kamis","start":"08.00","end":"09.40","class":"A2.07 (Ged baru)"},{"day":"Kamis","start":"16.00","end":"17.40","class":"Lab.1107/1109"}],"lecturer":["Ardhi Putra Pratama Hartono S.Kom, M.Sc"]}
    json_ddp2_e = {"name":"Kelas DDP 2 - E","language":"Indonesia","schedule":[{"day":"Selasa","start":"08.00","end":"09.40","class":"A2.08 (Ged Baru)"},{"day":"Kamis","start":"08.00","end":"09.40","class":"A2.08 (Ged Baru)"},{"day":"Kamis","start":"16.00","end":"17.40","class":"Lab.2.2601"}],"lecturer":["Dipta Tanaya S.Kom, M.Kom."]}
    ddp2_d = CourseParser.create_course_class_without_course(json_ddp2_d)
    ddp2_e = CourseParser.create_course_class_without_course(json_ddp2_e)
    self.assertTrue(ddp2_d.clashWith(ddp2_e))
    self.assertTrue(ddp2_e.clashWith(ddp2_d))

  def test_simple_backtracking_with_solution(self):
    bt = Backtracking()
    bt.add_variable('a', [1,2,3])
    bt.add_variable('b', [2,3])
    bt.add_variable('c', [3])
    bt.add_binary_constraint_to_all(lambda x, y: x != y)
    self.assertEqual(bt.solve(), {'a':1, 'b':2, 'c':3})
  
  def test_simple_backtracking_without_solution(self):
    bt = Backtracking()
    bt.add_variable('a', [1,2])
    bt.add_variable('b', [1,2])
    bt.add_variable('c', [1,2])
    bt.add_binary_constraint_to_all(lambda x, y: x != y)
    self.assertEqual(bt.solve(), None)
  
  def test_course_backtracking_with_solution(self):
    bt = Backtracking()
    course_to_classes = None
    with open(finders.find('data/s1_ki.json'),'r') as json_file:
      course_to_classes = CourseParser.get_course_to_classes_list(loads(json_file.read()))
    for course, classes in course_to_classes:
      # select all term 4 ki courses (does not clash)
      if course.term == 4:
        bt.add_variable(course, classes)
    bt.add_binary_constraint_to_all(lambda x, y: not x.clashWith(y))
    result = bt.solve()
    self.assertNotEqual(result, None)
    self.assertEqual(len(result), 5)

if __name__ == '__main__':
  unittest.main()