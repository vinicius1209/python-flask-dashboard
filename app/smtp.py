import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendInternalEmails(email):
    try:
        msg = MIMEMultipart('alternative')

        msg['Subject'] = email['SUBJECT']
        msg['From'] = email['FROM_ADDRESS']
        msg['To'] = email['TO_ADDRESS']

        txt = email['DESC_MENSAGEM']

        content = MIMEText(txt, 'html')
        msg.attach(content)

        s = smtplib.SMTP('mail.modallport.com.br', 587)
        s.login("arquivo.avaliacao.nc@modallport.com.br", "modal#7798")
        s.sendmail(email['FROM_ADDRESS'], email['TO_ADDRESS'], msg.as_string())
        s.quit()

    except Exception as e:
        print('Erro ao enviar o email interno de notificação: ' + email['IDNOTIFICACAO'] + '. Erro: ' + e)