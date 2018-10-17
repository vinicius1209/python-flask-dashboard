from app import db

class Tarefas(db.Model):
    idtarefa = db.Column(db.Integer, primary_key=True)
    ds_tarefa = db.Column(db.Text, unique=False, nullable=False)
    notepad_tar = db.Column(db.Text, unique=False, nullable=False)

class Nao_conformidades(db.Model):
    idnao_conf = db.Column(db.Integer, primary_key=True)
    ds_naoconf = db.Column(db.String(100), unique=False, nullable=False)
    obs_naoconf = db.Column(db.Text, unique=False, nullable=False)

class Tarefas_ctap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(1), unique=False, nullable=False)
    usuario_de = db.Column(db.String(8), unique=False, nullable=False)
    usuario_para = db.Column(db.String(8), unique=False, nullable=False)
    usuario_int = db.Column(db.String(8), unique=False, nullable=True)
    descricao = db.Column(db.String(100), unique=False, nullable=True)
    prioridade = db.Column(db.String(3), unique=False, nullable=True)
    urgencia = db.Column(db.String(1), unique=False, nullable=True)
    dt_cadastro = db.Column(db.DateTime, unique=False, nullable=True)
    idmodulo = db.Column(db.Integer, nullable=True)
    ds_mod = db.Column(db.String(40), unique=False, nullable=True)
    nome_abr_cli = db.Column(db.String(15), unique=False, nullable=True)
    status_progr = db.Column(db.Integer, nullable=True)
    modo_ct = db.Column(db.String(4), unique=False, nullable=False)
    celula = db.Column(db.String(100), unique=False, nullable=True)
    sigla = db.Column(db.String(5), unique=False, nullable=True)
    executada = db.Column(db.String(1), unique=False, nullable=True)
    setor = db.Column(db.String(1), unique=False, nullable=True)
    usuario_tar = db.Column(db.String(8), unique=False, nullable=True)
    islogopen = db.Column(db.String(1), unique=False, nullable=False)

class Tarefas_comentarios(db.Model):
    idcoment = db.Column(db.Integer, primary_key=True)
    dt_cadastro = db.Column(db.DateTime, unique=False, nullable=False)
    usuario = db.Column(db.String(8), unique=False, nullable=False)
    comentario = db.Column(db.Text, unique=False, nullable=True)
    idtarefa = db.Column(db.Integer, nullable=False)
    idnao_conf = db.Column(db.Integer, nullable=False)

class Mensagem_notificacoes(db.Model):
    idnotificacao = db.Column(db.Integer, primary_key=True)
    idtarefa = db.Column(db.Integer,  db.ForeignKey('tarefas.idtarefa'), nullable=True)
    idnao_conf = db.Column(db.Integer, db.ForeignKey('nao_conformidades.idnao_conf'), nullable=True)
    desc_mensagem = db.Column(db.Text, unique=False, nullable=True)
    to_address = db.Column(db.String(500), unique=False, nullable=True)
    copy_to = db.Column(db.String(500), unique=False, nullable=True)
    username = db.Column(db.String(255), unique=False, nullable=True)
    dh_cadastro = db.Column(db.DateTime, unique=False, nullable=True)
    enviada = db.Column(db.String(1), unique=False, nullable=True)
    tipo = db.Column(db.Integer, nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    from_address = db.Column(db.String(255), nullable=True)
    erro = db.Column(db.String(1), nullable=False)
    msg_erro = db.Column(db.Text, nullable=True)
    utiliza_layout = db.Column(db.String(1), nullable=False)
    tipo_mensagem = db.Column(db.String(1), nullable=False)

    tarefas = db.relationship('Tarefas', backref=db.backref('Mensagem_notificacoes', lazy=True))
    nao_conformidades = db.relationship('Nao_conformidades', backref=db.backref('Mensagem_notificacoes', lazy=True))