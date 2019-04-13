from flask_restful import Resource

class Hello(Resource):
	def get(self):
		return {'message': 'hello world'}

	def post(self):
		return {'message': 'hello world'}

