from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'  # Chave secreta para sessões
login_manager = LoginManager()
login_manager.init_app(app)

# Lista simulada de usuários (em produção, use um banco de dados)
users = [
    {"id": 1, "email": "user@example.com", "username": "user1", "password": generate_password_hash("password123")},
]

# Lista de tarefas (simulação de banco de dados)
tasks = [
    {"id": 1, "name": "Comprar leite", "completed": False},
    {"id": 2, "name": "Estudar Flask", "completed": False}
]

# Classe de usuário (UserMixin facilita a integração com Flask-Login)
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data["id"]
        self.email = user_data["email"]
        self.username = user_data["username"]
        self.password = user_data["password"]

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    user = next((user for user in users if user["id"] == int(user_id)), None)
    return User(user) if user else None

# Rota de Login (GET) - Exibe o formulário de login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Rota de Login (POST) - Processa o login
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')  # Mudança: utilizando .json para Postman
    password = request.json.get('password')

    # Validações de entrada
    if not email or not password:
        return jsonify({"message": "Email e senha são necessários"}), 400

    user = next((user for user in users if user["email"] == email), None)

    if user and check_password_hash(user["password"], password):
        user_obj = User(user)
        login_user(user_obj)
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401

# Rota de Logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido!"}), 200

# Rota inicial - Exibe as tarefas pendentes e concluídas
@app.route('/')
@login_required  # Garantir que o usuário esteja logado
def index():
    pending_tasks = [task for task in tasks if not task['completed']]
    completed_tasks = [task for task in tasks if task['completed']]
    return render_template('index.html', pending_tasks=pending_tasks, completed_tasks=completed_tasks)

# Rota para obter todas as tarefas via API (tanto pendentes quanto concluídas)
@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    return jsonify({"tasks": tasks})

# Rota para obter uma tarefa específica via API
@app.route('/task/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({"message": "Task not found"}), 404
# Rota para adicionar uma tarefa
@app.route('/add_task', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"tasks": tasks})

# Rota para concluir uma tarefa
@app.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            break
    return jsonify({"tasks": tasks})

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
