from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Show all posts"""
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Handle the addition of a new blog post"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    errors = {}
    title = data.get("title")
    content = data.get("content")

    if not title:
        errors["title"] = "Title is required."
    if not content:
        errors["content"] = "Content is required."
    if errors:
        return jsonify({"errors": errors}), 400


    new_id = max((post["id"] for post in POSTS), default=0) + 1
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
