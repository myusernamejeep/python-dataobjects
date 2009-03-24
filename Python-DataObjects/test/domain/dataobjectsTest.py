'''
Created on Mar 8, 2009

@author: Paulo Cheque (paulocheque@agilbits.com.br)

TODO entity list?
'''

import unittest
import datetime
from domain.validator import *
from domain.dataobjects import *

class DataObjectTest(unittest.TestCase):
  
  def testEntityWithoutConstraintsIsValidAndHasNoErrors(self):
    class MyEntity(Entity): pass
    self.assertEquals(True, MyEntity().valid())
    self.assertEquals(False, MyEntity().hasErrors())
    self.assertEquals([], MyEntity().errors())
    
  def testValueObjectWithoutConstraintsIsValidAndHasNoErrors(self):
    class MyValueObject(ValueObject): pass
    self.assertEquals(True, MyValueObject().valid())
    self.assertEquals(False, MyValueObject().hasErrors())
    self.assertEquals([], MyValueObject().errors())
    
  def testEntityWithNonDefaultConstructorWithoutConstraintsIsValidAndHasNoErrors(self):
    class MyEntity(Entity):
      def __init__(self):
        self.somevar = 1
    self.assertEquals(True, MyEntity().valid())
    self.assertEquals(False, MyEntity().hasErrors())
    self.assertEquals([], MyEntity().errors())


