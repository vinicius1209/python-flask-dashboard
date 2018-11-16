import pyodbc
from app.smtp import sendInternalEmails
from app.models import Mensagem_notificacoes
from datetime import datetime

def conSqlServer():
    try:
        server = '192.168.100.2'
        database = 'Finan'
        username = 'moises'
        password = 'moises'

        return pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    except Exception as e:
        print(e)


def sendEmailsInterval():

    print(str(datetime.utcnow()) + ' : Iniciando envio de e-mails.')

    lst_emails = Mensagem_notificacoes.query.filter_by(enviada='N').all()

    for email in lst_emails:
        sendInternalEmails(email)

        try:
            cnxn = conSqlServer()

            query_upd_enviada = \
                ("UPDATE MENSAGEM_NOTIFICACOES SET ERRO = 'N', ENVIADA = 'S', MSG_ERRO = NULL WHERE IDNOTIFICACAO = ? ")

            cursor = cnxn.cursor()
            cursor.execute(query_upd_enviada, email.idnotificacao)
            cnxn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            cnxn.close()

    print(str(datetime.utcnow()) + ' : Finalizando envio de e-mails.')