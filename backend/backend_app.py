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
    """Show all posts, optionally sorted by title or content"""
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    valid_sort_fields = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field '{sort_field}'. Must be 'title' or 'content'."}), 400

    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction '{direction}'. Must be 'asc' or 'desc'."}), 400

    if sort_field:
        reverse = (direction == 'desc')
        sorted_posts = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=reverse)
        return jsonify(sorted_posts), 200

    return jsonify(POSTS), 200


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


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post by ID"""
    post_to_delete = next((post for post in POSTS if post["id"] == post_id), None)

    if not post_to_delete:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post by ID, the title and content are optional for update"""
    post_to_update = next((post for post in POSTS if post["id"] == post_id), None)

    if not post_to_update:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided."}), 400

    title = data.get("title", post_to_update["title"])
    content = data.get("content", post_to_update["content"])

    post_to_update["title"] = title
    post_to_update["content"] = content

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for posts by title or content using query parameters"""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    matched_posts = [
        post for post in POSTS
        if (title_query in post["title"].lower() if title_query else True)
        and (content_query in post["content"].lower() if content_query else True)
    ]

    return jsonify(matched_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
