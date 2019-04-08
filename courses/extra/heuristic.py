from course import Course

class Heuristic:
  def get_morning_evening_index(list_of_courses):
    # returns a more negative integer if list of courses has many morning classes
    # and a more positive integer if evening classes

    if not (isinstance(list_of_courses, (list, Course))):
      raise ValueError('argument must be list of Courses')

    # TODO
    an_int = 0
    return an_int
  
  def get_class_spread_index(list_of_courses):
    # returns a more negative integer if classes across the week is less spread
    # and a more positive integer if more evenly spread

    if not (isinstance(list_of_courses, (list, Course))):
      raise ValueError('argument must be list of Courses')

    # TODO
    an_int = 0
    return an_int