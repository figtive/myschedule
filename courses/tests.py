from django.test import TestCase
from django.contrib.staticfiles import finders
from django.db.models import Q

from datetime import time
from itertools import product

from .models import *
from .utils import fill_specific_course_data_to_db, fill_department_table
from .backtracking import Backtracking


class BacktrackingTest(TestCase):
  def test_simple_bt_with_solution_of_ki_data(self):
    # populate test database with s1_ki.json data
    data_dir = finders.find('data/s1_ki.json')
    fill_department_table()
    fill_specific_course_data_to_db(data_dir)

    # setup backtracking CSP
    bt = Backtracking()
    # select only courses for term 4
    for course in Course.objects.all().filter(term = 4):
      bt.add_variable(course, list(course.course_classes.all()))
    bt.add_binary_constraint_to_all(lambda a, b: not a.clash_with(b))
    result = bt.solve()

    self.assertNotEqual(result, None)
    self.assertEqual(len(result), Course.objects.all().filter(term = 4).count())
    for course, class_ in result.items():
      self.assertNotEqual(class_, None)
  
  def test_simple_bt_with_solution_of_ik_data(self):
    # populate test database with s1_ki.json data
    data_dir = finders.find('data/s1_ik.json')
    fill_department_table()
    fill_specific_course_data_to_db(data_dir)
    # setup backtracking CSP
    bt = Backtracking()
    # select only courses for term 4
    for course in Course.objects.all().filter(term = 4):
      bt.add_variable(course, list(course.course_classes.all()))
    bt.add_binary_constraint_to_all(lambda a, b: not a.clash_with(b))
    result = bt.solve()

    self.assertNotEqual(result, None)
    self.assertEqual(len(result), Course.objects.all().filter(term = 4).count())
    for course, class_ in result.items():
      self.assertNotEqual(class_, None)

  def test_bt_with_no_solution(self):
    # populate test database with s1_ki.json data
    data_dir = finders.find('data/s1_ki.json')
    fill_department_table()
    fill_specific_course_data_to_db(data_dir)

    # setup backtracking CSP with MD2 and RPL as variables
    # which have clashing schedule
    bt = Backtracking()
    for course in Course.objects.all().filter(Q(course_name='Matematika Diskrit 2') | Q(course_name='Rekayasa Perangkat Lunak')):
      bt.add_variable(course, list(course.course_classes.all()))
    bt.add_binary_constraint_to_all(lambda a, b: not a.clash_with(b))
    result = bt.solve()
    
    self.assertEqual(len(bt.variable_to_domain), 2)
    self.assertEqual(result, None)

class CourseClassTestCase(TestCase):
  def setUp(self):
    # setup 3 course classes, c1 and c2 have
    # clashing schedule
    c1 = CourseClass.objects.create(name = 'Kelas Linear Algebra')
    c1.meetings.add(Meeting.objects.create(
      day='MON', 
      start_time = time(hour=10, minute=0), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    ))
    c2 = CourseClass.objects.create(name = 'Kelas Data Base')
    c2.meetings.add(Meeting.objects.create(
      day='MON', 
      start_time = time(hour=10, minute=0), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    ))
    c3 = CourseClass.objects.create(name = 'Kelas Programming Found 2')
    c3.meetings.add(Meeting.objects.create(
      day='TUE', 
      start_time = time(hour=8, minute=0), 
      end_time = time(hour=9, minute=40), 
      class_room = '-'
    ))
  
  def test_clashing_course_class(self):
    a = CourseClass.objects.get(name='Kelas Linear Algebra')
    b = CourseClass.objects.get(name='Kelas Data Base')
    self.assertTrue(a.clash_with(b))
    self.assertTrue(b.clash_with(a))

  def test_non_clashing_course_class(self):
    a = CourseClass.objects.get(name='Kelas Data Base')
    b = CourseClass.objects.get(name='Kelas Programming Found 2')
    self.assertFalse(a.clash_with(b))
    self.assertFalse(b.clash_with(a))

class MeetingTestCase(TestCase):
  def test_clasing_meetings(self):
    m1 = Meeting.objects.create(
      day='MON', 
      start_time = time(hour=10, minute=0), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    )
    m2 = Meeting.objects.create(
      day='MON', 
      start_time = time(hour=10, minute=40), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    )
    self.assertTrue(m1.clash_with(m2))
    self.assertTrue(m2.clash_with(m1))
  
  def test_non_clasing_meetings_same_day(self):
    m1 = Meeting.objects.create(
      day='MON', 
      start_time = time(hour=10, minute=0), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    )
    m2 = Meeting.objects.create(
      day='MON', 
      start_time = time(hour=12, minute=0), 
      end_time = time(hour=12, minute=50), 
      class_room = '-'
    )
    self.assertFalse(m1.clash_with(m2))
    self.assertFalse(m2.clash_with(m1))
  
  def test_non_clasing_meetings_different_day(self):
    m1 = Meeting.objects.create(
      day='MON', 
      start_time = time(hour=10, minute=0), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    )
    m2 = Meeting.objects.create(
      day='Tue', 
      start_time = time(hour=10, minute=0), 
      end_time = time(hour=11, minute=40), 
      class_room = '-'
    )
    self.assertFalse(m1.clash_with(m2))
    self.assertFalse(m2.clash_with(m1))