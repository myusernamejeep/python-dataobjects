'''
Created on Mar 8, 2009

@author: Paulo Cheque (paulocheque@agilbits.com.br)
'''

import unittest
import datetime
from domain.validator import *
    
class ConstraintFactoryTest(unittest.TestCase):
    
  def testAddConstraintMustAddPrefixToConstraintsList(self):
    class SomeConstraint(Constraint): pass
    ConstraintFactory.addConstraint(SomeConstraint)
    self.assertEquals(True, 'Some' in ConstraintFactory.constraintsRules)
    
  def testAddConstraintMustRaiseAndConstraintExceptionIfNotExtendConstraint(self):
    class SomeConstraint(object): pass
    try:
      ConstraintFactory.addConstraint(SomeConstraint)
    except ConstraintException: pass
    else: self.fail()
    
  def testGetConstraint(self):
    class SomeConstraint(Constraint):
      def __init__(self):
        self.a = None
    ConstraintFactory.addConstraint(SomeConstraint)
    self.assertEquals(SomeConstraint, ConstraintFactory.getConstraint('Some', 'a', None, None).__class__)
    
  def testGetConstraintRaiseAConstraintExceptionIfNotRegistered(self):
    try:
      constraint = ConstraintFactory.getConstraint('not registered constraint', '', '', '')
    except ConstraintException: pass
    else: self.fail()
    

class ConstraintTest(unittest.TestCase):
  
  def testConstraintHasAttributeNameAndRequiredValueAndValue(self):
    class MyConstraint(Constraint): pass
    my = MyConstraint('attributeName', 'requiredValue', 'value')
    self.assertEquals('attributeName', my.attributeName)
    self.assertEquals('requiredValue', my.requiredValue)
    self.assertEquals('value', my.value)
    
  def testConstraintNameMustBeTheClassNameWithoutConstraintTerm(self):
    class SomeConstraint(Constraint): pass
    self.assertEquals('Some', SomeConstraint.getName())
    class AnotherConstraint(Constraint): pass
    self.assertEquals('Another', AnotherConstraint.getName())

'''
Base Constraints Test
'''
    
class MinConstraintTest(unittest.TestCase):
  
  def testValidMustReturnTrueIfValueIsGreaterOrEqualThanRequiredValue(self):
    self.assertEquals(True, MinConstraint('attr', 2, 3).valid())
    self.assertEquals(True, MinConstraint('attr', 5, 5).valid())
    
  def testValidMustReturnFalseIfValueIsLowerThanRequiredValue(self):
    self.assertEquals(False, MinConstraint('attr', 3, 2).valid())
    
  def testValidMustReturnTrueIfLengthOfStringIsGreaterOrEqualThanRequiredValue(self):
    self.assertEquals(True, MinConstraint('attr', 2, 'abc').valid())
    self.assertEquals(True, MinConstraint('attr', 3, 'abc').valid())
    
  def testValidMustReturnFalseIfLengthOfStringIsLowerThanRequiredValue(self):
    self.assertEquals(False, MinConstraint('attr', 4, 'abc').valid())
    
  def testValidMustReturnTrueIfDateIsGreaterOrEqualThanRequiredValue(self):
    self.assertEquals(True, MinConstraint('attr', datetime.date(1999, 12, 31), datetime.date(2000, 12, 31)).valid())
    self.assertEquals(True, MinConstraint('attr', datetime.date(2000, 12, 30), datetime.date(2000, 12, 31)).valid())
    self.assertEquals(True, MinConstraint('attr', datetime.date(2000, 11, 11), datetime.date(2000, 11, 12)).valid())
    self.assertEquals(True, MinConstraint('attr', datetime.date(2009, 12, 31), datetime.date(2009, 12, 31)).valid())
    
  def testValidMustReturnFalseIfDateIsLowerThanRequiredValue(self):
    self.assertEquals(False, MinConstraint('attr', datetime.date(2000, 12, 31), datetime.date(1999, 12, 31)).valid())
    self.assertEquals(False, MinConstraint('attr', datetime.date(2000, 12, 31), datetime.date(2000, 12, 30)).valid())
    self.assertEquals(False, MinConstraint('attr', datetime.date(2000, 11, 12), datetime.date(2000, 11, 11)).valid())

  def testValidMustReturnTrueIfSizeOfTupleIsGreaterOrEqualThanRequiredValue(self):
    self.assertEquals(True, MinConstraint('attr', 2, (1, 2, 3)).valid())
    self.assertEquals(True, MinConstraint('attr', 5, (1, 2, 3, 4, 5)).valid())
    
  def testValidMustReturnFalseIfSizeOfTupleIsLowerThanRequiredValue(self):
    self.assertEquals(False, MinConstraint('attr', 3, (1, 2)).valid())
    
  def testValidMustReturnTrueIfSizeOfListIsGreaterOrEqualThanRequiredValue(self):
    self.assertEquals(True, MinConstraint('attr', 2, [1, 2, 3]).valid())
    self.assertEquals(True, MinConstraint('attr', 5, [1, 2, 3, 4, 5]).valid())
    
  def testValidMustReturnFalseIfSizeOfListIsLowerThanRequiredValue(self):
    self.assertEquals(False, MinConstraint('attr', 3, [1, 2]).valid())
    
  def testValidMustReturnTrueIfSizeOfDictIsGreaterOrEqualThanRequiredValue(self):
    self.assertEquals(True, MinConstraint('attr', 2, {1:1, 2:2, 3:3}).valid())
    self.assertEquals(True, MinConstraint('attr', 5, {1:1, 2:2, 3:3, 4:4, 5:5}).valid())
    
  def testValidMustReturnFalseIfSizeOfDictIsLowerThanRequiredValue(self):
    self.assertEquals(False, MinConstraint('attr', 3, {1:1, 2:2}).valid())
    
  def testNoneValue(self):
    self.assertEquals(False, MinConstraint('attr', 3, None).valid())
  
  def testMessage(self):
    self.assertEquals('VariableName (= 2) must be greater or equal than 3', 
                    MinConstraint('VariableName', 3, 2).message())
    self.assertEquals('VariableName (= [1, 2]) must have length greater or equal than 3', 
                    MinConstraint('VariableName', 3, [1, 2]).message())
    