class DataObjectAddConstraintTest(unittest.TestCase):

  def testEachDataObjectHasItsContraints(self):
    class MyEntity(Entity): 
      def __init__(self): self.somevalidvariable = 1
    class MyAnotherEntity(Entity):
      def __init__(self): self.somevalidvariable = 1
    self.assertEquals(id(Entity.constraints), id(MyEntity.constraints))
    self.assertEquals(id(Entity.constraints), id(MyAnotherEntity.constraints))
    
    MyEntity.addConstraints('somevalidvariable')
    self.assertNotEquals(id(Entity.constraints), id(MyEntity.constraints))
    self.assertEquals(id(Entity.constraints), id(MyAnotherEntity.constraints))
    
    MyAnotherEntity.addConstraints('somevalidvariable')
    self.assertNotEquals(id(Entity.constraints), id(MyEntity.constraints))
    self.assertNotEquals(id(Entity.constraints), id(MyAnotherEntity.constraints))
    self.assertNotEquals(id(MyEntity.constraints), id(MyAnotherEntity.constraints))
    
  def testEachDataObjectHasItsContraintsEvenForInheritance(self):
    class MyEntity(Entity): 
      def __init__(self): self.somevalidvariable = 1
    class MyAnotherEntity(MyEntity):
      def __init__(self): self.someanothervalidvariable = 1
    self.assertEquals(id(Entity.constraints), id(MyEntity.constraints))
    self.assertEquals(id(Entity.constraints), id(MyAnotherEntity.constraints))
    MyEntity.addConstraints('somevalidvariable')
    MyAnotherEntity.addConstraints('someanothervalidvariable')
    self.assertEquals(1, len(MyEntity.constraints))
    self.assertEquals(2, len(MyAnotherEntity.constraints))
    self.assertNotEquals(id(MyEntity.constraints), id(MyAnotherEntity.constraints))
    
  
  def testDataObjectAddConstraintForInstanceVariable(self):
    class MyDO(DataObject):
      def __init__(self): self.somevariable = 10
    MyDO.addConstraints('somevariable')
    self.assertNotEquals(None, MyDO.constraints['somevariable'])
    
  def testDataObjectAddConstraintForClassVariable(self):
    class MyDO(DataObject): somevariable = 10
    MyDO.addConstraints('somevariable')
    self.assertNotEquals(None, MyDO.constraints['somevariable'])
    
  def testDataObjectAddConstraintForAnEntityWithoutDefaultConstructor(self):
    class MyDO(DataObject): 
      def __init__(self, somevariable): self.somevariable = somevariable
    MyDO.addConstraints('somevariable')
    self.assertNotEquals(None, MyDO.constraints['somevariable'])
    
    
    
  def testDataObjectWithOneConstraintAndValidDataMustBeValid(self):
    class MyDO(DataObject):
      def __init__(self): self.someint = 10
    MyDO.addConstraints('someint', Min = 5)
    do = MyDO()
    self.assertEquals(True, do.valid())
    self.assertEquals(False, do.hasErrors())
    self.assertEquals([], do.errors())
    
  def testDataObjectWithOneConstraintAndValidDataMustBeValid(self):
    class MyDO(DataObject):
      def __init__(self): self.someint = 4
    MyDO.addConstraints('someint', Min = 5)
    do = MyDO()
    self.assertEquals(False, do.valid())
    self.assertEquals(True, do.hasErrors())
    self.assertEquals(['someint (= 4) must be greater or equal than 5'], do.errors())
    
  def testDataObjectWithOneListOfConstraintsAndValidDataMustBeValid(self):
    class MyDO(DataObject):
      def __init__(self): self.someint = 10
    MyDO.addConstraints('someint', Min = 5, Max = 15)
    do = MyDO()
    self.assertEquals(True, do.valid())
    self.assertEquals(False, do.hasErrors())
    self.assertEquals([], do.errors())
    
  def testDataObjectWithOneListOfConstraintsWithOneValidDateAndOneInvalidDataMustBeInvalid(self):
    class MyDO(DataObject):
      def __init__(self): self.somestring = 'paulocheque@gmail.com'
    MyDO.addConstraints('somestring', Email = True, Site = True)
    do = MyDO()
    self.assertEquals(False, do.valid())
    self.assertEquals(True, do.hasErrors())
    self.assertEquals(['somestring (= paulocheque@gmail.com) must be a valid site address'], do.errors())
    
  def testDataObjectWithOneListOfConstraintsWithTwoInvalidDataMustBeInvalid(self):
    class MyDO(DataObject):
      def __init__(self): self.somestring = 'xxx'
    MyDO.addConstraints('somestring', Email = True, Site = True)
    do = MyDO()
    self.assertEquals(False, do.valid())
    self.assertEquals(True, do.hasErrors())
    self.assertEquals('somestring (= xxx) must be a valid e-mail address', do.errors()[0])
    self.assertEquals('somestring (= xxx) must be a valid site address', do.errors()[1])
    
  def testDataObjectWithTwoListOfConstraintsAndValidDataMustBeValid(self):
    class MyDO(DataObject):
      def __init__(self):
        self.someint = 3
        self.somestring = 'abc'
    MyDO.addConstraints('someint', Min = 1, Max = 3)
    MyDO.addConstraints('somestring', Min = 1, Max = 5, Matches = '[a]+.+')
    do = MyDO()
    self.assertEquals(True, do.valid())
    self.assertEquals(False, do.hasErrors())
    self.assertEquals([], do.errors())
    
  def testDataObjectWithTwoListOfConstraintsAndOneInvalidDataMustBeInvalid(self):
    class MyDO(DataObject):
      def __init__(self):
        self.somefloat = 1.23
        self.somelist = [1, 2, 3]
    MyDO.addConstraints('somefloat', Min = 1, Scale = 2)
    MyDO.addConstraints('somelist', Min = 1, Max = 2)
    do = MyDO()
    self.assertEquals(False, do.valid())
    self.assertEquals(True, do.hasErrors())
    self.assertEquals(['somelist (= [1, 2, 3]) must have length lower or equal than 2'], do.errors())
    
  def testDataObjectWithTwoListOfConstraintsAndInvalidDataMustBeInvalid(self):
    class MyDO(DataObject):
      def __init__(self):
        self.somefloat = 1.23
        self.somedict = {1:1, 2:2, 3:3}
    MyDO.addConstraints('somefloat', Min = 1, Scale = 1)
    MyDO.addConstraints('somedict', Min = 1, Max = 2)
    do = MyDO()
    self.assertEquals(False, do.valid())
    self.assertEquals(True, do.hasErrors())
    self.assertEquals('somefloat (= 1.23) must have 1 decimals or less', do.errors()[1])
    self.assertEquals('somedict (= {1: 1, 2: 2, 3: 3}) must have length lower or equal than 2', do.errors()[0])
    
  def testConstraintOfInexistentVariableMustRaiseAConstraintException(self):
    class MyDO(DataObject): pass
    MyDO.addConstraints('someconstraint', Min = 1)
    try:
      MyDO().validate()
    except ConstraintException: pass
    else: self.fail()

  
  def testFullValidExample(self):
    class FullEntity(Entity):
      
      def __init__(self):
        self.someint = 1
        self.somefloat = 1.23
        self.somestring = 'abc'
        self.someemail = 'abc@abc.com'
        self.somesite = 'http://www.google.com'
        self.someip = '127.0.0.1'
        self.somelist = [1, 2]
        self.somedict = {1:1, 2:2}
        self.sometuple = (1, 2)
    FullEntity.addConstraints('someint', Min = 1, Max = 1, InList = [1], Custom = lambda x: x == 1)
    FullEntity.addConstraints('somefloat', Min = 1, Max = 2, InList = [1.23], Custom = lambda x: x == 1.23, Scale = 2)
    FullEntity.addConstraints('somestring', Min = 3, Max = 3, InList = ['abc'], Matches = 'abc', Custom = lambda x: x == 'abc')
    FullEntity.addConstraints('someemail', Email = True)
    FullEntity.addConstraints('somesite', Site = True)
    FullEntity.addConstraints('someip', IP = True)
    FullEntity.addConstraints('somelist', Min = 2, Max = 2, InList = [[1, 2]], Custom = lambda x: x == [1, 2])
    FullEntity.addConstraints('somedict', Min = 2, Max = 2, InList = [{1:1, 2:2}])
    FullEntity.addConstraints('sometuple', Min = 2, Max = 2, InList = [(1, 2)])
    fullEntity = FullEntity()
    self.assertEquals(True, fullEntity.valid())
    self.assertEquals(False, fullEntity.hasErrors())
    self.assertEquals([], fullEntity.errors())
    
  def testFullInvalidExample(self):
    class FullEntity(Entity):
      
      def __init__(self):
        self.someint = 1
        self.somefloat = 1.23
        self.somestring = 'abc'
        self.someemail = 'xxx'
        self.somesite = 'xxx'
        self.someip = 'xxx'
        self.somelist = [1, 2]
        self.somedict = {1:1, 2:2}
        self.sometuple = (1, 2)
    FullEntity.addConstraints('someint', Min = 2, Max = 0, InList = [2], Custom = lambda x: x == 2)
    FullEntity.addConstraints('somefloat', Min = 2, Max = 1, InList = [1.34], Custom = lambda x: x == 1.34, Scale = 1)
    FullEntity.addConstraints('somestring', Min = 4, Max = 2, InList = ['abcd'], Matches = 'abcd', Custom = lambda x: x == 'abcd')
    FullEntity.addConstraints('someemail', Email = True)
    FullEntity.addConstraints('somesite', Site = True)
    FullEntity.addConstraints('someip', IP = True)
    FullEntity.addConstraints('somelist', Min = 3, Max = 1, InList = [[1, 2, 3]], Custom = lambda x: x == [1, 2, 3])
    FullEntity.addConstraints('somedict', Min = 3, Max = 1, InList = [{1:1, 2:2, 3:3}])
    FullEntity.addConstraints('sometuple', Min = 3, Max = 1, InList = [(1, 2, 3)])
    fullEntity = FullEntity()
    self.assertEquals(False, fullEntity.valid())
    self.assertEquals(True, fullEntity.hasErrors())
    self.assertEquals(27, len(fullEntity.errors())) # 27 constraints

  def testValidatorMustRunRecursively(self):
    class InnerEntity(Entity):
      def __init__(self, name):
        self.name = name
    InnerEntity.addConstraints('name', Max = 2)
    class OuterEntity(Entity): 
      def __init__(self, inner):
        self.inner = inner
    OuterEntity.addConstraints('inner')
    
    outer = OuterEntity(InnerEntity('xx'))
    outer.validate()
    self.assertEquals(True, outer.valid())
    self.assertEquals(False, outer.hasErrors())
    self.assertEquals([], outer.errors())
    outer = OuterEntity(InnerEntity('xxx'))
    outer.validate()
    self.assertEquals(False, outer.valid())
    self.assertEquals(True, outer.hasErrors())
    self.assertEquals(['name (= xxx) must have length lower or equal than 2'], outer.errors())
    
  def testValidatorMustRunRecursivelyAndMustRunInnerConstraints(self):
    class InnerEntity(Entity):
      def __init__(self, name):
        self.name = name
    InnerEntity.addConstraints('name', Max = 2)
    class OuterEntity(Entity): 
      def __init__(self, inner):
        self.inner = inner
    OuterEntity.addConstraints('inner', Nullable = False)
    
    outer = OuterEntity(InnerEntity('xx'))
    outer.validate()
    self.assertEquals(True, outer.valid())
    self.assertEquals(False, outer.hasErrors())
    self.assertEquals([], outer.errors())
    outer = OuterEntity(None)
    outer.validate()
    self.assertEquals(False, outer.valid())
    self.assertEquals(True, outer.hasErrors())
    self.assertEquals(['inner (= None) must be different of None'], outer.errors())
    
  def testTwoLevelsOfRecursive(self):
    class InnestEntity(Entity):
      def __init__(self, name):
        self.name = name
    InnestEntity.addConstraints('name', Max = 2)
    class InnerEntity(Entity):
      def __init__(self, innest):
        self.innest = innest
    InnerEntity.addConstraints('innest')
    class OuterEntity(Entity): 
      def __init__(self, inner):
        self.inner = inner
    OuterEntity.addConstraints('inner')
    
    outer = OuterEntity(InnerEntity(InnestEntity('xx')))
    outer.validate()
    self.assertEquals(True, outer.valid())
    self.assertEquals(False, outer.hasErrors())
    self.assertEquals([], outer.errors())
    outer = OuterEntity(InnerEntity(InnestEntity('xxx')))
    outer.validate()
    self.assertEquals(False, outer.valid())
    self.assertEquals(True, outer.hasErrors())
    self.assertEquals(['name (= xxx) must have length lower or equal than 2'], outer.errors())
    InnerEntity.addConstraints('innest', Nullable = False)
    outer = OuterEntity(InnerEntity(None))
    outer.validate()
    self.assertEquals(False, outer.valid())
    self.assertEquals(True, outer.hasErrors())
    self.assertEquals(['innest (= None) must be different of None'], outer.errors())
    
    
  def testCycleDependencyMustNotGenerateAnInfiniteLoop(self):
    class A(Entity):
      def __init__(self):
        self.b = None
    class B(Entity): 
      def __init__(self):
        self.a = None
    a = A()
    b = B()
    a.b = b
    b.a = a
    a.validate()
    self.assertEquals(True, a.valid())
    self.assertEquals(False, a.hasErrors())
    self.assertEquals([], a.errors())
    b.validate()
    self.assertEquals(True, b.valid())
    self.assertEquals(False, b.hasErrors())
    self.assertEquals([], b.errors())
   
  def testInheritanceDerivedMustCallValidationOfBaseClass(self):
    class BaseClass(Entity):
      def __init__(self, base):
        self.base = base
    BaseClass.addConstraints('base', Min = 3)
    class DerivedClass(BaseClass): 
      def __init__(self, base):
        super(DerivedClass, self).__init__(base)
        self.derived = 3
    DerivedClass.addConstraints('derived', Min = 3)
    derived = DerivedClass(3)
    derived.validate()
    self.assertEquals(True, derived.valid())
    self.assertEquals(False, derived.hasErrors())
    self.assertEquals([], derived.errors())
    derived = DerivedClass(2)
    derived.validate()
    self.assertEquals(False, derived.valid())
    self.assertEquals(True, derived.hasErrors())
    self.assertEquals(['base (= 2) must be greater or equal than 3'], derived.errors())

