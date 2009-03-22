'''
Created on Mar 8, 2009

@author: Paulo Cheque (paulocheque@agilbits.com.br)
'''

from domain import validator

class DataObject(object):
  '''
  An data object with useful methods for validation
  
  Example of usage:
  
  import dataObject
  
  class MyEntity(dataObject.Entity):
    
    def __init__(self):
      self.someint = 1
      self.somefloat = 1.23
      self.somestring = 'abc'
      self.somelist = [1, 2]
      self.somedict = {1:1, 2:2}
      self.sometuple = (1, 2)
      
  MyEntity.addConstraints('someint', Nullable = False, Min = 3, Max = 4, InList = [1, 2], Custom = lambda x: x == 1)
  MyEntity.addConstraints('somefloat', Nullable = False, Min = 3, Max = 4, Scale = 4, InList = [1.0, 2.0], Custom = lambda x: x == 1.0)
  MyEntity.addConstraints('somestring', Nullable = False, Min = 3, Max = 4, InList = ['a', 'b'], Matches = '[0-9]', Email = True, IP = True, Site = True, Custom = lambda x: x == 'a')
  MyEntity.addConstraints('somelist', Nullable = False, Min = 3, Max = 4, InList = [[1, 2]], Custom = lambda x: x == [1, 2])
  MyEntity.addConstraints('somedict', Nullable = False, Min = 3, Max = 4, InList = [{1:1, 2:2], Custom = lambda x: x == {1:1, 2:2})
  MyEntity.addConstraints('sometuple', Nullable = False, Min = 3, Max = 4, InList = [(1, 2)], Custom = lambda x: x == (1, 2))
  
  class MyValueObject(dataObject.ValueObject):

    def __init__(self, somevariable):
      self.somevariable = somevariable
  
  MyValueObject.addConstraints('somevariable', Nullable = False, Min = 3)    
  
  # Now, run:
  
  example = MyEntity()
  print(example.valid())
  print(example.hasErrors())
  print(example.errors))
  
  print(MyValueObject(3) == MyValueObject(3))
  print(MyValueObject(3) == MyValueObject(4))
  print(MyValueObject(2).valid())
  print(MyValueObject(3).valid())
  '''
  
  constraints = {}

  @classmethod
  def addConstraints(clazz, attributeName, **attrConstraints):
    parentClass = clazz.__mro__[1]
    if id(parentClass.constraints) == id(clazz.constraints):
      clazz.constraints = {}
      clazz.constraints.update(parentClass.constraints)
    clazz.constraints[attributeName] = attrConstraints

  def __getValue(self, attributeName):
    try:
      return eval('self.' + attributeName)
    except AttributeError:
      raise validator.ConstraintException('Constraint error: Invalid attribute')

  def __validateInnerDataObject(self, var):
    eval('self.' + var + '.validate()')
    innerErrors = eval('self.' + var + '.errors()')
    self.__currentErrors.extend(innerErrors)

  def validate(self):
    self.__currentErrors = []
    for attributeName in self.constraints:
      value = self.__getValue(attributeName)
      if issubclass(value.__class__, DataObject):
        self.__validateInnerDataObject(attributeName)
      for constraintName in self.constraints[attributeName]:
        requiredValue = self.constraints[attributeName][constraintName]
        constraint = validator.ConstraintFactory.getConstraint(constraintName, attributeName, requiredValue, value)
        if not constraint.valid():
          self.__currentErrors.append(constraint.message())

  def errors(self):
    self.validate()
    return self.__currentErrors
  
  def valid(self):
    return len(self.errors()) == 0

  def hasErrors(self):
    return not self.valid()
  
  def __str__(self):
    string = self.__class__.__name__
    variables = sorted(vars(self))
    if len(variables) == 0: return string
    string += ': '
    for var in variables:
      string += (var + '=(' + str(eval('self.' + var)) + '), ')
    return string[0:len(string)-2]

class ValueObject(DataObject): 
  '''
  Value Objects don't have an identifier, they are equal by your properties.
  '''
  def __eq__(self, that):
    if isinstance(that, self.__class__):
      return vars(self) == vars(that)
    return False
  
  def __ne__(self, that):
    return not self.__eq__(that)

class Entity(DataObject): 
  '''
  Entity has an identifier, 
  '''
#  In the future, this class could have an id property and __eq__ __ne__ methods based
#  on id property
#  def __init__(self, id=None):
#    self.id = id
  pass