class MaxConstraintTest(unittest.TestCase):
  
  def testValidMustReturnTrueIfValueIsLowerOrEqualThanRequiredValue(self):
    self.assertEquals(True, MaxConstraint('attr', 3, 2).valid())
    self.assertEquals(True, MaxConstraint('attr', 5, 5).valid())
    
  def testValidMustReturnFalseIfValueIsGreaterThanRequiredValue(self):
    self.assertEquals(False, MaxConstraint('attr', 2, 3).valid())
    
  def testValidMustReturnTrueIfLengthOfStringIsLowerOrEqualThanRequiredValue(self):
    self.assertEquals(True, MaxConstraint('attr', 2, 'a').valid())
    self.assertEquals(True, MaxConstraint('attr', 3, 'abc').valid())
    
  def testValidMustReturnFalseIfLengthOfStringIsGreaterThanRequiredValue(self):
    self.assertEquals(False, MaxConstraint('attr', 4, 'abcde').valid())
    
  def testValidMustReturnTrueIfDateIsLowerOrEqualThanRequiredValue(self):
    self.assertEquals(True, MaxConstraint('attr', datetime.date(2000, 12, 31), datetime.date(1999, 12, 31)).valid())
    self.assertEquals(True, MaxConstraint('attr', datetime.date(2000, 12, 31), datetime.date(2000, 12, 30)).valid())
    self.assertEquals(True, MaxConstraint('attr', datetime.date(2000, 11, 12), datetime.date(2000, 11, 11)).valid())
    self.assertEquals(True, MaxConstraint('attr', datetime.date(2009, 12, 31), datetime.date(2009, 12, 31)).valid())
    
  def testValidMustReturnFalseIfDateIsGreaterThanRequiredValue(self):
    self.assertEquals(False, MaxConstraint('attr', datetime.date(1999, 12, 31), datetime.date(2000, 12, 31)).valid())
    self.assertEquals(False, MaxConstraint('attr', datetime.date(2000, 12, 30), datetime.date(2000, 12, 31)).valid())
    self.assertEquals(False, MaxConstraint('attr', datetime.date(2000, 11, 11), datetime.date(2000, 11, 12)).valid())
    
  def testValidMustReturnTrueIfSizeOfListIsLowerOrEqualThanRequiredValue(self):
    self.assertEquals(True, MaxConstraint('attr', 4, (1, 2, 3)).valid())
    self.assertEquals(True, MaxConstraint('attr', 5, (1, 2, 3, 4, 5)).valid())
    
  def testValidMustReturnFalseIfSizeOfListIsGreaterThanRequiredValue(self):
    self.assertEquals(False, MaxConstraint('attr', 1, (1, 2)).valid())
    
  def testValidMustReturnTrueIfSizeOfListIsLowerOrEqualThanRequiredValue(self):
    self.assertEquals(True, MaxConstraint('attr', 4, [1, 2, 3]).valid())
    self.assertEquals(True, MaxConstraint('attr', 5, [1, 2, 3, 4, 5]).valid())
    
  def testValidMustReturnFalseIfSizeOfListIsGreaterThanRequiredValue(self):
    self.assertEquals(False, MaxConstraint('attr', 1, [1, 2]).valid())
    
  def testValidMustReturnTrueIfSizeOfDictIsLowerOrEqualThanRequiredValue(self):
    self.assertEquals(True, MaxConstraint('attr', 4, {1:1, 2:2, 3:3}).valid())
    self.assertEquals(True, MaxConstraint('attr', 5, {1:1, 2:2, 3:3, 4:4, 5:5}).valid())
    
  def testValidMustReturnFalseIfSizeOfDictIsGreaterThanRequiredValue(self):
    self.assertEquals(False, MaxConstraint('attr', 1, {1:1, 2:2}).valid())
    
  def testNoneValue(self):
    self.assertEquals(False, MaxConstraint('attr', 3, None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= 11) must be lower or equal than 10', 
                    MaxConstraint('VariableName', 10, 11).message())
    self.assertEquals('VariableName (= [1, 2]) must have length lower or equal than 1', 
                    MaxConstraint('VariableName', 1, [1, 2]).message())
    
