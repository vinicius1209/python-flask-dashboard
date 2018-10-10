from flask import session
import pyodbc
import json
from app import smtp
from app.smtp import sendInternalEmails

def conSqlServer():
    cnxn = None

    try:
        server = '192.168.100.2'
        database = 'Finan'
        username = session['username']
        password = session['password']
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    except Exception as e:
        print('Erro ao conectar na base de dados: ' + e)
        return False

    finally:
        return cnxn

def getMsgErros():

    resultado = None

    try:
        cnxn = conSqlServer()

        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT"
            "   IDNOTIFICACAO, "
            "   FROM_ADDRESS, "
            "   TO_ADDRESS, "
            "   COPY_TO, "
            "   SUBJECT, "
            "   USERNAME, "
            "   MSG_ERRO "
            "FROM"
            "   MENSAGEM_NOTIFICACOES "
            "WHERE"
            "   ERRO = 'S'"
        )
        row_headers = [x[0] for x in cursor.description]
        result_set = cursor.fetchall()

        msg_erro = []

        for row in result_set:
            msg_erro.append(dict(zip(row_headers, row)))

        resultado = [msg_erro, len(msg_erro)]
    except Exception as e:
        print('Erro ao buscar os e-mails com erros na base: ' + e)
        return False

    finally:
        cursor.close()
        cnxn.close()
        return resultado

def getTarefas():

    resultado = None

    try:
        cnxn = conSqlServer()
        cursor = cnxn.cursor()

        query = (
            "SELECT"
            "   PAI.PRIORIDADE, "
            "   PAI.TIPO, "
            "   CASE "
            "       WHEN PAI.TIPO = 'T' THEN "
            "           'TAREFA' "
            "       ELSE 'NC' "
            "   END AS DESC_TIPO, "
            "   PAI.URGENCIA, "
            "   PAI.ID,	"
            "   PAI.DT_CADASTRO, "
            "   PAI.USUARIO_DE,"
            "   PAI.USUARIO_PARA, "
            "   PAI.DESCRICAO,	"
            "   FILHO.DS_TAREFA AS DEFINICAO, "
            "   CASE "
            "       WHEN PAI.TIPO = 'T' THEN "
            "           FILHO.NOTEPAD_TAR "
            "       ELSE NC.OBS_NAOCONF "
            "   END AS REQUISITOS, "
            "   PAI.DS_MOD, "
            "   FILHO.ROTINA, "
            "   PAI.NOME_ABR_CLI, "
            "   PAI.STATUS_PROGR, "
            "   PAI.MODO_CT, "
            "   PAI.ISLOGOPEN,"
            "   PAI.CELULA,"
            "   FILHO.STATUS_SOLIC_ORCAMENTO FROM "
            "   DBO.TAREFAS_CTAP PAI, "
            "   DBO.TAREFAS FILHO "
            "   LEFT JOIN NAO_CONFORMIDADES NC ON (NC.IDNAO_CONF = FILHO.IDTAREFA) "
            "WHERE"
            "   PAI.ID = FILHO.IDTAREFA AND "
            "   PAI.USUARIO_TAR IS NOT NULL "
            "   AND PAI.EXECUTADA = 'N' AND "
            "   PAI.STATUS_PROGR BETWEEN 1 AND 8 AND "
            "   PAI.USUARIO_PARA = ? "
        )

        params = (session['username'])
        cursor.execute(query, params)

        row_headers = [x[0] for x in cursor.description]
        result_set = cursor.fetchall()

        lst_tarefas = []

        for row in result_set:
            lst_tarefas.append(dict(zip(row_headers, row)))

        resultado = [lst_tarefas, len(lst_tarefas)]

    except Exception as e:
        print('Erro ao buscar a lista de tarefas na base: ' + e)
        return False

    finally:
        cursor.close()
        cnxn.close()
        return resultado

