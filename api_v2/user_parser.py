from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position')
parser.add_argument('speciality')
parser.add_argument("address")
parser.add_argument("email", required=True)
parser.add_argument("password")
parser.add_argument("id", type=int)