class NullableConstraintTest(unittest.TestCase):
  
  def testValidMustReturnTrueIfValueIsNoneAndAcceptNullable(self):
    self.assertEquals(True, NullableConstraint('attr', True, None).valid())
    
  def testValidMustReturnFalseIfValueIsNoneAndDontAcceptNullable(self):
    self.assertEquals(False, NullableConstraint('attr', False, None).valid())
  
  def testValidMustReturnTrueIfValueIsNotNoneAndAcceptNullable(self):
    self.assertEquals(True, NullableConstraint('attr', True, 0).valid())

  def testValidMustReturnTrueIfValueIsNotNoneAndDontAcceptNullable(self):
    self.assertEquals(True, NullableConstraint('attr', False, 0).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= 2) must be different of None', 
                    NullableConstraint('VariableName', True, 2).message())
    self.assertEquals('VariableName (= None) must be different of None', 
                    NullableConstraint('VariableName', True, None).message())
    
class MatchesConstraintTest(unittest.TestCase):
  
  def testValidMustReturnFalseIsValueIsNotString(self):
    self.assertEquals(False, MatchesConstraint('attr', '.', 1).valid())
  
  def testValidMustReturnTrueIsStringMatchesExpReg(self):
    self.assertEquals(True, MatchesConstraint('attr', '.', 'a').valid())
    
  def testValidMustReturnTrueIsStringDontMatchesExpReg(self):
    self.assertEquals(False, MatchesConstraint('attr', 'a', 'b').valid())
    
  def testNoneValue(self):
    self.assertEquals(False, MatchesConstraint('attr', '.', None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= zzz) must matches [0-9]', 
                    MatchesConstraint('VariableName', '[0-9]', 'zzz').message())
    
class InListConstraintTest(unittest.TestCase):

  def testValidMustReturnFalseIfListIsEmpty(self):
    self.assertEquals(False, InListConstraint('attr', [], 'a').valid())

  def testValidMustReturnTrueIfValueIsInList(self):
    self.assertEquals(True, InListConstraint('attr', ['a'], 'a').valid())
    self.assertEquals(True, InListConstraint('attr', ['a', 'b', 'c'], 'b').valid())
    self.assertEquals(True, InListConstraint('attr', [1, 2, 3], 2).valid())
    
  def testValidMustReturnTrueIfValueIsNotInList(self):
    self.assertEquals(False, InListConstraint('attr', ['a'], 'b').valid())
    self.assertEquals(False, InListConstraint('attr', ['a'], 2).valid())
    
  def testNoneValue(self):
    self.assertEquals(False, InListConstraint('attr', [1], None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= 2) must be in list [1, 2, 3]', 
                    InListConstraint('VariableName', [1, 2, 3], 2).message())
    
