import win32com.client as win32
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

# Função para enviar um email com anexo PDF usando Outlook

def enviar_email_pdf(destinatario, assunto, corpo, anexo, email_remetente=None):
    '''Envia um email com um anexo PDF usando o Outlook.
       Permite especificar um remetente diferente se necessário.'''

    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    if email_remetente:
        conta_encontrada = None
        for conta in outlook.Session.Accounts:
            if conta.SmtpAddress.lower() == email_remetente.lower():
                email.SendUsingAccount = conta
                conta_encontrada = True
                break
        if not conta_encontrada:
            raise ValueError(
                f"Conta de email '{email_remetente}' não encontrada no Outlook.")
        
    email.To = destinatario
    email.Subject = assunto
    email.HTMLBody = corpo
    email.Attachments.Add(anexo)

    email.Send()

def enviar_email_smtp(destinatario, assunto, corpo_html, caminho_anexo):
    """
    Envia um e--mail diretamente usando um servidor SMTP.
    """
    seu_email = os.getenv("EMAIL_USER")
    sua_senha_de_app = os.getenv("EMAIL_PASSWORD")

    if not seu_email or not sua_senha_de_app:
        raise ValueError("Credenciais de e-mail não encontradas no arquivo .env")

    servidor_smtp = "smtp.office365.com"
    porta_smtp = 587

    # Cria a estrutura do e-mail.
    msg = MIMEMultipart()
    msg['From'] = seu_email
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo_html, 'html'))

    # Anexa o arquivo PDF.
    try:
        with open(caminho_anexo, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(caminho_anexo)}',
        )
        msg.attach(part)
    except FileNotFoundError:
        raise ValueError(f"Arquivo de anexo não encontrado: {caminho_anexo}")

    # Conecta-se ao servidor e envia o e-mail.
    try:
        server = smtplib.SMTP(servidor_smtp, porta_smtp)
        server.starttls()
        server.login(seu_email, sua_senha_de_app)
        texto_email = msg.as_string()
        server.sendmail(seu_email, destinatario, texto_email)
        server.quit()
    except Exception as e:
        raise e