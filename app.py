from flask import Flask, jsonify, request, Response, abort
from database.db import initialize_db
from database.models import Professor, ResearchGroup, Student
import json
from bson.objectid import ObjectId
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {    
    'host':'mongodb://mongo:27017/flask-db'    
}

db = initialize_db(app)

@app.route('/')
def get_route():
    output = {'message': 'Hello there!'}
    return output, 200

#Doneded! get professors by designation!
@app.route('/listProfessors', methods=['GET'])
def list_professors():
  designation = request.args.get('designation')

  professors = None
  if designation is None:
    professors = Professor.objects()
  else:
    professors = Professor.objects(designation=designation)
  
  res = list(map(lambda p: { 'name' : p.name, 'email': p.email, 'designation': p.designation}, professors))  
  return Response(json.dumps(res), mimetype="application/json", status=200)

# Read	GET	/listProfessor/{prof_id}	–	
# Single database object 
# { name: name, eamil: email, designation: designation, interests: [interests] } - Status Code: 200
@app.route('/listProfessor/<prof_id>')
def get_professor(prof_id):

  professors = None

  try:
    professors = Professor.objects(id=prof_id)    
  except:
    app.logger.info("catching error")
    return abort(404)
  

  if len(professors) == 0:
    return abort(404)

  p = professors[0]


  res = {
    "name": p.name,
    "email": p.email,
    "designation": p.designation,
    "interests": p.interests
  }

  app.logger.info("professor %s", res)
  return Response(json.dumps(res), mimetype="application/json", status=200)


# OK!

# Single database object 
# { name: name, studentNumber: studentNumber, researchGroups: [group_id] } - Status Code: 200

@app.route('/listStudent/<student_id>', methods=['GET'])
def get_student_by_id(student_id):
  students = None

  try:
    students = Student.objects(id=student_id)    
  except:
    app.logger.info("catching error")
    return abort(404)
  

  if len(students) == 0:
    return abort(404)

  s = students[0]


  res = {
    "name": s.name,
    "studentNumber": s.studentNumber,    
    "researchGroups": s.researchGroups
  }

  return Response(json.dumps(res), mimetype="application/json", status=200)
    

# OK!

# Get Read	GET	/listGroup/{group_id}	–	
# Single database object { id: group_id, name: name, founder: prof_id } - Status Code: 200
@app.route('/listGroup/<group_id>', methods=['GET'])
def get_group_by_id(group_id):
  groups = None

  try:
    groups = ResearchGroup.objects(id=group_id)    
  except:    
    return abort(404)
  
  if len(groups) == 0:
    return abort(404)

  g = groups[0]

  res = {
    #"id": g.name,
    name: g.name    
  }  
  return Response(json.dumps(res), mimetype="application/json", status=200)



@app.route('/testing/student/<name>')
def create_stud(name):
  student = {
    "name": name,
    "studentNumber": "abcdef",
    "researchGroups": []
  }

  s = Student(**student).save()
  id = s.id
  return {'id': str(id)}, 200

@app.route('/testing/<name>')
def testing(name):
    body = {
      'name': name,
      'designation': 'Professor',
      'email': 'pro@email.com'
    }

    professor = Professor(**body).save()
    id = professor.id

    r = ResearchGroup(**{
      'name': 'jokfgj',
      'description': 'dkfhjdfd',
      'founder': professor
    }).save()
    Professor.objects(id=id).update(researchGroups=[r])
    return {'id': str(id)}, 200

@app.route('/testing/professors')
def testing2():
  professors = Professor.objects().to_json()  
  return Response(professors, mimetype="application/json", status=200)

@app.route('/testing/research')
def testing3():
  groups = ResearchGroup.objects().to_json()  
  return Response(groups, mimetype="application/json", status=200)