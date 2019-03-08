from app.models import Mensagem_notificacoes, db
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def sendEmailsInterval():

    print(str(datetime.utcnow()) + ' : Iniciando envio de e-mails.')

    try:
        lst_emails = Mensagem_notificacoes.query.filter_by(enviada='N').all()
    except Exception as e:
        print('Não foi possível buscar a lista de notificações: {}'.format(e))
        return None

    for email in lst_emails:
        sendInternalEmails(email)
        try:
            print('Vai atualizar as informações do e-mail.')
            db.session.commit()
            print('Informações do e-mail atualizadas.')
        except Exception as e:
            print('Erro no procedimento para o e-mail {}'.format(email.idnotificacao))
            continue

    print(str(datetime.utcnow()) + ' : Finalizando envio de e-mails.')

    return True

def sendInternalEmails(email):
    try:
        server = smtplib.SMTP('mail.modallport.com.br', 587)

        if email.utiliza_layout == 'N':

            msg = MIMEMultipart('alternative')

            desc_mensagem = email.desc_mensagem

            # Retira a tag <SCRIPT>
            inicio = desc_mensagem.find('<SCRIPT')
            fim = desc_mensagem.find('</SCRIPT>') + len('</SCRIPT>')
            message_format = desc_mensagem[:inicio] + desc_mensagem[fim:]
            message = message_format

            to_address = email.to_address + ',' + email.copy_to
            to_address_plus_copy = [x.strip() for x in to_address.split(',')]

            msg['From'] = email.from_address
            msg['To'] = email.to_address
            msg['Subject'] = email.subject
            msg['Cc'] = email.copy_to
            msg.add_header('Content-Type', 'text/html')
            msg.attach(MIMEText(message, 'html'))

            #Loga no servidor SMTP
            server.login("arquivo.avaliacao.nc@modallport.com.br", "modal#7798")
            server.sendmail(email.from_address, to_address_plus_copy, msg.as_string())
            server.quit()

            #Atualiza as informações do objeto email
            email.erro = 'N'
            email.enviada = 'S'
            email.msg_erro = None

            return True
        else:
            email_content = ("""
                <html>
                    <head>
                        <title>Notificacao ModallPort</title>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style type="text/css">
                            body, table, td, a{
                                -webkit-text-size-adjust: 100%;
                                -ms-text-size-adjust: 100%;
                            }
                            table, td {
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                            }
                            img {
                                -ms-interpolation-mode: bicubic;
                            }        
                            img {
                                border: 0;
                                height: auto;
                                line-height: 100%;
                                outline: none;
                                text-decoration: none;
                            }     
                            table {
                                border-collapse: collapse !important;
                            }     
                            body {
                                height: 100% !important;
                                margin: 0 !important;
                                padding: 0 !important;
                                width: 100% !important;
                            }
                        </style>
                    </head>
                        <body style="margin: 0 !important; padding: 0 !important;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td bgcolor="#ffffff" align="center">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px;" class="wrapper">
                                            <tr>
                                                <td align="center" valign="top" style="padding: 10px 0;" class="logo">
                                                    <a href="http://www.modallport.com.br" target="_blank">
                                                        <img alt="Logo" src="http://www.modallport.com.br/shared/img/logo-modallport.gif" width="60" height="60" style="display: block; font-family: Helvetica, Arial, sans-serif; color: #ffffff; font-size: 16px;" border="0">
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#ffffff" align="center" style="padding: 5px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px;" class="responsive-table">
                                            <tr>
                                                <td>
                                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                                        <tr>
                                                            <td align="center" style="font-size: 24px; font-family: Helvetica, Arial, sans-serif; color: #333333; padding-top: 15px;" class="padding-copy">
                                                            """ + email.subject + """
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td align="left" style="padding: 15px 0 0 0; font-size: 16px; line-height: 26px; font-family: Helvetica, Arial, sans-serif; color: #666666;" class="padding-copy">
                                                            """ + email.desc_mensagem + """
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#ffffff" align="center" style="padding: 20px 0px;">
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" style="max-width: 500px;" class="responsive-table">
                                            <tr>
                                                <td align="center" style="font-size: 12px; line-height: 18px; font-family: Helvetica, Arial, sans-serif; color:#666666;">
                                                    <a href="http://www.modallport.com.br" target="_blank" style="color: #666666; text-decoration: none;"> ModallPort Sistemas Ltda &nbsp;&nbsp;|&nbsp;&nbsp; </a>
                                                    <a style="color: #666666; text-decoration: none;">Tel/Fax: 55 (47) 3348-0434</a>
                                                    <br>
                                                    <span style="font-family: Arial, sans-serif; font-size: 12px; color: #444444;"></span>
                                                    <a style="color: #666666; text-decoration: none;">Mensagem automática, gerada eletronicamente pelo serviço de notificação.</a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </body>
                </html>
            """)

            msg = MIMEMultipart('alternative')
            content = MIMEText(email_content, 'html')

            msg['Subject'] = email.subject
            msg['From'] = email.from_address
            msg['To'] = email.to_address
            msg['Cc'] = email.copy_to

            to_address = email.to_address + ',' + email.copy_to
            to_address_plus_copy = [x.strip() for x in to_address.split(',')]

            msg.add_header('Content-Type', 'text/html')
            msg.attach(content)

            #Loga no SMTP
            server.login("arquivo.avaliacao.nc@modallport.com.br", "modal#7798")
            server.sendmail(email.from_address, to_address_plus_copy, msg.as_string())
            server.quit()

            #Atualiza as informações do objeto email
            email.erro = 'N'
            email.enviada = 'S'
            email.msg_erro = None

            return True

    except Exception as e:
        msg = 'Não foi possível se conectar e enviar os e-mails no SMTP: {}'.format(e)
        
        #Atualiza as informações do objeto email
        email.erro = 'S'
        email.enviada = 'N'
        email.msg_erro = msg

        return False