class ScaleConstraintTest(unittest.TestCase):
  
  def testValidMustReturnFalseIfValueIsNotFloat(self):
    self.assertEquals(False, ScaleConstraint('attr', 2, 1).valid())
    self.assertEquals(False, ScaleConstraint('attr', 2, 'a').valid())
    
  def testValidMustReturnTrueIfValueHasValidScale(self):
    self.assertEquals(True, ScaleConstraint('attr', 2, 1.00).valid())
    self.assertEquals(True, ScaleConstraint('attr', 2, 1.99).valid())
    self.assertEquals(True, ScaleConstraint('attr', 3, 1.999).valid())
    
  def testValidMustReturnTrueIfValueHasOnlyZerosInDecimalPart(self):
    self.assertEquals(True, ScaleConstraint('attr', 2, 1.00000).valid())
    self.assertEquals(True, ScaleConstraint('attr', 3, 1.00000).valid())
    self.assertEquals(True, ScaleConstraint('attr', 10, 1.00000).valid())
    self.assertEquals(False, ScaleConstraint('attr', 2, 1.00100).valid())
    
  def testValidMustReturnFalseIfValueHasInvalidScale(self):
    self.assertEquals(False, ScaleConstraint('attr', 2, 1.001).valid())
    self.assertEquals(False, ScaleConstraint('attr', 2, 1.999).valid())
    self.assertEquals(False, ScaleConstraint('attr', 3, 1.0005).valid())
    
  def testNoneValue(self):
    self.assertEquals(False, ScaleConstraint('attr', 2, None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= 2.015) must have 3 decimals or less', 
                    ScaleConstraint('VariableName', 3, 2.015).message())
    
class EmailConstraintTest(unittest.TestCase):

  def testValidMustReturnTrueIfNotRequired(self):
    self.assertEquals(True, EmailConstraint('attr', False, 1).valid())
    self.assertEquals(True, EmailConstraint('attr', False, 'a').valid())
    
  def testValidMustReturnFalseIfValueIsNotString(self):
    self.assertEquals(False, EmailConstraint('attr', True, 1).valid())
    
  def testValidMustReturnTrueIfValueIsValidEmail(self):
    self.assertEquals(True, EmailConstraint('attr', True, 'paulocheque@gmail.com').valid())
    self.assertEquals(True, EmailConstraint('attr', True, 'paulocheque@gmail.com.br').valid())

  def testValidMustReturnFalseIfValueIsInvalidEmail(self):
    self.assertEquals(False, EmailConstraint('attr', True, 'paulocheque').valid())
    self.assertEquals(False, EmailConstraint('attr', True, '@gmail.com').valid())
    self.assertEquals(False, EmailConstraint('attr', True, 'paulocheque@gmail').valid())
    
  def testNoneValue(self):
    self.assertEquals(False, EmailConstraint('attr', True, None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= @gmail.com) must be a valid e-mail address', 
                    EmailConstraint('VariableName', 3, '@gmail.com').message())

class IPConstraintTest(unittest.TestCase):
  
  def testValidMustReturnTrueIfNotRequired(self):
    self.assertEquals(True, IPConstraint('attr', False, 1).valid())
    self.assertEquals(True, IPConstraint('attr', False, 'a').valid())

  def testValidMustReturnFalseIfValueIsNotString(self):
    self.assertEquals(False, IPConstraint('attr', True, 1).valid())
    
  def testValidMustReturnTrueIfValueIsValidIP(self):
    self.assertEquals(True, IPConstraint('attr', True, '0.0.0.0').valid())
    self.assertEquals(True, IPConstraint('attr', True, '127.0.0.1').valid())
    self.assertEquals(True, IPConstraint('attr', True, '255.255.255.255').valid())
    
  def testValidMustReturnFalseIfValueIsInvalidIP(self):
    self.assertEquals(False, IPConstraint('attr', True, '-1.0.0.0').valid())
    self.assertEquals(False, IPConstraint('attr', True, '0.0.0.-1').valid())
    self.assertEquals(False, IPConstraint('attr', True, '256.0.0.0').valid())
    self.assertEquals(False, IPConstraint('attr', True, '0.0.0.256').valid())
    self.assertEquals(False, IPConstraint('attr', True, '256.256.256.256').valid())
    self.assertEquals(False, IPConstraint('attr', True, '256.256.256.256.').valid())
    self.assertEquals(False, IPConstraint('attr', True, 'a.a.a.a').valid())
    
  def testNoneValue(self):
    self.assertEquals(False, IPConstraint('attr', 3, None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= 127.0.0.1) must be a valid ip address', 
                    IPConstraint('VariableName', True, '127.0.0.1').message())

