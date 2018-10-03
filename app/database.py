from flask import session
import pyodbc
import json

def conSqlServer():
    cnxn = None

    try:
        server = '192.168.100.2'
        database = 'Finan'
        username = session['username']
        password = session['password']
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server Native Client 10.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    except:
        print('Erro ao conectar na base de dados!.')
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
    except:
        print('Erro ao buscar os e-mails com erros na base!')
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
			"   FILHO.STATUS_SOLIC_ORCAMENTO "
            "FROM"
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

    except:
        print('Erro ao buscar a lista de tarefas na base!')
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

    except:
        print('Erro ao buscar as listas de comentarios no Forum e informacoes da Tarefa!')
        return False
    finally:
        cursor.close()
        cnxn.close()
        return resultado

def setEmail(email):

    try:
        cnxn = conSqlServer()
        query = (
                " UPDATE MENSAGEM_NOTIFICACOES "
                " SET ERRO = 'N', "
                " TO_ADDRESS = replace(TO_ADDRESS , ?, ''), "
                " COPY_TO = replace(COPY_TO, ?, '') "
                " WHERE ERRO = 'S' AND ENVIADA = 'N' "
        )

        params = (email, email)

        cursor = cnxn.cursor()
        cursor.execute(query, params)
        cnxn.commit()

    except:
        print('Erro ao efetuar update dos e-mails com problema para VAZIO.')
        return False
    finally:
        cursor.close()
        cnxn.close()
        return True