import unittest

from backtracking import Backtracking
from course import Course, Meeting, Day

class Test(unittest.TestCase):
  def test_clashing_meetings(self):
    meetingA = Meeting(Day.MONDAY, 8, 10)
    meetingB = Meeting(Day.MONDAY, 9, 11)
    self.assertTrue(meetingA.clashWith(meetingB))
    self.assertTrue(meetingB.clashWith(meetingA))
    
    meetingC = Meeting(Day.MONDAY, 8, 9)
    meetingD = Meeting(Day.MONDAY, 8, 10)
    self.assertTrue(meetingC.clashWith(meetingD))
    self.assertTrue(meetingD.clashWith(meetingC))

  def test_non_clashing_meetings(self):
    meetingA = Meeting(Day.MONDAY, 8, 10)
    meetingB = Meeting(Day.MONDAY, 10, 12)
    self.assertFalse(meetingA.clashWith(meetingB))
    self.assertFalse(meetingB.clashWith(meetingA))

    meetingC = Meeting(Day.MONDAY, 8, 10)
    meetingD = Meeting(Day.THURSDAY, 8, 10)
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