class DataObjectToStringTest(unittest.TestCase):

  def testToStringWithoutAttributes(self):
    class MyDO(DataObject): pass
    self.assertEquals('MyDO', str(MyDO()))
    
  def testToStringWithOneAttribute(self):
    class MyDO(DataObject):
      def __init__(self, x):
        self.x = x
    self.assertEquals('MyDO: x=(5)', str(MyDO(5)))
    
  def testToStringWithVariousAttributes(self):
    class MyDO(DataObject):
      def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    self.assertEquals('MyDO: x=(5), y=(6), z=(7)', str(MyDO(5, 6, 7)))
    
  def testToStringWithInnerDO(self):
    class MyInnerDO(DataObject):
      def __init__(self, x):
        self.x = x
    class MyDO(DataObject):
      def __init__(self, x, inner):
        self.x = x
        self.inner = inner
    self.assertEquals('MyDO: inner=(MyInnerDO: x=(6)), x=(5)', str(MyDO(5, MyInnerDO(6))))

class ValueObjectTest(unittest.TestCase):
  
  def testEqualAndNotEqualWithoutAttributes(self):
    class MyVO(ValueObject): pass
    class MyAnotherVO(ValueObject): pass
    self.assertTrue(MyVO() == MyVO())
    self.assertFalse(MyVO() != MyVO())
    self.assertFalse(MyVO() == MyAnotherVO())
    self.assertTrue(MyVO() != MyAnotherVO())
    
  def testEqualAndNotEqualWithOneAttribute(self):
    class MyVO(ValueObject):
      def __init__(self, x):
        self.x = x
    class MyAnotherVO(ValueObject):
      def __init__(self, x):
        self.x = x
    self.assertTrue(MyVO(1) == MyVO(1))
    self.assertTrue(MyVO(1) != MyVO(2))
    self.assertFalse(MyVO(1) == MyAnotherVO(1))
    self.assertTrue(MyVO(1) != MyAnotherVO(2))
    
  def testEqualAndNotEqualWithALotOfAttributes(self):
    class MyVO(ValueObject):
      a = 3
      def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    self.assertTrue(MyVO(x=1, y=2, z=3) == MyVO(z=3, y=2, x=1))
    self.assertTrue(MyVO(1, 3, 2) != MyVO(1, 2, 3))
    
  def testEqualsAndNotEqualsWithExplicitVariables(self):
    class MyVO(ValueObject):
      a = 3
      def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
      def equalsVariables(self):
        return ['x', 'y']
    self.assertTrue(MyVO(1, 2, 3) == MyVO(1, 2, 3))
    self.assertTrue(MyVO(1, 2, 3) == MyVO(1, 2, 4))
    self.assertTrue(MyVO(1, 2, 3) != MyVO(1, 3, 3))
    self.assertTrue(MyVO(1, 2, 3) != MyVO(2, 2, 3))
    
  def testEqualsAndNotEqualsWithEmptyExplicitVariables(self):
    class MyVO(ValueObject):
      def __init__(self, x):
        self.x = x
      def equalsVariables(self):
        return []
    self.assertTrue(MyVO(1) == MyVO(2))
    
  def testEqualsAndNotEqualsWithExplicitVariablesThatDontExistRaiseAnException(self):
    class MyVO(ValueObject):
      def __init__(self, x):
        self.x = x
      def equalsVariables(self):
        return ['y']
    try:
      self.assertTrue(MyVO(1, 2, 3) == MyVO(1, 2, 3))
    except: pass
    else: self.fail()
    
  def atestEqualAndNotEqualWithCycleDependency(self):
    # FIXME bug, how? Use equalsVariables
    class MyVO1(ValueObject):
      def __init__(self):
        self.vo = MyVO2()
    class MyVO2(ValueObject):
      def __init__(self):
        self.vo = MyVO1()
    self.assertEquals(MyVO1(), MyVO1())
    self.assertEquals(MyVO2(), MyVO2())
    
