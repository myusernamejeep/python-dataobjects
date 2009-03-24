'''
Created on Mar 8, 2009

@author: Paulo Cheque (paulocheque@agilbits.com.br)
'''

from domain import validator

class DataObject(object):
  '''
  An data object with useful methods for validation
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

class Entity(DataObject): 
  '''
  Ps: Entity generaly has an identifier.
   
  Example of usage:
  
  from domain import dataobjects
  
  class MyEntity(dataobjects.Entity):
    
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
  
  # Now, run:
  
  example = MyEntity()
  print(example)
  print(example.valid())
  print(example.hasErrors())
  print(example.errors))
  '''
  
#  In the future, this class could have an id property and __eq__ __ne__ methods based
#  on id property
#  def __init__(self, id=None):
#    self.id = id
  pass

class ValueObject(DataObject): 
  '''
  Ps: Value Objects don't have an identifier, they are equal by your properties.
  
  Beyond the functionality of Entity, ValueObjects also has:
  
  from domain import dataobjects
  
  class MyValueObject(dataobjects.ValueObject):

    def __init__(self, somevariable, anothervariable):
      self.somevariable = somevariable
      self.anothervariable = anothervariable
      
    def equalsVariables(self):
      return ['somevariable']
  
  MyValueObject.addConstraints('somevariable', Nullable = False, Min = 3)
  MyValueObject.addConstraints('anothervariable', Nullable = False, Max = 4)
  
  # Now, run:
  
  print(MyValueObject(3, 4))
  print(MyValueObject(3, 4) == MyValueObject(3, 4)) # True
  print(MyValueObject(3, 4) == MyValueObject(4, 4)) # False
  print(MyValueObject(3, 4) == MyValueObject(3, 5)) # True
  print(MyValueObject(3, 4).valid()) # True
  print(MyValueObject(2, 5).valid()) # False
  '''
  
  def equalsVariables(self):
    pass
  
  def __eq__(self, that):
    # FIXME: bug with cycle dependency, Example: Player has Team that has lot of Players
    if isinstance(that, self.__class__):
      variables = self.equalsVariables()
      if variables == None:
          return vars(self) == vars(that)
      else:
        for var in variables:
          if vars(self)[var] != vars(that)[var]:
            return False
        return True
    return False
  
  def __ne__(self, that):
    return not self.__eq__(that)

class OrderedValueObject(ValueObject):
  '''
  Beyond the functionality of Entity and ValueObject, OrderedValueObjects also has:
  
  from domain import dataobjects
  
  class MyValueObject(dataobjects.ValueObject):

    def __init__(self, vara, varb, varc):
      self.vara = vara
      self.varb = varb
      self.varc = varc
      
    # Override this method is optional: Default order is lexicographical of the variable names
    def priorityOrder(self):
      return ['varb', 'vara']
  
  MyValueObject.addConstraints('vara', Nullable = False, Min = 3)
  MyValueObject.addConstraints('varb', Nullable = False, Min = 3)
  
  # Now, run:
  
  print(MyOrderedValueObject(3,3,3))
  print(MyOrderedValueObject(3,3,3) == MyOrderedValueObject(3,3,3)) # True
  print(MyOrderedValueObject(3,3,3) == MyOrderedValueObject(4,4,4)) # False
  print(MyOrderedValueObject(2,2,2).valid()) # False
  print(MyOrderedValueObject(3,3,3).valid()) # True
  print(MyOrderedValueObject(3, 3, 3) > MyOrderedValueObject(4, 4, 4)) # False: varb < varb
  print(MyOrderedValueObject(3, 3, 3) < MyOrderedValueObject(4, 4, 4)) # True: varb < varb
  print(MyOrderedValueObject(4, 4, 4) >= MyOrderedValueObject(4, 4, 4)) # True: varb = varb and vara = vara
  print(MyOrderedValueObject(3, 3, 3) <= MyOrderedValueObject(4, 4, 4)) # True: varb < varb
  print(MyOrderedValueObject(30, 4, 30) > MyOrderedValueObject(40, 3, 40)) # True: varb > varb
  print(MyOrderedValueObject(4, 4, 30) > MyOrderedValueObject(3, 4, 40)) # True: varb = varb and vara > vara
  print(MyOrderedValueObject(4, 4, 30) > MyOrderedValueObject(4, 4, 40)) # False: varb = varb and vara = vara, ignoring 30 and 40
  
  PS1: Unorderable variables are ignored.
  PS1: Variables thar are not in priorityOrder methods are ignores.
  '''

  def priorityOrder(self):
    return sorted(vars(self).keys())
  
  def __comparation(self, that, acceptEqual):
    if isinstance(that, self.__class__):
      for var in self.priorityOrder():
        try:
          if vars(self)[var] < vars(that)[var]:
            return True
          if vars(self)[var] > vars(that)[var]:
            return False
        # TODO: create method isorderable()?
        except TypeError: pass
      return acceptEqual
    return False
  
  def __lt__(self, that):
    return self.__comparation(that, False)
  
  def __le__(self, that):
    return self.__comparation(that, True)
  
  def __gt__(self, that):
    return not self.__le__(that)
  
  def __ge__(self, that):
    return not self.__lt__(that)

