from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo)

class Person(StructuredNode)
    __primarykey__ = 'name'
    name = StringProperty(unique_index=True)
    passport = StringProperty(unique_index=True)

class Employee(Person):
    pass

class Student(Person):
    pass

class EmployeeStudent(Person):
    pass