from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Lista de tarefas (simulação de banco de dados)
tasks = [
    {"id": 1, "name": "Comprar leite", "completed": False},
    {"id": 2, "name": "Estudar Flask", "completed": False}
]

# Rota inicial - Exibe as tarefas pendentes e concluídas
@app.route('/')
def index():
    pending_tasks = [task for task in tasks if not task['completed']]
    completed_tasks = [task for task in tasks if task['completed']]
    return render_template('index.html', pending_tasks=pending_tasks, completed_tasks=completed_tasks)

# Rota para obter todas as tarefas via API (tanto pendentes quanto concluídas)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

# Rota para adicionar uma tarefa
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()  # Pega os dados como JSON
    task_name = data.get('task')
    
    if task_name:
        new_task = {"id": len(tasks) + 1, "name": task_name, "completed": False}
        tasks.append(new_task)
        return jsonify({"tasks": tasks}), 201  # Retorna as tarefas após adicionar
    else:
        return jsonify({"message": "Task name is required"}), 400

# Rota para editar uma tarefa
@app.route('/edit_task/<int:task_id>', methods=['PUT'])  # Usando PUT para editar
def edit_task(task_id):
    data = request.get_json()  # Pega os dados como JSON
    new_name = data.get('task')
    
    if new_name:
        for task in tasks:
            if task['id'] == task_id:
                task['name'] = new_name
                return jsonify({"tasks": tasks})
        return jsonify({"message": "Task not found"}), 404
    else:
        return jsonify({"message": "Task name is required"}), 400

# Rota para deletar uma tarefa
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])  # Usando DELETE para deletar
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"tasks": tasks})

# Rota para concluir uma tarefa
@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            break
    return jsonify({"tasks": tasks})

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
