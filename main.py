from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'  # Specify position of db
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


# db.create_all()  # Create DB/overwrites existing one

# Specify arguments we expect to receive by the PUT method
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

# Specify arguments we expect to receive by the PATCH method
video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument("name", type=str, help="Name of the video")
video_patch_args.add_argument("views", type=int, help="Views of the video")
video_patch_args.add_argument("likes", type=int, help="Likes of the video")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)  # Takes the unserialized instance and serializes it
    def get(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()  # Unserialized instance

        # Check if query is valid
        if not video:
            abort(404, message=f"Video with id {video_id} does not exist")
        return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()

        # Check if video exists already
        video = VideoModel.query.filter_by(id=video_id).first()
        if video:
            abort(409, message=f"Video with id {video_id} already exists")

        video = VideoModel(id=video_id, name=args["name"], views=args["views"],
                           likes=args["likes"])  # Creates video objects
        db.session.add(video)  # Adds it to db temporarily
        db.session.commit()  # Commits the change to db permanently
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_patch_args.parse_args()

        video = VideoModel.query.filter_by(id=video_id).first()
        # Check if query is valid
        if not video:
            abort(404, message=f"Video with id {video_id} does not exist")

        if args["name"]:
            video.name = args["name"]
        if args["views"]:
            video.views = args["views"]
        if args["likes"]:
            video.likes = args["likes"]

        db.session.commit()
        return video, 201

    def delete(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        # Check if query is valid
        if not video:
            abort(404, message=f"Video with id {video_id} does not exist")

        db.session.delete(video)
        db.session.commit()
        return "", 204


# URL/Endpoint
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
