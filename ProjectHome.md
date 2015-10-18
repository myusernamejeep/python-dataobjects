Library with a lot of unit test to help creation of Entities and ValueObjects in Python with easy validation, inspired by sintax of GORM of Groovy.

Class Entity and ValueObject extends DataObject class. The DataObject class has a common implementation of str and ValueObject has an common implementation of eq and ne methods.

Class OrderedValueObject extends ValueObject and implement lt, le, gt and ge methods with easy customization.

This project is independent of database or web-frameworks stuff, like most of programs of validation. So you can use it in Scripts/GUI/Console/WebApplications programs without necessity of adaptation and configuration files. It is also extensible and easy to register new constraints for validation.

# Example of usage: #

## Entity ##

```
  from domain import dataobjects
  
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
```

Now run:

```
  example = MyEntity()
  print(example)
  print(example.valid())
  print(example.hasErrors())
  print(example.errors))
```

## ValueObject ##

```
  from domain import dataobjects

  class MyValueObject(dataObject.ValueObject):
    def __init__(self, somevariable, anothervariable):
      self.somevariable = somevariable
      self.anothervariable = anothervariable
      
    def equalsVariables(self):
      return ['somevariable']
  
  MyValueObject.addConstraints('somevariable', Nullable = False, Min = 3)
  MyValueObject.addConstraints('anothervariable', Nullable = False, Max = 4)
```

Now run:

```
  print(MyValueObject(3, 4))
  print(MyValueObject(3, 4) == MyValueObject(3, 4)) # True
  print(MyValueObject(3, 4) == MyValueObject(4, 4)) # False
  print(MyValueObject(3, 4) == MyValueObject(3, 5)) # True
  print(MyValueObject(3, 4).valid()) # True
  print(MyValueObject(2, 5).valid()) # False
```

## OrderedValueObject ##

```
  from domain import dataobjects

  class MyValueObject(dataObject.ValueObject):

    def __init__(self, vara, varb, varc):
      self.vara = vara
      self.varb = varb
      self.varc = varc
      
    # Override this method is optional: Default order is lexicographical of the variable names
    def priorityOrder(self):
      return ['varb', 'vara']
  
  MyValueObject.addConstraints('vara', Nullable = False, Min = 3)
  MyValueObject.addConstraints('varb', Nullable = False, Min = 3)
```

Now run:

```
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
```

PS1: Unorderable variables are ignored.

PS2: Variables thar are not in priorityOrder methods are ignores.

# Adding a new constraint #

Min refer to MinConstraint class, Matches refer to MatchesConstraint class, and so on.

To register a new constraint, follow:

```
from domain import validator

class MyConstraint(validator.Constraint):
  def valid(self):
    return True # bool value

  def message(self): return 'some text that can link the follow variables:self.attributeName, self.value, self.requiredValue'

MyConstraint.load()
```

Now, it is possible to do this:

```
MyEntity.addConstraints('somevariable', My = SomeRequiredValueHere)
```

# General #

  * Implemented with Python 3.0

  * Dependencies:
    * Distutils