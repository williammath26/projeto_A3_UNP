from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Configuração do app Flask e banco de dados
app = Flask(__name__)
app.secret_key = 'secret_key'  # Chave secreta para sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tarefas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando extensões
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Modelo para a tabela "users" (apenas para login fixo)
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

# Usuário fixo
user = User(id=1, username='admin', email='admin@example.com', password=generate_password_hash('password123'))

# Modelo para a tabela "tasks"
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    if user.id == int(user_id):
        return user
    return None

# Rota de Login (GET) - Exibe o formulário de login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Validação de entrada
    if not email or not password:
        return jsonify({"message": "Email e senha são necessários"}), 400

    # Verificando os dados do usuário fixo
    if email == user.email:
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login bem-sucedido!"}), 200
        else:
            return jsonify({"message": "Senha incorreta"}), 401
    else:
        return jsonify({"message": "Usuário não encontrado"}), 401

# Rota de Logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido!"}), 200

# Rota inicial - Exibe as tarefas pendentes e concluídas (WEB)
@app.route('/', methods=['GET'])
@login_required
def index():
    pending_tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('index.html', pending_tasks=pending_tasks, completed_tasks=completed_tasks)

# Rota para adicionar uma tarefa (API)
@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    task_name = data.get('task')

    if task_name:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Tarefa adicionada!"}), 201
    else:
        return jsonify({"message": "O nome da tarefa é obrigatório!"}), 400

# Rota para editar uma tarefa (API)
@app.route('/edit_task/<int:task_id>', methods=['PUT'])
@login_required
def edit_task(task_id):
    data = request.get_json()
    new_name = data.get('task')

    if new_name:
        task = Task.query.get(task_id)
        if task:
            task.name = new_name
            db.session.commit()
            return jsonify({"message": "Tarefa atualizada!"}), 200
        else:
            return jsonify({"message": "Tarefa não encontrada!"}), 404
    else:
        return jsonify({"message": "O nome da tarefa é obrigatório!"}), 400

# Rota para deletar uma tarefa (API)
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarefa deletada!"}), 200
    else:
        return jsonify({"message": "Tarefa não encontrada!"}), 404

# Rota para concluir uma tarefa (API)
@app.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({"message": "Tarefa concluída!"}), 200
    else:
        return jsonify({"message": "Tarefa não encontrada!"}), 404

# Rota para obter todas as tarefas (API, JSON)
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    pending_tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()

    tasks = {
        "pending_tasks": [{"id": task.id, "name": task.name, "completed": task.completed} for task in pending_tasks],
        "completed_tasks": [{"id": task.id, "name": task.name, "completed": task.completed} for task in completed_tasks]
    }
    
    return jsonify(tasks)

# Rota para obter uma tarefa específica (API, JSON)
@app.route('/api/task/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task_data = {
            "id": task.id,
            "name": task.name,
            "completed": task.completed
        }
        return jsonify(task_data), 200
    else:
        return jsonify({"message": "Tarefa não encontrada!"}), 404

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

