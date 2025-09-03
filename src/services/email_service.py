import win32com.client as win32
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
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

# Certifique-se de ter todos estes imports no início do seu arquivo
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage # <-- Importante para a imagem
from email import encoders

def enviar_email_smtp(destinatario, assunto, corpo_html, caminho_anexo, caminho_imagem_embutida):
    """
    Envia um e-mail completo com HTML, anexo PDF e imagem embutida.
    """
    seu_email = os.getenv("EMAIL_USER")
    sua_senha_de_app = os.getenv("EMAIL_PASSWORD")

    if not seu_email or not sua_senha_de_app:
        raise ValueError("Credenciais de e-mail não encontradas no arquivo .env")

    # MUDANÇA 1: Uso de 'related' para que o HTML possa se relacionar com a imagem embutida.
    msg = MIMEMultipart('related')
    msg['From'] = seu_email
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Anexa o corpo principal em HTML.
    msg.attach(MIMEText(corpo_html, 'html'))

    # Anexa o arquivo PDF (seu código original já estava correto).
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

    # Adiciona imagem embutida
    try:
        with open(caminho_imagem_embutida, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<fence.logo1.png>')
            msg.attach(img)
    except FileNotFoundError:
        raise ValueError(f"Arquivo de imagem não encontrado: {caminho_imagem_embutida}")

    # Conecta-se ao servidor e envia o e-mail.
    try:
        servidor_smtp = "smtp.gmail.com"
        porta_smtp = 587
        server = smtplib.SMTP(servidor_smtp, porta_smtp)
        server.starttls()
        server.login(seu_email, sua_senha_de_app)
        server.send_message(msg) # Usar send_message é mais moderno e seguro para multipartes
        server.quit()
        print(f"E-mail enviado com sucesso para {destinatario}")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")
        raise e