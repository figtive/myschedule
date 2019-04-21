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
    self.saved_states = []
  
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
      self.pop_variable_to_legal_values_state()
      return
    variable = self.get_unassigned_variable()
    while(True):
      value = self.get_legal_value(variable)
      self.push_variable_to_legal_values_state()
      if value == None:
        self.assignments[variable] = None
        self.pop_variable_to_legal_values_state()
        self.variable_to_legal_values = self.pop_variable_to_legal_values_state()
        break
      self.assignments[variable] = value
      self.do_forward_check(variable)
      if self.constraint_is_satisfied():
        self.get_solution_helper()
      else:
        self.assignments[variable] = None
  
  def pop_variable_to_legal_values_state(self):
    return self.saved_states.pop() if len(self.saved_states) > 0 else None
  
  def push_variable_to_legal_values_state(self):
    self.saved_states.append(copy.deepcopy(self.variable_to_legal_values))

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
    return most constrained unassigned variable
    '''

    sort_by_least_legal_value = sorted(
      [(variable, values) for variable, values in self.variable_to_legal_values.items() 
          if self.assignments[variable] == None], 
      key=lambda e: len(e[1])
    )
    
    return sort_by_least_legal_value[0][0] if len(sort_by_least_legal_value) > 0 else None

  def get_legal_value(self, variable):
    '''
    remove last legal value in list of legal values and 
    return it or None if no posible value for variable
    '''
    if variable == None:
      return None
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
  
  def do_forward_check(self, assigned_variable):
    '''
    remove values from legal values in self.variable_to_legal_values 
    that break constraint after variable in argument is assigned
    '''
    for other_variable in self.variable_to_legal_values:
      # if unassigned and not same variable
      if self.assignments[other_variable] == None and other_variable != assigned_variable:
        for value_to_be_checked in self.variable_to_legal_values[other_variable]:
          # if break constraint
          if not self.constraint_function(self.assignments[assigned_variable], value_to_be_checked):
            self.variable_to_legal_values[other_variable].remove(value_to_be_checked)
  
class Fitness:
  '''
  TODO: this class will have functions to order assignments
  of course to class based on preference.

  prefernce include morning/evening class, tight/spread schedule
  '''
  pass