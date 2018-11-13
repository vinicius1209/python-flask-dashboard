import smtplib
import email.mime.message as em
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendInternalEmails(email):
    try:
        server = smtplib.SMTP('mail.modallport.com.br', 587)

        if email.utiliza_layout == 'N':
            msg = MIMEMultipart()
            message = email.desc_mensagem

            to_address = email.to_address + ',' + email.copy_to
            to_address_plus_copy = [x.strip() for x in to_address.split(',')]

            msg['From'] = email.from_address
            msg['To'] = email.to_address
            msg['Subject'] = email.subject
            msg['Cc'] = email.copy_to

            msg.attach(MIMEText(message, 'plain'))

            server.login("arquivo.avaliacao.nc@modallport.com.br", "modal#7798")
            server.sendmail(email.from_address, to_address_plus_copy, msg.as_string().encode('utf-8'))
            server.quit()
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
            msg = em.message.Message()

            msg['Subject'] = email.subject
            msg['From'] = email.from_address
            msg['To'] = email.to_address
            msg['Cc'] = email.copy_to

            to_address = email.to_address + ',' + email.copy_to
            to_address_plus_copy = [x.strip() for x in to_address.split(',')]

            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)

            server.login("arquivo.avaliacao.nc@modallport.com.br", "modal#7798")
            server.sendmail(email.from_address, to_address_plus_copy, msg.as_string().encode('utf-8'))
            server.quit()

    except Exception as e:
        print(e)
