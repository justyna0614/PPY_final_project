from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'done': False
    }
]


# Get all taskas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return tasks


# Run the flask app
if __name__ == '__main__':
    app.run(debug=True)