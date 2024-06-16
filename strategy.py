
# Strategy Pattern:

# The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.
# Strategy lets the algorithm vary independently from clients that use it.



# Links to specific articles on the Strategy pattern:
# https://www.tutorialspoint.com/design_pattern/strategy_pattern.htm
# https://sourcemaking.com/design_patterns/strategy
# https://refactoring.guru/design-patterns/strategy


class Person:
  def __init__(self, lastName,  age, married):
    self.lastName = lastName
    self.age = age
    self.married = married

  def getLastName(self):
    return self.lastName
  
  def getAge(self):
    return self.age

  def isMarried(self):
    return self.married


class PersonFilter:
  def apply(self, person):
    pass
  
class AdultFilter(PersonFilter):
  def apply(self, person):
    return person.getAge() >= 18

class SeniorFilter(PersonFilter):
  def apply(self, person):
    return person.getAge() >= 65
  
class MarriedFilter(PersonFilter):
  def apply(self, person):
    return person.isMarried()

class PeopleCount:
  def __init__(self):
    self.filter: PersonFilter = None
  
  def setFilter(self,filter):
    self.filter = filter
  
  def count(self, people):
    count = 0
    for person in people:
      if self.filter.apply(person):
        count+=1
    return count

    
  