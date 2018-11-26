from app import db
from app import login_manager
import time


class Tarefas(db.Model):
    idtarefa = db.Column(db.Integer, primary_key=True, nullable=False)
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
    # Colunas "imaginarias" das relações existentes
    notificacoes = db.relationship('Mensagem_notificacoes', backref='notificacoes_tarefa')
    comentarios = db.relationship('Tarefas_comentarios', backref='comentarios_tarefa')
    ncs = db.relationship('Nao_conformidades', backref='ncs')
    modulo = db.relationship('Modulos')
    cliente = db.relationship('Clientes')


class Nao_conformidades(db.Model):
    idnao_conf = db.Column(db.Integer, primary_key=True, nullable=False)
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
    # Colunas "imaginarias" das relações existentes
    notificacoes = db.relationship('Mensagem_notificacoes', backref='notificacoes_nc')
    comentarios = db.relationship('Tarefas_comentarios', backref='comentarios_nc')
    modulo = db.relationship('Modulos')
    cliente = db.relationship('Clientes')
    tarefa = db.relationship('Tarefas')


class Tarefas_comentarios(db.Model):
    idcoment = db.Column(db.Integer, primary_key=True, nullable=False)
    dt_cadastro = db.Column(db.DateTime, nullable=False)
    usuario = db.Column(db.String(8), nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    idtarefa = db.Column(db.Integer, db.ForeignKey('tarefas.idtarefa'), nullable=True)
    idnao_conf = db.Column(db.Integer, db.ForeignKey('nao_conformidades.idnao_conf'), nullable=True)


class Mensagem_notificacoes(db.Model):
    idnotificacao = db.Column(db.Integer, primary_key=True, nullable=False)
    idtarefa = db.Column(db.Integer, db.ForeignKey('tarefas.idtarefa'), nullable=True)
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


class Usuarios(db.Model):
    usuario = db.Column(db.String(8), primary_key=True, nullable=False)
    senha_interna = db.Column(db.String(8), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    modo_ct = db.Column(db.String(4), nullable=False)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.usuario
        except AttributeError:
            raise NotImplementedError('Erro em get_id na classe Usuarios')


@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(user_id)


def add_comentarios(task_id, msg, user_id):
    is_task = Tarefas.query.filter_by(idtarefa=task_id, modo_ct='CTAP').first()
    dt_cadastro = time.strftime('%Y-%m-%d %H:%M:%S')
    if is_task is not None:
        forum = Tarefas_comentarios(dt_cadastro=dt_cadastro, usuario=user_id, comentario=msg, idtarefa=task_id)
        db.session.add(forum)
        db.session.commit()
    else:
        is_nc = Nao_conformidades.query.filter_by(idnao_conf=task_id, modo_ct='CTAP').first()
        if is_nc is not None:
            forum = Tarefas_comentarios(dt_cadastro=dt_cadastro, usuario=user_id, comentario=msg, idnao_conf=task_id)
            db.session.add(forum)
            db.session.commit()
        else:
            return False
