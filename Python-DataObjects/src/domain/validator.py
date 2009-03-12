'''
Created on Mar 8, 2009

@author: Paulo Cheque (paulocheque@agilbits.com.br)

To register a new constraint, follow:

from domain import validator

class MyConstraint(validator.Constraint):
  def valid(self):
    return True # bool value

  def message(self): return 'some text (self.attributeName, self.value, self.requiredValue)'
  
MyConstraint.load()

Now, it is possible to do this:

MyEntity.addConstraints('somevariable', My = True)
'''

import re
from string import Template

class ConstraintException(Exception):
  '''
  Exception that raises when validation fail
  '''
  
  def __init__(self, value):
    '''
    value: message of this exception
    '''
    self.value = value
    
  def __str__(self):
    return repr(self.value)


class Constraint(object):
  '''
  Constraint is an abstract class
  To implement a constraint, just extend this class and implement 
  the methods valid (return a bool) and message (return a string)
  '''
  
  def __init__(self, attributeName, requiredValue, value):
    self.attributeName = attributeName
    self.requiredValue = requiredValue
    self.value = value
  
  @classmethod
  def load(clazz):
    '''
    Just a method to facilitate the developers work. 
    Cycle dependency but it is ok for a good reason.
    '''
    ConstraintFactory.addConstraint(clazz)

  @classmethod
  def getName(clazz):
    return clazz.__name__.replace('Constraint', '')
  
  def valid(self): pass
  
  def message(self): pass
  
class ConstraintFactory(object):
  
  constraintsRules = []
  
  def addConstraint(constraintClass):
    if not issubclass(constraintClass, Constraint):
      raise ConstraintException('Invalid Constraint, please, extend Constraint class') 
    ConstraintFactory.constraintsRules.append(constraintClass.getName())
  addConstraint = staticmethod(addConstraint)
  
  def getConstraint(name, attributeName, requiredValue, value):
    if name in ConstraintFactory.constraintsRules:
#      FIXME need to get the module name
#      return eval('from domain import validatorTest')
      return eval(name + 'Constraint(attributeName, requiredValue, value)')
    else:
      raise ConstraintException('Constraint ' + name + 'Constraint not registered')
  getConstraint = staticmethod(getConstraint)
  
class MinConstraint(Constraint):
  
  def valid(self):
    if self.value is None: return False
    if isinstance(self.value, (str, list, dict, tuple)):
      return len(self.value) >= self.requiredValue
    return self.value >= self.requiredValue
  
  def message(self):
    if isinstance(self.value, (str, list, dict, tuple)):
      t = Template('$attr (= $value) must have length greater or equal than $required')
    else:
      t = Template('$attr (= $value) must be greater or equal than $required')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)
  
MinConstraint.load()
  
class MaxConstraint(Constraint):
  
  def valid(self):
    if self.value is None: return False
    if isinstance(self.value, (str, list, dict, tuple)):
      return len(self.value) <= self.requiredValue
    return self.value <= self.requiredValue
  
  def message(self):
    if isinstance(self.value, (str, list, dict, tuple)):
      t = Template('$attr (= $value) must have length lower or equal than $required')
    else:
      t = Template('$attr (= $value) must be lower or equal than $required')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)
  
MaxConstraint.load()
  
class NullableConstraint(Constraint):
  
  def valid(self):
    if self.requiredValue: return True
    else: return self.value is not None
    
  def message(self):
    t = Template('$attr (= $value) must be different of None')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)
  
NullableConstraint.load()
    
class MatchesConstraint(Constraint):

  def valid(self):
    if not isinstance(self.value, str): return False
    return re.match(self.requiredValue, self.value) is not None
  
  def message(self):
    t = Template('$attr (= $value) must matches $required')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

MatchesConstraint.load()

class InListConstraint(Constraint):

  def valid(self):
    return self.value in self.requiredValue
  
  def message(self):
    t = Template('$attr (= $value) must be in list $required')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)
  
InListConstraint.load()

class ScaleConstraint(Constraint):

  def valid(self):
    if not isinstance(self.value, float): return False
    return len(re.sub('[0-9][.]', '', str(self.value))) <= self.requiredValue
  
  def message(self):
    t = Template('$attr (= $value) must have $required decimals or less')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

ScaleConstraint.load()

class EmailConstraint(MatchesConstraint):

  def valid(self):
    '''
    TODO need better regular expression
    '''
    if not self.requiredValue: return True
    if not isinstance(self.value, str): return False
    matches = MatchesConstraint(self.attributeName, '^.+[@].+[.].{1,4}$', self.value)
    return matches.valid()

  def message(self):
    t = Template('$attr (= $value) must be a valid e-mail address')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

EmailConstraint.load()

class IPConstraint(MatchesConstraint):

  def valid(self):
    if not self.requiredValue: return True
    if not isinstance(self.value, str): return False
    matches = MatchesConstraint(
      self.attributeName, 
      '^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[.]){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]){1}$', 
      self.value)
    return matches.valid()
    
  def message(self):
    t = Template('$attr (= $value) must be a valid ip address')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

IPConstraint.load()

class SiteConstraint(MatchesConstraint):

  def valid(self):
    '''
    TODO need better regular expression
    '''
    if not self.requiredValue: return True
    if not isinstance(self.value, str): return False
    matches = MatchesConstraint(self.attributeName, '^(http|https)[:][/][/].+$', self.value)
    return matches.valid()
    
  def message(self):
    t = Template('$attr (= $value) must be a valid site address')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

SiteConstraint.load()
  
class CustomConstraint(MatchesConstraint):

  def valid(self):
    return self.requiredValue(self.value)
  
  def message(self):
    '''
    TODO is it possible to print the lambda function?
    '''
    t = Template('$attr (= $value) must be satisfied by specific function')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

CustomConstraint.load()
