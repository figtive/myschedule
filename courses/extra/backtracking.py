from itertools import combinations

from .course import Course, Meeting, Day

class Backtracking:
  '''
  represents a CSP problem solved with backtracking search
  '''
  def __init__(self):
    self.variable_to_domain = {}
    self.assignments = {}
    self.constraint_function = None
    self.binary_contraints = []
  
  # add new variable with it's possible values
  def add_variable(self, variable, values):
    self.variable_to_domain[variable] = values
    self.assignments[variable] = None
  
  # add binary constraint specified in lambda_func to all current variables
  def add_binary_constraint_to_all(self, lambda_func):
    self.constraint_function = lambda_func
    self.binary_contraints = list(combinations(list(self.variable_to_domain.keys()), 2))
  
  # solve CSP with recursive backtracking search, returns a dictionary of assigned variables
  def solve(self):
    if self.all_variable_is_assigned():
      return self.assignments
    variable = self.get_unassigned_variable()
    for value in self.variable_to_domain[variable]:
      self.assignments[variable] = value
      if self.constraint_is_satisfied():
        return self.solve()
      else:
        self.assignments[variable] = None
  
  # check wether all variables already have a value
  def all_variable_is_assigned(self):
    for _, value in self.assignments.items():
      if value == None:
        return False
    return True
  
  # get a random unassigned variable
  def get_unassigned_variable(self):
    for key, value in self.assignments.items():
      if value == None:
        return key
    return None
  
  # check if any assignment breaks constraint
  def constraint_is_satisfied(self):
    for var1, var2 in self.binary_contraints:
      if self.assignments[var1] and self.assignments[var2] and \
        not self.constraint_function(
          self.assignments[var1], self.assignments[var2]
        ):
        return False
    return True

def main():
  pass

if __name__ == '__main__':
  main()