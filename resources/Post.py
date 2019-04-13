from flask import jsonify, request
from flask_restful import Resource
from Model import db, Post, Category, PostSchema

posts_schema = PostSchema(many=True)
post_schema = PostSchema()

class PostResource(Resource):
    def get(self):
        posts = Post.query.all()
        posts = posts_schema.dump(posts).data
        return {"status":"success", "data":posts}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = post_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        category_id = Category.query.filter_by(id=data['category_id']).first()
        if not category_id:
            return {'status': 'error', 'message': 'post category not found'}, 400
        post = Post(
            category_id=data['category_id'], 
            title=data['title'],
            description=data['description']
            )
        db.session.add(post)
        db.session.commit()

        result = post_schema.dump(post).data

        return {'status': "success", 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = post_schema.load(json_data)
        if errors:
            return errors, 422
        post = Post.query.filter_by(id=data['id']).first()
        if not post:
            return {'message': 'Post does not exist'}, 400
        post.name = data['name']
        post.description = data['description']
        post.category_id = data['category_id']
        db.session.commit()

        result = post_schema.dump(post).data

        return { "status": 'success', 'data': result }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = post_schema.load(json_data)
        if errors:
            return errors, 422
        post = Post.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = post_schema.dump(post).data

        return { "status": 'success', 'data': result}, 204