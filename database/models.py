from .db import db

class Professor(db.Document):
    designations = ['Professor', 'Assistant Professor', 'Associate Professor']

    name = db.StringField(required=True)
    designation = db.StringField(required=True, choises=designations)
    email = db.StringField()
    interests = db.ListField(db.StringField())
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))


class ResearchGroup(db.Document):    
    name = db.StringField(required=True)
    description = db.StringField()
    founder = db.ReferenceField('Professor', required = True)    

class Student(db.Document):
    name = db.StringField(required=True)
    studentNumber = db.StringField(required=True)
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))
    