class SiteConstraintTest(unittest.TestCase):
  
  def testValidMustReturnTrueIfNotRequired(self):
    self.assertEquals(True, SiteConstraint('attr', False, 1).valid())
    self.assertEquals(True, SiteConstraint('attr', False, 'a').valid())

  def testValidMustReturnFalseIfValueIsNotString(self):
    self.assertEquals(False, SiteConstraint('attr', True, 1).valid())
    
  def testValidMustReturnTrueIfValueIsValidURL(self):
    self.assertEquals(True, SiteConstraint('attr', True, 'http://localhost').valid())
    self.assertEquals(True, SiteConstraint('attr', True, 'https://localhost').valid())
    self.assertEquals(True, SiteConstraint('attr', True, 'http://www.google.com').valid())
    self.assertEquals(True, SiteConstraint('attr', True, 'https://www.google.com.br').valid())
    
  def testValidMustReturnFalseIfValueIsInvalidURL(self):
    self.assertEquals(False, SiteConstraint('attr', True, '').valid())
    self.assertEquals(False, SiteConstraint('attr', True, 'http').valid())
    self.assertEquals(False, SiteConstraint('attr', True, 'http://').valid())
    self.assertEquals(False, SiteConstraint('attr', True, 'localhost').valid())
    
  def testNoneValue(self):
    self.assertEquals(False, SiteConstraint('attr', 3, None).valid())
    
  def testMessage(self):
    self.assertEquals('SomeSite (= http://localhost) must be a valid site address', 
                    SiteConstraint('SomeSite', True, 'http://localhost').message())

class CustomConstraintTest(unittest.TestCase):
  
  def testValidMustReturnTheValidationMadeByTheFuctionParameter(self):
    self.assertEquals(True, CustomConstraint('attr', lambda value: True, 'anything').valid())
    self.assertEquals(True, CustomConstraint('attr', lambda value: True, None).valid())
    self.assertEquals(False, CustomConstraint('attr', lambda value: False, 'anything').valid())
    self.assertEquals(False, CustomConstraint('attr', lambda value: False, None).valid())
    
  def testValidMoreComplexExample(self):
    self.assertEquals(True, CustomConstraint('attr', lambda value: value, True).valid())
    self.assertEquals(False, CustomConstraint('attr', lambda value: value, False).valid())
    self.assertEquals(False, CustomConstraint('attr', lambda value: value == 'x', 'y').valid())
    self.assertEquals(True, CustomConstraint('attr', lambda value: value == 'x', 'x').valid())
    
  def testNoneValue(self):
    self.assertEquals(False, CustomConstraint('attr', lambda x: x == 1, None).valid())
    
  def testMessage(self):
    self.assertEquals('VariableName (= 2) must be satisfied by specific function', 
                    CustomConstraint('VariableName', lambda x: x == True, 2).message())

'''
General tests
'''

class MyConstraint(Constraint):
  def valid(self):
    return True

  def message(self):
    t = Template('$attr (= $value) always returns True (ignoring $required)')
    return t.substitute(attr=self.attributeName, value=self.value, required=self.requiredValue)

class GeneralValidatorTest(unittest.TestCase):

  def testLoadOfBaseConstraints(self):
    constraint = ConstraintFactory.getConstraint('Min', '', '', '')
    self.assertEquals(MinConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Max', '', '', '')
    self.assertEquals(MaxConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Nullable', '', '', '')
    self.assertEquals(NullableConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Scale', '', '', '')
    self.assertEquals(ScaleConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Matches', '', '', '')
    self.assertEquals(MatchesConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Email', '', '', '')
    self.assertEquals(EmailConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('IP', '', '', '')
    self.assertEquals(IPConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Site', '', '', '')
    self.assertEquals(SiteConstraint, constraint.__class__)
    constraint = ConstraintFactory.getConstraint('Custom', '', '', '')
    self.assertEquals(CustomConstraint, constraint.__class__)
    
    
  def testDeveloperCreateYourConstraint(self):
    try:
      constraint = ConstraintFactory.getConstraint('My', '', '', '')
    except ConstraintException: pass
    else: self.fail()
    MyConstraint.load()
    constraint = ConstraintFactory.getConstraint('My', '', '', '')
    self.assertEquals(MyConstraint, constraint.__class__)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()