from app import db

class Tarefas_ctap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(1), unique=False, nullable=False)
    usuario_de = db.Column(db.String(8), unique=False, nullable=False)
    usuario_para = db.Column(db.String(8), unique=False, nullable=False)
    descricao = db.Column(db.String(100), unique=False, nullable=True)

class Tarefas_comentarios(db.Model):
    idcoment = db.Column(db.Integer, primary_key=True)
    dt_cadastro = db.Column(db.DateTime, unique=False, nullable=False)
    usuario = db.Column(db.String(8), unique=False, nullable=False)
    comentario = db.Column(db.Text, unique=False, nullable=True)
    idtarefa = db.Column(db.Integer, nullable=False)
    idnao_conf = db.Column(db.Integer, nullable=False)