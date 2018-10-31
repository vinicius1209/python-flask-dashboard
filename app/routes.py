from flask import render_template, redirect, request, session, flash, jsonify
from app import dashboard, cache
from app.database import conSqlServer, replaceAddressEmail, insertForumMessage, setEmailSent
from app.smtp import sendInternalEmails
from app.models import Tarefas_comentarios, Tarefas, Nao_conformidades, Mensagem_notificacoes
from sqlalchemy import or_


@dashboard.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html', title='Login', user='Vinicius')
    else:
        return redirect('dashboard')

@dashboard.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        cnxn = conSqlServer()
        if not cnxn:
            flash('Credenciais invalidas. Por favor tente novamente.')
            session['username'] = None
            session['password'] = None
            return redirect('login')
        else:
            session['logged_in'] = True
            cnxn.close()
            return redirect('dashboard')
    else:
        return render_template('login.html', title='Login')

@dashboard.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        session['username'] = None
        session['password'] = None

    return render_template('login.html', title='Login')

@dashboard.route('/dashboard')
@cache.cached(timeout=5)
def relatorio():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    user = session['username']

    total_tasks = Tarefas.query.filter_by(status_para_tar='N', para=user, modo_ct='CTAP').count()
    total_emails = Mensagem_notificacoes.query.filter_by(enviada='N').count()
    total_ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=user, modo_ct='CTAP').count()

    return render_template('dashboard.html', title='Dashboard', user=user, total_emails=total_emails, total_tasks=total_tasks, total_ncs=total_ncs)

@dashboard.route('/emails')
def emails():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    emails = Mensagem_notificacoes.query.filter_by(enviada='N').all()

    return render_template('emails.html', title='E-mails', emails=emails)

@dashboard.route('/tasks')
def tasks():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    user = session['username']

    tasks = Tarefas.query.filter_by(status_para_tar='N', para=user, modo_ct='CTAP').all()

    return render_template('tasks.html', title='Tarefas', tasks=tasks)

@dashboard.route('/ncs')
def ncs():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    user = session['username']

    ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=user, modo_ct='CTAP').all()

    return render_template('ncs.html', title="Nc's", ncs=ncs)

@dashboard.route('/forum/', methods=['GET'])
@dashboard.route('/forum/<int:task_id>', methods=['GET', 'POST'])
def forum(task_id=-1):

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    if request.path == '/forum/' or task_id == -1:
        return redirect('dashboard')

    if request.method == 'POST':
        insertForumMessage(task_id, request.form['mensagem'], session['username'])

    forum = Tarefas_comentarios.query.filter(or_(Tarefas_comentarios.idtarefa==task_id, Tarefas_comentarios.idnao_conf==task_id)).all()

    return render_template('forum.html', title='Forum tarefa %d' % task_id, forum=forum)

@dashboard.route('/sendEmails', methods=['GET'])
def sendEmails():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    try:
        lst_emails = Mensagem_notificacoes.query.filter_by(enviada='N').all()

        if len(lst_emails) == 0:
            flash('A lista de e-mails está vazia!', 'error')
            return redirect('emails')

        for email in lst_emails:
            sendInternalEmails(email)
            setEmailSent(email.idnotificacao)

        flash('E-Mails enviados com sucesso!', 'success')
        return redirect('emails')

    except Exception as e:
        print(e)
        flash('Erro estranho aconteceu, verifique com o administrador :/', 'error')


@dashboard.route('/replace', methods=['POST'])
def replace():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    email = request.form['email']
    idnotificacao = request.form['idnotificacao']

    if not replaceAddressEmail(email, idnotificacao):
        flash('Erro nao tratado em setEmail!')
    else:
        flash('E-mails do {} ajustados com sucesso!'.format(email))

@dashboard.route('/_dashboardValues', methods= ['GET'])
def stuff():
    user = session['username']

    total_tasks = Tarefas.query.filter_by(status_para_tar='N', para=user, modo_ct='CTAP').count()
    total_emails = Mensagem_notificacoes.query.filter_by(enviada='N').count()
    total_ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=user, modo_ct='CTAP').count()

    return jsonify(total_tasks=total_tasks, total_emails=total_emails, total_ncs=total_ncs)

