import unittest

from backtracking import Backtracking
from course import Course, Meeting, Day, Time

class Test(unittest.TestCase):
  def test_clashing_meetings(self):
    meetingA = Meeting(Day.MONDAY, Time('08:00'), Time('09:40'))
    meetingB = Meeting(Day.MONDAY, Time('09:00'), Time('10:40'))
    self.assertTrue(meetingA.clashWith(meetingB))
    self.assertTrue(meetingB.clashWith(meetingA))

  def test_non_clashing_meetings(self):
    meetingA = Meeting(Day.MONDAY, Time('08:00'), Time('09:40'))
    meetingB = Meeting(Day.MONDAY, Time('10:00'), Time('11:40'))
    self.assertFalse(meetingA.clashWith(meetingB))
    self.assertFalse(meetingB.clashWith(meetingA))
    
  def test_non_clashing_meetings_2(self):
    meetingC = Meeting(Day.MONDAY, Time('08:00'), Time('08:50'))
    meetingD = Meeting(Day.THURSDAY, Time('08:00'), Time('09:40'))
    self.assertFalse(meetingC.clashWith(meetingD))
    self.assertFalse(meetingD.clashWith(meetingC))

  def test_backtracking_with_solution(self):
    bt = Backtracking()
    bt.add_variable('a', [1,2,3])
    bt.add_variable('b', [2,3])
    bt.add_variable('c', [3])
    bt.add_binary_constraint_to_all(lambda x, y: x != y)
    self.assertEqual(bt.solve(), {'a':1, 'b':2, 'c':3}.items())
  
  def test_backtracking_without_solution(self):
    bt = Backtracking()
    bt.add_variable('a', [1,2])
    bt.add_variable('b', [1,2])
    bt.add_variable('c', [1,2])
    bt.add_binary_constraint_to_all(lambda x, y: x != y)
    self.assertEqual(bt.solve(), None)

if __name__ == '__main__':
  unittest.main()