from email.mime.image import MIMEImage  # <-- Importante para a imagem
import smtplib
import os
import logging
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def enviar_email_pdf(destinatario, assunto, corpo, anexo, email_remetente=None):
    """
    Wrapper mínimo compatível com main.py — usa SMTP.
    """
    return enviar_email_smtp(destinatario, assunto, corpo, anexo, None)


def enviar_email_smtp(destinatario, assunto, corpo_html, caminho_anexo, caminho_imagem_embutida):
    seu_email = os.getenv("EMAIL_USER")
    sua_senha_de_app = os.getenv("EMAIL_PASSWORD")
    servidor_smtp = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    porta_smtp = int(os.getenv("SMTP_PORT", "587"))
    timeout = int(os.getenv("SMTP_TIMEOUT", "30"))

    # Pequeno atraso para evitar problemas de timing em GUIs
    time.sleep(0.5)

    if not seu_email or not sua_senha_de_app:
        raise ValueError(
            "Credenciais de e-mail não encontradas no arquivo .env (EMAIL_USER/EMAIL_PASSWORD)")

    if not caminho_anexo or not os.path.isfile(caminho_anexo):
        raise ValueError(f"Arquivo de anexo não encontrado: {caminho_anexo}")

    msg = MIMEMultipart('related')
    msg['From'] = seu_email
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # corpo HTML
    msg.attach(MIMEText(corpo_html or "", 'html'))

    # anexa PDF corretamente como application/pdf
    try:
        with open(caminho_anexo, 'rb') as attachment:
            part = MIMEBase('application', 'pdf')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename="{os.path.basename(caminho_anexo)}"')
        msg.attach(part)
    except FileNotFoundError:
        raise ValueError(f"Arquivo de anexo não encontrado: {caminho_anexo}")

    # anexa imagem embutida somente se fornecida e existente
    if caminho_imagem_embutida:
        if not os.path.isfile(caminho_imagem_embutida):
            raise ValueError(
                f"Arquivo de imagem não encontrado: {caminho_imagem_embutida}")
        with open(caminho_imagem_embutida, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<fence.logo1.png>')
            img.add_header('Content-Disposition', 'inline',
                           filename=os.path.basename(caminho_imagem_embutida))
            msg.attach(img)

    server = None
    try:
        server = smtplib.SMTP(servidor_smtp, porta_smtp, timeout=timeout)
        server.ehlo()
        try:
            server.starttls()
            server.ehlo()
        except Exception:
            logger.debug(
                "starttls não disponível/necessário para este servidor")
        server.login(seu_email, sua_senha_de_app)
        server.send_message(msg)
        print(f"E-mail enviado com sucesso para {destinatario}")
    except Exception as e:
        logger.exception("Falha ao enviar e-mail: %s", e)
        raise
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                try:
                    server.close()
                except Exception:
                    pass
