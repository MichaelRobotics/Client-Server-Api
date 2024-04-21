from flask_restx import Namespace, Resource

from .api_models import course_model, course_input_model
from .models import Robot
from .extensions import db

ns = Namespace("api")

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "world"}
    
@ns.route("/courses")
class CourseListAPI(Resource):

    @ns.marshal_list_with(course_model)
    def get(self):
        return Robot.query.all()
    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def post(self):
        print(ns.payload)
        course = Robot(name=ns.payload["name"], IP=ns.payload["IP"])
        db.session.add(course)
        db.session.commit()
        return course, 201

@ns.route("/courses/<name>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, name):
        return Robot.query.filter_by(name=name).first()

    
    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, name):
        course = Robot.query.filter_by(name=name).first()
        course.name = ns.payload["name"]
        course.IP = ns.payload["IP"]
        db.session.commit()
        return course, 200
    
    def delete(self, name):
        course = Robot.query.filter_by(name=name).first()
        db.session.delete(course)
        db.session.commit()
        return "", 204
