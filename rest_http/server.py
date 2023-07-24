
import time, os 
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (you can replace this with your own data or database)
tasks = [
    {"id": 1, "title": "Task 1", "description": "Description for Task 1", "done": False},
    {"id": 2, "title": "Task 2", "description": "Description for Task 2", "done": False},
    {"id": 3, "title": "Task 3", "description": "Description for Task 3", "done": False},
    {"id": 4, "title": "Task 4", "description": "Description for Task 4", "done": False},
    {"id": 5, "title": "Task 5", "description": "Description for Task 5", "done": False},
]


# Endpoint to get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Endpoint to add a new task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid JSON data"}), 400

        new_task = {
            "id": data.get("id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "done": data.get("done", False)
        }

        tasks.append(new_task)
        return jsonify({"message": "Task added successfully", "task": new_task}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Endpoint to mark a task as completed
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    #if task["done"]:
    #    return jsonify({"message": "Task is already completed"}), 400

    # Simulate completion by adding a delay of 2 seconds (you can replace this with actual task completion logic)
    time.sleep(5)

    task["done"] = True
    return jsonify({"message": "Task marked as completed", "task": task}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
