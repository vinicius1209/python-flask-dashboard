from flask import render_template, redirect, request, flash, jsonify, url_for
from app import dashboard
from app.models import Tarefas_comentarios, Tarefas, Nao_conformidades, Mensagem_notificacoes, Usuarios, add_comentarios
from sqlalchemy import or_, desc
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urljoin, urlparse

# Check if url is safe http://flask.pocoo.org/snippets/63/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@dashboard.route('/', methods=['GET', 'POST'])
@dashboard.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        if request.form['username'] is None:
            return abort(400)

        if request.form['password'] is None:
            return abort(400)        
        
        usuario = Usuarios.query.filter_by(usuario=request.form['username'], senha_interna=request.form['password']).first()
        
        if usuario is None:
            flash('Credenciais invalidas. Por favor tente novamente!', 'error')
            return render_template('login.html', title='Login')
        else:
            login_user(usuario)
            next = request.args.get('next')

            if not is_safe_url(next):
                return abort(400)

            return redirect('dashboard')
    else:
        return render_template('login.html', title='Login')


@dashboard.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return render_template('login.html', title='Login')


@dashboard.route('/dashboard')
@login_required
def relatorio():
    if current_user.is_authenticated:
        user = current_user.usuario
        total_tasks = Tarefas.query.filter_by(status_para_tar='N', para=user, modo_ct='CTAP').count()
        total_emails = Mensagem_notificacoes.query.filter_by(enviada='N').count()
        total_ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=user, modo_ct='CTAP').count()
        return render_template('dashboard.html', title='Dashboard', user=user, total_emails=total_emails, total_tasks=total_tasks, total_ncs=total_ncs)
    return redirect('login')


@dashboard.route('/emails')
@login_required
def emails():
    if current_user.is_authenticated:
        emails = Mensagem_notificacoes.query.filter_by(enviada='N').all()

        if len(emails) == 0:
            flash('Sem e-mails travados no momento :)', 'warning')
            return redirect('dashboard')

        return render_template('emails.html', title='E-mails', emails=emails)
    else:
        return redirect('login')


@dashboard.route('/tasks')
@login_required
def tasks():
    if current_user.is_authenticated:
        user = current_user.usuario
        tasks = Tarefas.query.filter_by(status_para_tar='N', para=user, modo_ct='CTAP').all()

        if len(tasks) == 0:
            flash('Sem tarefas no momento :)', 'warning')
            return redirect('dashboard')

        return render_template('tasks.html', title='Tarefas', tasks=tasks)
    else:
        return redirect('login')


@dashboard.route('/ncs')
@login_required
def ncs():
    if current_user.is_authenticated:
        user = current_user.usuario
        ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=user, modo_ct='CTAP').all()

        if len(ncs) == 0:
            flash('Sem NCs no momento :)', 'warning')
            return redirect('dashboard')

        return render_template('ncs.html', title="Nc's", ncs=ncs)
    else:
        return redirect('login')


@dashboard.route('/forum/', methods=['GET'])
@dashboard.route('/forum/<int:task_id>', methods=['GET', 'POST'])
@login_required
def forum(task_id=-1):
    if current_user.is_authenticated:
        if request.path == '/forum/' or task_id == -1:
            return redirect('dashboard')
        if request.method == 'POST':
            msg = request.form['mensagem']
            user = current_user.usuario
            add_comentarios(task_id, msg, user)
        #Busca os comentarios, com a clausula Where usando um "or", depois ordena de forma "DESC" a consulta e pegar todos os registros "ALL"
        forum = Tarefas_comentarios.query.filter(or_(Tarefas_comentarios.idtarefa==task_id, Tarefas_comentarios.idnao_conf==task_id)).order_by(desc(Tarefas_comentarios.dt_cadastro)).all()
        return render_template('forum.html', title='Forum tarefa %d' % task_id, forum=forum)
    else:
        return redirect('login')

@dashboard.route('/modalforum/<int:task_id>', methods=['GET', 'POST'])
@login_required
def modalforum(task_id=-1):

    if current_user.is_authenticated:
        
        if task_id == -1:
            return redirect('dashboard')

        if request.method == 'POST':
            msg = request.json['mensagem']
            user = current_user.usuario

            if msg != '':
                add_comentarios(task_id, msg, user)

        #Busca os comentarios, com a clausula Where usando um "or", depois ordena de forma "DESC" a consulta e pegar todos os registros "ALL"
        resultado = Tarefas_comentarios.query.filter(or_(Tarefas_comentarios.idtarefa==task_id, Tarefas_comentarios.idnao_conf==task_id)).order_by(desc(Tarefas_comentarios.dt_cadastro)).limit(5).all()
        forum_json = []

        for x in resultado:
            forum = { "comentario": x.comentario, "usuario": x.usuario, "dt_cadastro":  x.dt_cadastro}
            forum_json.append(forum)

        return jsonify(forum_json)
    else:
        return redirect('login')

@dashboard.route('/_dashboardValues', methods=['GET'])
def stuff():
    if current_user.is_authenticated:
        user = current_user.usuario
        total_tasks = Tarefas.query.filter_by(status_para_tar='N', para=user, modo_ct='CTAP').count()
        total_emails = Mensagem_notificacoes.query.filter_by(enviada='N').count()
        total_ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=user, modo_ct='CTAP').count()
        return jsonify(total_tasks=total_tasks, total_emails=total_emails, total_ncs=total_ncs)
    else:
        return jsonify(total_tasks=0, total_emails=0, total_ncs=0)

