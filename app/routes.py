from flask import (render_template, request, redirect, url_for,flash, abort, jsonify, session)
from app import app

#---MODEL (Nossa lista offline simulando um banco de dados) ---
TAREFAS_DB = {
    1:{'texto':'Aprender os conceitos de Flask', "concluida": True},
    2:{'texto': 'Ver os exemplos de código', 'concluída': False},
    3:{'texto': 'COnstruir minha própria aplicação', 'concluída': False}
}
next_id = 4
# --- FIM DO MODEL ---

# --- CONTROLLER ---
#Rota 1: Coleção de Itens (Página inicial)
@app.route('/')
def index():
    return render_template('index.html', tarefas=TAREFAS_DB)

#Rota 2: Página de Detalhes
@app.route('/tarefa/<int:tarefa_id>')
def detalhe_tarefa(tarefa_id):
    tarefa = TAREFAS_DB.get(tarefa_id)
    if not tarefa:
        abort(404) # Dispara o erro 404
    return render_template('detalhe.html', tarefa=tarefa, tarefa_id=tarefa_id)

#Rota 3: Adicionar Tarefa (Acesso a dados, Validação, Flash, Sessão)
@app.route('/adicionar', methods=['POST'])
def adicionar():
    global next_id
    texto_tarefa = request.form.get('texto_da_tarefa')

    # Validação no Back-end
    if not texto_tarefa or len(texto_tarefa) < 3:
        flash('A tarefa precisa ter pelo menos 3 caracteres!', 'erro')
    else:
        #Lógica do Model
        TAREFAS_DB[next_id] = {'texto': texto_tarefa, 'concluida': False}
        next_id += 1

        #Flash Message de sucesso 
        flash('Tarefa adiciona com sucesso!', 'sucesso')

        # Lógica de Sessão
        session['contador'] = session.get('contador', 0) + 1
        flash(f"Você já adicionou {session['contador']} tarefas", 'info')

    return redirect(url_for('index'))

# Rota 4: Rota para a interação AJAX
@app.route('/tarefa/concluir/<int:tarefa_id>', methods=['POST'])
def concluir_tarefa(tarefa_id):
    tarefa = TAREFAS_DB.get(tarefa_id)
    if tarefa:
        tarefa['concluida'] = not tarefa['concluida']
        return jsonify({'status': 'sucesso', 'concluida': tarefa['concluida']})
    return jsonify({'status': 'erro'}), 404

# Rota 5: Simulação de página restrita para gerar erro 403
@app.route('/admin')
def admin_panel():
    if session.get('username') != 'admin': # Exemplo de verificação
        abort(403) # Dispara o erro 403
    return "<h1>Painel do administrador</h1>"

# Handler para o erro 404 (Não encontrado)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('erros/404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('erros/403.html'), 403

# Handler para o Erro 401 ( Não autorizado) - (não simulado, mas pronto para uso)
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('erros/401.html'), 401
