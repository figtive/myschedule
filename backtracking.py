from itertools import combinations

from course import Course, Meeting, Day

class Backtracking:
  '''
  represents a CSP problem solved with backtracking search
  '''
  def __init__(self):
    self.variable_to_domain = {}
    self.assignments = {}
    self.constraint_function = None
    self.binary_contraints = []
  
  def add_variable(self, variable, values):
    # add new variable with it's domain values
    self.variable_to_domain[variable] = values
    self.assignments[variable] = None
  
  def add_binary_constraint_to_all(self, lambda_func):
    # add binary constraint specified in lambda_func to all current variables
    self.constraint_function = lambda_func
    self.binary_contraints = list(combinations(list(self.variable_to_domain.keys()), 2))
  
  def solve(self):
    # solve CSP with recursive backtracking search, returns a dictionary of assigned variables
    if self.all_variable_is_assigned():
      return self.assignments.items()
    variable = self.get_unassigned_variable()
    for value in self.variable_to_domain[variable]:
      self.assignments[variable] = value
      if self.constraint_is_satisfied():
        return self.solve()
      else:
        self.assignments[variable] = None
  
  def all_variable_is_assigned(self):
    # check wether all variables already have a value
    for key, value in self.assignments.items():
      if value == None:
        return False
    return True
  
  def get_unassigned_variable(self):
    # get a random unassigned variable
    for key, value in self.assignments.items():
      if value == None:
        return key
    return None
  
  def constraint_is_satisfied(self):
    # check if any assignment breaks constraint
    for variable_1, variable_2 in self.binary_contraints:
      if self.assignments[variable_1] != None and self.assignments[variable_2] != None and self.constraint_function(self.assignments[variable_1], self.assignments[variable_2]) == False:
        return False
    return True

def main():
  print('main')

if __name__ == '__main__':
  main()