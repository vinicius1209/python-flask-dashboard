from app import db

class Tarefas(db.Model):
    idtarefa = db.Column(db.Integer, primary_key=True,  nullable=False)
    ds_tarefa = db.Column(db.Text, nullable=True)
    notepad_tar = db.Column(db.Text, nullable=True)
    rotina = db.Column(db.String(255), nullable=True)
    desc_tar = db.Column(db.String(100), nullable=True)
    de = db.Column(db.String(8), nullable=False)
    para = db.Column(db.String(8), nullable=False)
    modo_ct = db.Column(db.String(4), nullable=False)
    idmodulo = db.Column(db.Integer, db.ForeignKey('modulos.idmodulo'), nullable=True)
    idcliente = db.Column(db.Integer, db.ForeignKey('clientes.idcliente'), nullable=True)
    idchamado = db.Column(db.Integer, nullable=True)
    status_progr = db.Column(db.Integer, nullable=True)
    status_para_tar = db.Column(db.Integer, nullable=False)
    status_solic_orcamento = db.Column(db.Integer, nullable=True)
    data_criacao_tar = db.Column(db.DateTime, nullable=True)
    #Colunas "imaginarias" das relações existentes
    notificacoes = db.relationship('Mensagem_notificacoes', backref='notificacoes_tarefa')
    comentarios = db.relationship('Tarefas_comentarios', backref='comentarios_tarefa')
    ncs = db.relationship('Nao_conformidades', backref='ncs')

class Nao_conformidades(db.Model):
    idnao_conf = db.Column(db.Integer, primary_key=True,  nullable=False)
    idtarefa = db.Column(db.Integer, db.ForeignKey('tarefas.idtarefa'), nullable=False)
    usuario_de = db.Column(db.String(8), nullable=False)
    usuario_para = db.Column(db.String(8), nullable=False)
    ds_naoconf = db.Column(db.String(100), nullable=False)
    modo_ct = db.Column(db.String(4), nullable=False)
    obs_naoconf = db.Column(db.Text, nullable=False)
    status_exec = db.Column(db.Integer, nullable=False)
    dh_cadastro = db.Column(db.DateTime, nullable=True)
    status_progr = db.Column(db.Integer, nullable=True)
    idcliente = db.Column(db.Integer, db.ForeignKey('clientes.idcliente'), nullable=True)
    idmodulo = db.Column(db.Integer, db.ForeignKey('modulos.idmodulo'), nullable=True)
    #Colunas "imaginarias" das relações existentes
    notificacoes = db.relationship('Mensagem_notificacoes', backref='notificacoes_nc')
    comentarios = db.relationship('Tarefas_comentarios', backref='comentarios_nc')

class Tarefas_comentarios(db.Model):
    idcoment = db.Column(db.Integer, primary_key=True, nullable=False)
    dt_cadastro = db.Column(db.DateTime, nullable=False)
    usuario = db.Column(db.String(8), nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    idtarefa = db.Column(db.Integer,  db.ForeignKey('tarefas.idtarefa'), nullable=True)
    idnao_conf = db.Column(db.Integer, db.ForeignKey('nao_conformidades.idnao_conf'), nullable=True)

class Mensagem_notificacoes(db.Model):
    idnotificacao = db.Column(db.Integer, primary_key=True, nullable=False)
    idtarefa = db.Column(db.Integer,  db.ForeignKey('tarefas.idtarefa'), nullable=True)
    idnao_conf = db.Column(db.Integer, db.ForeignKey('nao_conformidades.idnao_conf'), nullable=True)
    desc_mensagem = db.Column(db.Text, nullable=True)
    to_address = db.Column(db.String(500), nullable=True)
    copy_to = db.Column(db.String(500), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    dh_cadastro = db.Column(db.DateTime, nullable=True)
    enviada = db.Column(db.String(1), nullable=True)
    tipo = db.Column(db.Integer, nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    from_address = db.Column(db.String(255), nullable=True)
    erro = db.Column(db.String(1), nullable=False)
    msg_erro = db.Column(db.Text, nullable=True)
    utiliza_layout = db.Column(db.String(1), nullable=False)
    tipo_mensagem = db.Column(db.String(1), nullable=False)

class Modulos(db.Model):
    idmodulo = db.Column(db.Integer, primary_key=True, nullable=False)
    ds_mod = db.Column(db.String(40), nullable=True)
    sigla = db.Column(db.String(10), nullable=True)

class Clientes(db.Model):
    idcliente = db.Column(db.Integer, primary_key=True, nullable=False)
    nome_abr_cli = db.Column(db.String(15), nullable=True)