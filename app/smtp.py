import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendInternalEmails(email):
    try:
        msg = MIMEMultipart('alternative')

        msg['Subject'] = email['SUBJECT']
        msg['From'] = email['FROM_ADDRESS']
        msg['To'] = email['TO_ADDRESS']

        if email['UTILIZA_LAYOUT'] == 'N':
            txt = email['DESC_MENSAGEM']
        else:
            txt = ("""
                  <html>
                      <head>
                                            <title>Notificação ModallPort</title>
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
                                                                                """ + email['SUBJECT'] + """
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td align="left" style="padding: 15px 0 0 0; font-size: 16px; line-height: 26px; font-family: Helvetica, Arial, sans-serif; color: #666666;" class="padding-copy">
                                                                                """ + email['DESC_MENSAGEM'] + """
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

        content = MIMEText(txt, 'html')

        msg.attach(content)

        s = smtplib.SMTP('mail.modallport.com.br', 587)
        s.login("arquivo.avaliacao.nc@modallport.com.br", "modal#7798")
        s.sendmail(email['FROM_ADDRESS'], email['TO_ADDRESS'], msg.as_string())
        s.quit()
    except Exception as e:
        print(e)