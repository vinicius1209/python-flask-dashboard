from app.smtp import sendInternalEmails
from app.models import Mensagem_notificacoes, db
from datetime import datetime

def sendEmailsInterval():

    print(str(datetime.utcnow()) + ' : Iniciando envio de e-mails.')

    lst_emails = Mensagem_notificacoes.query.filter_by(enviada='N').all()

    for email in lst_emails:
        if sendInternalEmails(email):
            try:
                print('Vai atualizar as informações do e-mail.')
                email.erro = 'N'
                email.enviada = 'S'
                email.msg_erro = None
                db.session.commit()
                print('Informações do e-mail atualizadas.')
            except Exception as e:
                print(e)

    print(str(datetime.utcnow()) + ' : Finalizando envio de e-mails.')