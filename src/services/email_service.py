import win32com.client as win32

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
