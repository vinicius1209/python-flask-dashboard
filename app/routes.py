from flask import render_template, redirect, request, session, flash
from app import dashboard, cache
from app.database import conSqlServer, getTarefas, getEmailsToSend, replaceAddressEmail, insertForumMessage, setEmailSent
from app.smtp import sendInternalEmails
from app.models import Tarefas_comentarios, Tarefas, Nao_conformidades
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
@cache.cached(timeout=10)
def relatorio():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    user = session['username']
    emails = getEmailsToSend()
    tasks = getTarefas()

    return render_template('dashboard.html', title='Dashboard', user=user, emails=emails, tasks=tasks)

@dashboard.route('/emails')
def emails():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    emails = getEmailsToSend()

    return render_template('emails.html', title='E-mails', emails=emails)

@dashboard.route('/tasks')
def tasks():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    usuario = session['username']

    tasks = Tarefas.query.filter_by(status_para_tar='N', para=usuario, modo_ct='CTAP').all()
    ncs = Nao_conformidades.query.filter_by(status_exec='N', usuario_para=usuario, modo_ct='CTAP').all()

    return render_template('tasks.html', title='Tarefas', tasks=tasks, ncs=ncs)

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
        lst_emails = getEmailsToSend()

        if lst_emails[1] == 0:
            return '302'

        for email in lst_emails[0]:
            sendInternalEmails(email)
            setEmailSent(email['IDNOTIFICACAO'])
        return '200'
    except Exception as e:
        print(e)
        return '404'


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

@dashboard.route('/teste')
def teste():

    #Busco os dados pela classe
    mensagens = Tarefas_ctap.query.filter_by(usuario_para='VINICIUS', executada='N').all()

    #Consigo acessar cada atributo da classe
    for mensagem in mensagens:
        print(mensagem)

    return redirect('dashboard')

