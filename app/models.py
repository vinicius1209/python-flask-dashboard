from app import db

class Tarefas_ctap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_de = db.Column(db.String(8), unique=False, nullable=False)
    usuario_para = db.Column(db.String(8), unique=False, nullable=False)
    descricao = db.Column(db.String(100), unique=False, nullable=True)