from flask import render_template, redirect, request, current_app, session, jsonify, flash
from app import dashboard
from app.database import conSqlServer, getMsgErros, getTarefas, getTarefaForumById, setEmail

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
def relatorio():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    user = session['username']
    errors = getMsgErros()
    tasks = getTarefas()

    return render_template('dashboard.html', title='Dashboard', user=user, errors=errors, tasks=tasks)

@dashboard.route('/emails')
def emails():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    errors = getMsgErros()

    return render_template('emails.html', title='E-mails', errors=errors)

@dashboard.route('/todo')
@dashboard.route('/tasks')
def tasks():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    tasks = getTarefas()

    if request.path == '/tasks':
        return render_template('tasks.html', title='Tarefas', tasks=tasks)
    else:
        return render_template('todo.html', title='To do', tasks=tasks)

@dashboard.route('/forum/')
@dashboard.route('/forum/<int:task_id>')
def forum(task_id=-1):

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    if task_id == -1:
        return redirect('dashboard')
    else:
        forum = getTarefaForumById(task_id)
        return render_template('forum.html', title='Task %d' % task_id, forum=forum)

@dashboard.route('/replace', methods=['POST'])
def replace():

    if not session.get('logged_in'):
        return render_template('login.html', title='Login')

    email = request.form['email']
    if not setEmail(email):
        flash('Erro nao tratado em setEmail!')
    else:
        flash('E-mails do {} ajustados com sucesso!'.format(email))
    
    return redirect('dashboard')