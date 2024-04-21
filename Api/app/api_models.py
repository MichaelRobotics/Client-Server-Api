from flask_restx import fields 

from .extensions import api

course_model = api.model("Robot", {
    "id": fields.Integer,
    "IP": fields.String,
    "name": fields.String,
})

course_input_model = api.model("RobotInput", {
    "IP": fields.String,
    "name": fields.String
})
