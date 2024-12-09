from flask import Flask, request, jsonify, make_response
import uuid
from functools import wraps

app = Flask(__name__)

# In-memory database
books = []
members = []
tokens = {}  # Stores tokens for authentication


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token or token not in tokens:
            return jsonify({'message': 'Authentication token is missing or invalid!'}), 401
        return f(*args, **kwargs)
    return decorated


def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

# Root Route
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Library Management System API'}), 200

# Authentication: Login (Generate Token)
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify', 401)
    
    token = str(uuid.uuid4())
    tokens[token] = auth.get('username')  # Store the token
    return jsonify({'token': token})

# CRUD Operations for Books
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    book = request.json
    book['id'] = str(uuid.uuid4())  # Unique ID for each book
    books.append(book)
    return jsonify({'message': 'Book added successfully', 'book': book}), 201

@app.route('/books', methods=['GET'])
@token_required
def get_books():
    title = request.args.get('title')
    author = request.args.get('author')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    filtered_books = books
    if title:
        filtered_books = [b for b in books if title.lower() in b.get('title', '').lower()]
    if author:
        filtered_books = [b for b in filtered_books if author.lower() in b.get('author', '').lower()]
    
    paginated_books = paginate(filtered_books, page, per_page)
    return jsonify({'books': paginated_books, 'total': len(filtered_books)}), 200

@app.route('/books/<string:book_id>', methods=['GET'])
@token_required
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'book': book}), 200

@app.route('/books/<string:book_id>', methods=['PUT'])
@token_required
def update_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    updates = request.json
    book.update(updates)
    return jsonify({'message': 'Book updated successfully', 'book': book}), 200

@app.route('/books/<string:book_id>', methods=['DELETE'])
@token_required
def delete_book(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return jsonify({'message': 'Book deleted successfully'}), 200

# CRUD Operations for Members
@app.route('/members', methods=['POST'])
@token_required
def add_member():
    member = request.json
    member['id'] = str(uuid.uuid4())  # Unique ID for each member
    members.append(member)
    return jsonify({'message': 'Member added successfully', 'member': member}), 201

@app.route('/members', methods=['GET'])
@token_required
def get_members():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    paginated_members = paginate(members, page, per_page)
    return jsonify({'members': paginated_members, 'total': len(members)}), 200

@app.route('/members/<string:member_id>', methods=['GET'])
@token_required
def get_member(member_id):
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    return jsonify({'member': member}), 200

@app.route('/members/<string:member_id>', methods=['PUT'])
@token_required
def update_member(member_id):
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    updates = request.json
    member.update(updates)
    return jsonify({'message': 'Member updated successfully', 'member': member}), 200

@app.route('/members/<string:member_id>', methods=['DELETE'])
@token_required
def delete_member(member_id):
    global members
    members = [m for m in members if m['id'] != member_id]
    return jsonify({'message': 'Member deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)