def getTarefaForumById(tarefa):

    resultado = None

    try:
        cnxn = conSqlServer()
        cursor = cnxn.cursor()

        queryForum = (
            "SELECT "
            "   IDCOMENT, "
            "   IDTAREFA, "
            "   IDNAO_CONF, "
            "   DT_CADASTRO, "
            "   USUARIO, "
            "   COMENTARIO "
            "FROM"
            "   TAREFAS_COMENTARIOS "
            "WHERE"
            "   (IDTAREFA = ? OR IDNAO_CONF = ?) "
            "ORDER BY "
            "   DT_CADASTRO DESC"
        )

        queryTarefa = (
            "SELECT "
            "   PAI.PRIORIDADE, "
            "   PAI.TIPO, "
            "   PAI.URGENCIA, "
            "   PAI.ID,	"
            "   PAI.DT_CADASTRO, "
            "   PAI.USUARIO_DE, "
            "   PAI.USUARIO_PARA, "
            "   PAI.DESCRICAO,	"
            "   FILHO.DS_TAREFA AS DEFINICAO, "
            "   CASE "
            "       WHEN PAI.TIPO = 'T' THEN "
            "           FILHO.NOTEPAD_TAR "
            "       ELSE NC.OBS_NAOCONF "
            "   END AS REQUISITOS, "
            "   PAI.DS_MOD, "
            "   FILHO.ROTINA, "
            "   PAI.NOME_ABR_CLI, "
            "   PAI.STATUS_PROGR, "
            "   PAI.MODO_CT, "
            "   PAI.ISLOGOPEN,"
            "   PAI.CELULA "
            "FROM"
            "   DBO.TAREFAS_CTAP PAI, "
            "   DBO.TAREFAS FILHO "
            "   LEFT JOIN NAO_CONFORMIDADES NC ON (NC.IDNAO_CONF = FILHO.IDTAREFA) "
            "WHERE "
            "   PAI.ID = FILHO.IDTAREFA AND "
            "   PAI.USUARIO_TAR IS NOT NULL AND "
            "   PAI.EXECUTADA = 'N' AND "
            "   PAI.STATUS_PROGR BETWEEN 1 AND 8 AND "
            "   PAI.ID = ? "
        )

        params = (tarefa, tarefa)
        cursor.execute(queryForum, params)

        row_headers = [x[0] for x in cursor.description]
        result_set = cursor.fetchall()
        lst_forum = []

        for row in result_set:
            lst_forum.append(dict(zip(row_headers, row)))

        cursor.execute(queryTarefa, tarefa)

        row_headers = [x[0] for x in cursor.description]
        result_set = cursor.fetchall()
        lst_tarefa = []

        for row in result_set:
            lst_tarefa.append(dict(zip(row_headers, row)))

        resultado = [lst_forum, lst_tarefa]

    except Exception as e:
        print('Erro ao buscar as listas de comentarios no Forum e informacoes da Tarefa: ' + e)
        return False

    finally:
        cursor.close()
        cnxn.close()
        return resultado

def setEmail(email, idnotificacao):

    try:
        cnxn = conSqlServer()
        query = (
                " UPDATE MENSAGEM_NOTIFICACOES "
                " SET ERRO = 'N', "
                " TO_ADDRESS = replace(TO_ADDRESS , ?, ''), "
                " COPY_TO = replace(COPY_TO, ?, '') "
                " WHERE ERRO = 'S' AND ENVIADA = 'N' AND IDNOTIFICACAO = ? "
        )

        params = (email, email, idnotificacao)

        cursor = cnxn.cursor()
        cursor.execute(query, params)
        cnxn.commit()

    except Exception as e:
        print('Erro ao efetuar update do e-mail de notificação : ' + str(idnotificacao) + ' para VAZIO. Erro: ' + e)
        return False

    finally:
        cursor.close()
        cnxn.close()
        return True

def getEmailsToSend():

    try:
        cnxn = conSqlServer()
        query = (
            "SELECT "
                " IDNOTIFICACAO, "
                " NOTI.IDNAO_CONF, "
                " (CASE ISNULL(NOTI.IDNAO_CONF,0) "
                    " WHEN 0 THEN "
                        " TAR.DS_TAREFA "
                    " ELSE "
                        " NC.DS_NAOCONF "
                " END) AS TAREFA, "
                " NOTI.IDTAREFA, "
                " DESC_MENSAGEM, "
                " TO_ADDRESS, "
                " COPY_TO, "
                " USERNAME, "
                " ENVIADA, "
                " SUBJECT, "
                " TIPO, "
                " FROM_ADDRESS, "
                " ERRO, "
                " MSG_ERRO, "
                " UTILIZA_LAYOUT, "
                " TIPO_MENSAGEM  FROM " 
                " MENSAGEM_NOTIFICACOES NOTI "
                " LEFT JOIN TAREFAS TAR ON (TAR.IDTAREFA = NOTI.IDTAREFA) "
                " LEFT JOIN NAO_CONFORMIDADES NC ON (NC.IDNAO_CONF = NOTI.IDNAO_CONF) WHERE "
                " ISNULL(ENVIADA,'N') = 'N' "
        )

        cursor = cnxn.cursor()
        cursor.execute(query)

        row_headers = [x[0] for x in cursor.description]
        result_set = cursor.fetchall()
        lst_emails = []

        for row in result_set:
            lst_emails.append(dict(zip(row_headers, row)))

        for email in lst_emails:
            sendInternalEmails(email)

    except Exception as e:
        print('Erro em getEmailsToSend: ' + e)
        return False

    finally:
        cursor.close()
        cnxn.close()
        return True