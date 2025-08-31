import win32com.client as win32

# Função para enviar um email com anexo PDF usando Outlook


def enviar_email_pdf(destinatario, assunto, corpo, anexo):
    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.To = destinatario
    email.Subject = assunto
    email.HTMLBody = corpo
    email.Attachments.Add(anexo)
    email.Send()