class OrderedValueObjectTest(unittest.TestCase):
    
  def testVOWithoutAttributs(self):
    class MyVO(OrderedValueObject):
      pass
    self.assertFalse(MyVO() < MyVO())
    self.assertTrue(MyVO() <= MyVO())
    self.assertFalse(MyVO() > MyVO())
    self.assertTrue(MyVO() >= MyVO())
    
  def testVOWithOneNumberAttribute(self):
    class MyVO(OrderedValueObject):
      def __init__(self, value):
        self.value = value
    self.assertTrue(MyVO(1) < MyVO(2))
    self.assertFalse(MyVO(2) < MyVO(2))
    self.assertFalse(MyVO(2) < MyVO(1))
    
    self.assertTrue(MyVO(1) <= MyVO(2))
    self.assertTrue(MyVO(2) <= MyVO(2))
    self.assertFalse(MyVO(2) <= MyVO(1))
    
    self.assertFalse(MyVO(1) > MyVO(2))
    self.assertFalse(MyVO(2) > MyVO(2))
    self.assertTrue(MyVO(2) > MyVO(1))
    
    self.assertFalse(MyVO(1) >= MyVO(2))
    self.assertTrue(MyVO(2) >= MyVO(2))
    self.assertTrue(MyVO(2) >= MyVO(1))
    
  def testVOWithOneStringAttributeMustBeTheLexicographicalOrder(self):
    class MyVO(OrderedValueObject):
      def __init__(self, value):
        self.value = value
    self.assertTrue(MyVO('aa') < MyVO('ab'))
    self.assertFalse(MyVO('ab') < MyVO('ab'))
    self.assertFalse(MyVO('ab') < MyVO('aa'))
    
    self.assertTrue(MyVO('aa') <= MyVO('ab'))
    self.assertTrue(MyVO('ab') <= MyVO('ab'))
    self.assertFalse(MyVO('ab') <= MyVO('aa'))
    
    self.assertFalse(MyVO('aa') > MyVO('ab'))
    self.assertFalse(MyVO('ab') > MyVO('ab'))
    self.assertTrue(MyVO('ab') > MyVO('aa'))
    
    self.assertFalse(MyVO('aa') >= MyVO('ab'))
    self.assertTrue(MyVO('ab') >= MyVO('ab'))
    self.assertTrue(MyVO('ab') >= MyVO('aa'))
    
  def testVOWithTwoAttributeMustBeOrderByLexicographicalOrderOfVariableNames(self):
    class MyVO(OrderedValueObject):
      def __init__(self, valuea, valueb):
        self.valuea = valuea
        self.valueb = valueb
    self.assertTrue(MyVO(1, 'aa') < MyVO(2, 'ab'))
    self.assertTrue(MyVO(1, 'aa') < MyVO(2, 'aa'))
    self.assertTrue(MyVO(1, 'aa') < MyVO(1, 'ab'))
    self.assertFalse(MyVO(2, 'aa') < MyVO(2, 'aa'))
    self.assertFalse(MyVO(2, 'ab') < MyVO(1, 'aa'))
    self.assertFalse(MyVO(2, 'aa') < MyVO(1, 'aa'))
    self.assertFalse(MyVO(1, 'ab') < MyVO(1, 'aa'))
    
    self.assertTrue(MyVO(1, 'aa') <= MyVO(2, 'ab'))
    self.assertTrue(MyVO(1, 'aa') <= MyVO(2, 'aa'))
    self.assertTrue(MyVO(1, 'aa') <= MyVO(1, 'ab'))
    self.assertTrue(MyVO(2, 'aa') <= MyVO(2, 'aa'))
    self.assertFalse(MyVO(2, 'ab') <= MyVO(1, 'aa'))
    self.assertFalse(MyVO(2, 'aa') <= MyVO(1, 'aa'))
    self.assertFalse(MyVO(1, 'ab') <= MyVO(1, 'aa'))
    
    self.assertFalse(MyVO(1, 'aa') > MyVO(2, 'ab'))
    self.assertFalse(MyVO(1, 'aa') > MyVO(2, 'aa'))
    self.assertFalse(MyVO(1, 'aa') > MyVO(1, 'ab'))
    self.assertFalse(MyVO(2, 'aa') > MyVO(2, 'aa'))
    self.assertTrue(MyVO(2, 'ab') > MyVO(1, 'aa'))
    self.assertTrue(MyVO(2, 'aa') > MyVO(1, 'aa'))
    self.assertTrue(MyVO(1, 'ab') > MyVO(1, 'aa'))
    
    self.assertFalse(MyVO(1, 'aa') >= MyVO(2, 'ab'))
    self.assertFalse(MyVO(1, 'aa') >= MyVO(2, 'aa'))
    self.assertFalse(MyVO(1, 'aa') >= MyVO(1, 'ab'))
    self.assertTrue(MyVO(2, 'aa') >= MyVO(2, 'aa'))
    self.assertTrue(MyVO(2, 'ab') >= MyVO(1, 'aa'))
    self.assertTrue(MyVO(2, 'aa') >= MyVO(1, 'aa'))
    self.assertTrue(MyVO(1, 'ab') >= MyVO(1, 'aa'))
    
  def testVOMustBeOrderByDefinedPriorityOrder(self):
    class MyVO(OrderedValueObject):
      def __init__(self, valuea, valueb):
        self.valuea = valuea
        self.valueb = valueb
      def priorityOrder(self):
        return ['valueb', 'valuea']
    self.assertTrue(MyVO(1, 'aa') < MyVO(2, 'ab'))
    self.assertTrue(MyVO(1, 'aa') < MyVO(2, 'aa'))
    self.assertTrue(MyVO(1, 'aa') < MyVO(1, 'ab'))
    self.assertFalse(MyVO(2, 'aa') < MyVO(2, 'aa'))
    self.assertFalse(MyVO(2, 'ab') < MyVO(1, 'aa'))
    self.assertFalse(MyVO(2, 'aa') < MyVO(1, 'aa'))
    self.assertFalse(MyVO(1, 'ab') < MyVO(1, 'aa'))
    self.assertFalse(MyVO(1, 'ab') < MyVO(2, 'aa'))
    self.assertTrue(MyVO(2, 'aa') < MyVO(1, 'ab'))
    
    self.assertTrue(MyVO(1, 'aa') <= MyVO(2, 'ab'))
    self.assertTrue(MyVO(1, 'aa') <= MyVO(2, 'aa'))
    self.assertTrue(MyVO(1, 'aa') <= MyVO(1, 'ab'))
    self.assertTrue(MyVO(2, 'aa') <= MyVO(2, 'aa'))
    self.assertFalse(MyVO(2, 'ab') <= MyVO(1, 'aa'))
    self.assertFalse(MyVO(2, 'aa') <= MyVO(1, 'aa'))
    self.assertFalse(MyVO(1, 'ab') <= MyVO(1, 'aa'))
    self.assertFalse(MyVO(1, 'ab') <= MyVO(2, 'aa'))
    self.assertTrue(MyVO(2, 'aa') <= MyVO(1, 'ab'))
    
    self.assertFalse(MyVO(1, 'aa') > MyVO(2, 'ab'))
    self.assertFalse(MyVO(1, 'aa') > MyVO(2, 'aa'))
    self.assertFalse(MyVO(1, 'aa') > MyVO(1, 'ab'))
    self.assertFalse(MyVO(2, 'aa') > MyVO(2, 'aa'))
    self.assertTrue(MyVO(2, 'ab') > MyVO(1, 'aa'))
    self.assertTrue(MyVO(2, 'aa') > MyVO(1, 'aa'))
    self.assertTrue(MyVO(1, 'ab') > MyVO(1, 'aa'))
    self.assertTrue(MyVO(1, 'ab') > MyVO(2, 'aa'))
    self.assertFalse(MyVO(2, 'aa') > MyVO(1, 'ab'))
    
    self.assertFalse(MyVO(1, 'aa') >= MyVO(2, 'ab'))
    self.assertFalse(MyVO(1, 'aa') >= MyVO(2, 'aa'))
    self.assertFalse(MyVO(1, 'aa') >= MyVO(1, 'ab'))
    self.assertTrue(MyVO(2, 'aa') >= MyVO(2, 'aa'))
    self.assertTrue(MyVO(2, 'ab') >= MyVO(1, 'aa'))
    self.assertTrue(MyVO(2, 'aa') >= MyVO(1, 'aa'))
    self.assertTrue(MyVO(1, 'ab') >= MyVO(1, 'aa'))
    self.assertTrue(MyVO(1, 'ab') >= MyVO(2, 'aa'))
    self.assertFalse(MyVO(2, 'aa') >= MyVO(1, 'ab'))
    
  def testVOWithOptionalArgumentMustIgnoreThatToOrder(self):
      class MyVO(OrderedValueObject):
        def __init__(self, valuea, valueb):
          self.valuea = valuea
          self.valueb = valueb
        def priorityOrder(self):
          return ['valuea']
      self.assertTrue(MyVO(1, 'aa') < MyVO(2, 'ab'))
      self.assertTrue(MyVO(1, 'aa') < MyVO(2, 'aa'))
      self.assertFalse(MyVO(1, 'aa') < MyVO(1, 'ab'))
      self.assertFalse(MyVO(2, 'aa') < MyVO(2, 'aa'))
      self.assertFalse(MyVO(2, 'ab') < MyVO(1, 'aa'))
      self.assertFalse(MyVO(2, 'aa') < MyVO(1, 'aa'))
      self.assertFalse(MyVO(1, 'ab') < MyVO(1, 'aa'))
      self.assertTrue(MyVO(1, 'ab') < MyVO(2, 'aa'))
      self.assertFalse(MyVO(2, 'aa') < MyVO(1, 'ab'))
      
      self.assertTrue(MyVO(1, 'aa') <= MyVO(2, 'ab'))
      self.assertTrue(MyVO(1, 'aa') <= MyVO(2, 'aa'))
      self.assertTrue(MyVO(1, 'aa') <= MyVO(1, 'ab'))
      self.assertTrue(MyVO(2, 'aa') <= MyVO(2, 'aa'))
      self.assertFalse(MyVO(2, 'ab') <= MyVO(1, 'aa'))
      self.assertFalse(MyVO(2, 'aa') <= MyVO(1, 'aa'))
      self.assertTrue(MyVO(1, 'ab') <= MyVO(1, 'aa'))
      self.assertTrue(MyVO(1, 'ab') <= MyVO(2, 'aa'))
      self.assertFalse(MyVO(2, 'aa') <= MyVO(1, 'ab'))
      
      self.assertFalse(MyVO(1, 'aa') > MyVO(2, 'ab'))
      self.assertFalse(MyVO(1, 'aa') > MyVO(2, 'aa'))
      self.assertFalse(MyVO(1, 'aa') > MyVO(1, 'ab'))
      self.assertFalse(MyVO(2, 'aa') > MyVO(2, 'aa'))
      self.assertTrue(MyVO(2, 'ab') > MyVO(1, 'aa'))
      self.assertTrue(MyVO(2, 'aa') > MyVO(1, 'aa'))
      self.assertFalse(MyVO(1, 'ab') > MyVO(1, 'aa'))
      self.assertFalse(MyVO(1, 'ab') > MyVO(2, 'aa'))
      self.assertTrue(MyVO(2, 'aa') > MyVO(1, 'ab'))
      
      self.assertFalse(MyVO(1, 'aa') >= MyVO(2, 'ab'))
      self.assertFalse(MyVO(1, 'aa') >= MyVO(2, 'aa'))
      self.assertTrue(MyVO(1, 'aa') >= MyVO(1, 'ab'))
      self.assertTrue(MyVO(2, 'aa') >= MyVO(2, 'aa'))
      self.assertTrue(MyVO(2, 'ab') >= MyVO(1, 'aa'))
      self.assertTrue(MyVO(2, 'aa') >= MyVO(1, 'aa'))
      self.assertTrue(MyVO(1, 'ab') >= MyVO(1, 'aa'))
      self.assertFalse(MyVO(1, 'ab') >= MyVO(2, 'aa'))
      self.assertTrue(MyVO(2, 'aa') >= MyVO(1, 'ab'))
  
  def testOrderIgnoreUnorderedAttributes(self):
    class MyVO(OrderedValueObject):
      def __init__(self, orderedattr, unorderedattr):
        self.orderedattr = orderedattr
        self.unorderedattr = unorderedattr
    self.assertFalse(MyVO(3, {4:4}) < MyVO(2, {3:3}))
    self.assertFalse(MyVO(3, {4:4}) <= MyVO(2, {3:3}))
    self.assertTrue(MyVO(3, {3:3}) > MyVO(2, {4:4}))
    self.assertTrue(MyVO(3, {3:3}) >= MyVO(2, {4:4}))
    self.assertTrue(MyVO(2, {3:3}) >= MyVO(2, {4:4}))
    self.assertTrue(MyVO(2, {3:3}) <= MyVO(2, {4:4}))
    self.assertFalse(MyVO(2, {3:3}) > MyVO(2, {4:4}))
    self.assertFalse(MyVO(2, {3:3}) < MyVO(2, {4:4}))
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()