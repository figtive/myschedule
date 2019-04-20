from itertools import combinations
import copy

class Backtracking:
  '''
  represents a CSP problem solved with backtracking search

  TODO:
  - update constraint upon add_variable
  - add argument type checking
  '''
  def __init__(self):
    self.variable_to_domain = {}
    self.variable_to_legal_values = {}
    self.solutions = []
    self.assignments = {}
    self.constraint_function = None
    self.binary_contraints = []
  
  def add_variable(self, variable, values):
    '''
    add new variable with values
    '''
    self.variable_to_domain[variable] = values
    self.variable_to_legal_values[variable] = copy.deepcopy(values)
    self.assignments[variable] = None
  
  def add_binary_constraint_to_all(self, lambda_func):
    '''
    add binary constraints lambda_func to current variables
    '''
    self.constraint_function = lambda_func
    self.binary_contraints = list(combinations(list(self.variable_to_domain.keys()), 2))
  
  def get_solution(self):
    if self.solutions == []:
      self.get_solution_helper()
    return self.solutions[0] if len(self.solutions) > 0 else None

  def get_solutions(self):
    if self.solutions == []:
      self.get_solution_helper()
    return self.solutions if len(self.solutions) > 0 else None

  def get_solution_helper(self):
    '''
    do backtracking search with variables and values in 
    self.variable_to_domain, returning a dictionary of
    assignments or None if no possible assignment
    '''
    if self.all_variable_is_assigned():
      self.solutions.append(copy.deepcopy(self.assignments))
      return
    variable = self.get_unassigned_variable()
    while(True):
      value = self.get_legal_value(variable)
      self.do_forward_chaining(variable, value)
      if value == None:
        self.assignments[variable] = None
        self.variable_to_legal_values[variable] = copy.deepcopy(self.variable_to_domain[variable])
        break
      self.assignments[variable] = value
      if self.constraint_is_satisfied():
        self.get_solution_helper()
      else:
        self.assignments[variable] = None
  
  def all_variable_is_assigned(self):
    '''
    return true if all variables in assignment are assigned, 
    return false otherwise
    '''
    for _, value in self.assignments.items():
      if value == None:
        return False
    return True
  
  def get_unassigned_variable(self):
    '''
    return first unassigned variable when iterating assignments
    dictionary or None if all are assigned

    TODO: instead of random, pick most contrained variable, 
    i.e. variable that has fewest legal values
    '''
    for key, value in self.assignments.items():
      if value == None:
        return key
    return None
  
  def get_legal_value(self, variable):
    '''
    remove last legal value in list of legal values and 
    return it or None if no posible value for variable

    TODO: instead of random, pick least constraining value
    '''
    if self.variable_to_legal_values[variable]:
      return self.variable_to_legal_values[variable].pop()
    else:
      return None

  def constraint_is_satisfied(self):
    '''
    return true if current assignment breaks any of complete 
    binary constraints, return false otherwise

    TODO: implement binary_constraints as generator
    '''
    for var1, var2 in self.binary_contraints:
      if self.assignments[var1] and self.assignments[var2] and \
        not self.constraint_function(
          self.assignments[var1], self.assignments[var2]
        ):
        return False
    return True
  
  def do_forward_chaining(self, variable, value):
    '''
    remove values from legal values in self.variable_to_legal_values 
    that break constraint after assignment specified in argument

    TODO: implement above 
    '''
    pass
  
class Fitness:
  '''
  TODO: this class will have functions to order assignments
  of course to class based on preference.

  prefernce include morning/evening class, tight/spread schedule
  '''
  pass